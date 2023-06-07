# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
from compass.clients import CompassPersonClient
from compass.dao.group import is_group_member
from uw_gws import GWS
from restclients_core.exceptions import DataFailureException


class AppUserManager(models.Manager):
    def upsert_appuser(self, uwnetid):
        """
        New app users are created when they first create content in
        the app, such as a new contact. This record is only used to associate
        data to a user of the system, login credentials are determined by UW
        group memberships. Since uwnetids may change over time, this method
        uses the PDS to resolve prior netids and then update them in Compass as
        needed.
        """
        # request the current person object for the user
        person = CompassPersonClient().get_person_by_uwnetid(uwnetid)
        # check the AppUser table to see if they have an existing entry
        for netid in (person.prior_uwnetids + [person.uwnetid]):
            try:
                # update the AppUsers uwnetid
                user = AppUser.objects.get(uwnetid=netid)
                user.uwnetid = person.uwnetid
                user.save()
                return user
            except AppUser.DoesNotExist:
                continue
        else:
            # if no user is found, then create one
            user = AppUser(uwnetid=uwnetid)
            user.save()
            return user


class AppUser(models.Model):
    """
    User of the app that content, such as contacts, is associated with.
    """

    objects = AppUserManager()

    uwnetid = models.CharField(unique=True, max_length=50)

    # A user's Access Group affiliation is derived at login via GWS Groups.
    # A GWS group key is generated using the <access_id>. It is important to
    # notethat UW Group memberships are managed externally from the app

    class Meta:
        indexes = [
            models.Index(fields=["uwnetid"]),
        ]

    def __str__(self):
        return f"{self.uwnetid}"


class Student(models.Model):
    """
    The student model is used to associate app data to a student. In this app
    only system_key is stored as it provides a unique key that is used to
    request student information from the PDS. Besides system-key, no student
    information is ever stored in the app, all student data is fetched directly
    from the PDS since it is kept up to date via automated jobs.
    """

    system_key = models.CharField(unique=True, max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["system_key"]),
        ]

    def __str__(self):
        return self.system_key


class AccessGroupManager(models.Manager):
    def by_name(self, name):
        return AccessGroup.objects.get(name=name)

    def get_roles_for_user(self, request):
        """
        Return the unique roles for a user, without group context.
        """
        roles = []
        for group in super().get_queryset().all():
            for role in AccessGroup.ROLES:
                if role not in roles and is_group_member(
                    request, group.authz_group_id(role)
                ):
                    roles.append(role)
        return roles

    def get_access_groups_for_netid(self, uwnetid):
        """
        Returns the list of access groups that a uwnetid is a member of
        """
        access_groups = []
        try:
            for access_group in AccessGroup.objects.all():
                groups = GWS().search_groups(
                    member=uwnetid, name=f"{access_group.access_group_id}*"
                )
                if groups:
                    access_groups.append(access_group)
        except DataFailureException:
            pass
        return access_groups

    def is_access_group_member(self, uwnetid, access_group):
        user_access_groups = self.get_access_groups_for_netid(uwnetid)
        if access_group in user_access_groups:
            return True
        return False


class AccessGroup(models.Model):
    """
    AccessGroups manage their Affiliation, ContactTopic, ContactType, and
    ContactMethod lists. AccessGroup membership is defined externally in
    UW groups (Astra) and determined for a AppUser via a request to the
    GWS at login. Contact records created by a member of one access group
    are only visible to other members of that same access group.

    Access groups for the app are created in the Django Admin. The
    access_group_id is the prefix of the uw-groups (user and manger) that it
    is affiliated with. For example, there are two uw-groups for OMAD named
    u_astra_compass_omad-manager and u_astra_compass_omad-user. Within the
    Django Admin there is then an associated AccessGroup with an
    access_group_id of 'u_astra_compass_omad'. The access_group_id associates
    the membership of a uw-group to the apps AccessGroup, thereby controlling
    access to content within the app.
    """

    ROLE_MANAGER = "manager"
    ROLE_USER = "user"
    ROLES = [ROLE_MANAGER, ROLE_USER]

    objects = AccessGroupManager()

    name = models.CharField(unique=True, max_length=50)
    access_group_id = models.CharField(unique=True, max_length=50)

    def save(self, *args, **kwargs):
        created = not self.pk
        super(AccessGroup, self).save(*args, **kwargs)
        if created:
            # set uneditable contact type presets
            uneditable_contact_types = [
                "Quick Question",
                "Appointment",
                "Workshop",
            ]
            for contact_type_name in uneditable_contact_types:
                ContactType(
                    access_group=self, name=contact_type_name, editable=False
                ).save()
            # set uneditable contact methods presets
            uneditable_contact_methods = [
                "In-person",
                "Telephone",
                "Video Conference",
            ]
            for contact_method_name in uneditable_contact_methods:
                ContactMethod(
                    access_group=self, name=contact_method_name, editable=False
                ).save()
            # set default contact topics
            default_contact_topics = [
                "Add/Drop a Class",
            ]
            for contact_topic_name in default_contact_topics:
                ContactTopic(access_group=self, name=contact_topic_name).save()

    def authz_group_id(self, role):
        return "{}-{}".format(self.access_group_id, role)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<AccessGroup(name='{self.name}')>"

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, AccessGroup):
            return self.access_group_id == other.access_group_id
        return False

    def has_role(self, request, role):
        return is_group_member(request, self.authz_group_id(role))


class Contact(models.Model):
    """
    A contact/appointment with a student. For OMAD contacts are generated
    via the automated check-in system and updated by advisers, or created
    manually by advisers.
    """

    # required fields
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    access_group = models.ManyToManyField("AccessGroup")
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    contact_type = models.ForeignKey("ContactType", on_delete=models.CASCADE)
    contact_method = models.ForeignKey("ContactMethod",
                                       on_delete=models.CASCADE, null=True)
    checkin_date = models.DateTimeField()
    # optional fields
    noshow = models.BooleanField(default=False)
    notes = models.TextField(default=None, blank=True, null=True)
    actions = models.TextField(default=None, blank=True, null=True)
    contact_topics = models.ManyToManyField("ContactTopic")
    # generated by check-in queue system
    source = models.CharField(default="Compass", max_length=50)
    # contact history fields
    created_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(history_user_id_field="app_user")

    # The history user feature is a Django App used to track changes to
    # contacts. Although we don't currently display this in the UW, it is
    # accessible via the Django Admin.

    @property
    def _history_user(self):
        return self.app_user

    @_history_user.setter
    def _history_user(self, value):
        self.app_user = value

    def __str__(self):
        return f"{self.app_user} w/ {self.student} @ {self.checkin_date}"


class BaseAccessGroupContent(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        created = not self.pk
        if created:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StudentAffiliation(models.Model):
    """
    Affiliation assigned to a student
    """
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    affiliation = models.ForeignKey("Affiliation", on_delete=models.CASCADE)
    cohorts = models.ManyToManyField("Cohort")
    date = models.DateField(null=True)
    actively_advised = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} {self.affiliation}"


class Affiliation(BaseAccessGroupContent):
    """
    Departmental/Group Affiliation
    (e.g. CAMP, TRIO, SSS, Champions, IC Eligible)
    """
    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    active = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)


class Cohort(models.Model):
    start_year = models.SmallIntegerField()
    end_year = models.SmallIntegerField()


class ContactType(BaseAccessGroupContent):
    """
    Type of contact with a student. These are created for a given access group
    by the access group managers. Examples include Quick Question, Appointment,
    and Workshop.
    """

    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    active = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)


class ContactMethod(BaseAccessGroupContent):
    """
    The method used in the contact. These are created for a given access group
    by the access group managers. Examples include Telephone, In-Person,
    and Video Conference.
    """

    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    active = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)


class ContactTopic(BaseAccessGroupContent):
    """
    Topics discussed with a student. These are created for a given access group
    by the access group managers. Examples include Add/Drop Class,
    Join/Affiliate, Academic Difficulties, Hardship Withdrawl, Internships,
    Research Opportunities, Graduate Professional School, and
    Testing/Assessment.
    """

    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    active = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)


class StudentEligibility(models.Model):
    """
    Services and resources for which a Student is provided access
    """
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE)
    eligibility = models.ManyToManyField("EligibilityType")


class EligibilityType(BaseAccessGroupContent):
    """
    A service or resource that is available to students
    """
    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    editable = models.BooleanField(default=True)


class Visit(models.Model):
    """
    Student interaction with service
    """
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    visit_type = models.ForeignKey("VisitType", on_delete=models.CASCADE)
    course_code = models.CharField(max_length=64)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()


class VisitType(BaseAccessGroupContent):
    """
    Type of student visit. These are created for a given access group
    by the access group managers. Examples include IC Drop-In Tutoring and
    and IC Workshop
    """
    access_group = models.ForeignKey("AccessGroup", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    editable = models.BooleanField(default=False)
