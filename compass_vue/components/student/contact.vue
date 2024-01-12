<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts</axdd-card-heading>
      <axdd-card-action>
        <AddEditContact
          :button-type="'button'"
          :person="person"
          @contactUpdated="loadStudentContacts()"
          ><i class="bi bi-calendar-plus text-dark me-2"></i>Record new
          contact</AddEditContact
        >
      </axdd-card-action>
    </template>
    <template #body>
      <template v-if="contacts.length > 0">
        <div class="table-responsive m-n3">
          <table class="table m-0">
            <thead class="table-light text-muted small">
              <tr>
                <th class="ps-3">Details</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="contact in contacts" :key="contact.id">
                <td class="ps-3 align-bottom">
                  <div class="small d-flex justify-content-between mb-4">
                    <div>
                      <strong>{{ contact.app_user.display_name }}</strong>
                      <span class="text-secondary ms-1"
                        >({{ contact.app_user.uwnetid }})</span
                      >
                    </div>
                    <div class="text-secondary">
                      <i class="bi bi-calendar-event text-gray me-1"></i>
                      {{ getTimeFromNow(contact.checkin_date) }}
                    </div>
                  </div>

                  <template v-if="contact.contact_type">
                    <div
                      v-if="contact.contact_type.slug == 'parent'"
                      class="badge rounded-pill text-bg-danger border-0 px-2 py-1 m-0 me-2"
                    >
                      {{ contact.contact_type.name }}
                    </div>

                    <div
                      v-else-if="contact.contact_type.slug == 'admin'"
                      class="badge rounded-pill text-bg-primary border-0 px-2 py-1 m-0 me-2"
                    >
                      {{ contact.contact_type.name }}
                    </div>

                    <div
                      v-else
                      class="badge rounded-pill text-bg-dark-purple border-0 px-2 py-1 m-0 me-2"
                    >
                      {{ contact.contact_type.name }}
                    </div>
                  </template>

                  <div
                    v-if="contact.contact_method"
                    class="badge rounded-pill text-bg-light-gray border-0 px-2 py-1 m-0 me-1"
                  >
                    {{ contact.contact_method.name }}
                  </div>

                  <ul
                    v-if="contact.contact_topics"
                    class="list-unstyled mt-1 mb-0"
                  >
                    <template v-for="topic in contact.contact_topics">
                      <li
                        v-if="topic.slug !== 'none'"
                        :key="topic.id"
                        class="badge rounded-pill text-bg-dark-beige border-0 px-2 py-1 mb-0 me-1"
                      >
                        {{ topic.name }}
                      </li>
                    </template>
                  </ul>

                  <template v-if="contact.contact_type">
                    <div
                      v-if="contact.contact_type.slug == 'parent'"
                      class="my-3"
                    >
                      <span class="small text-muted visually-hidden"
                        >Parent</span
                      >
                      <div class="text-danger fs-8">
                        <i class="bi bi-exclamation-octagon-fill me-1"></i
                        >Parent contacts should not be discussed this contact
                        with their student.
                      </div>
                    </div>
                  </template>

                  <div v-if="contact.notes" class="mt-3">
                    <span class="small visually-hidden">Notes</span>
                    <p class="text-dark small text-break">
                      {{ contact.notes }}
                    </p>
                  </div>
                  <div
                    v-if="contact.actions"
                    class="border-top border-light pt-3"
                  >
                    <span class="small visually-hidden">Actions</span>
                    <p class="small text-break">
                      {{ contact.actions }}
                    </p>
                  </div>

                  <div class="mt-4 small d-flex justify-content-between">
                    <div class="text-secondary">
                      {{
                        formatUTCToLocalDateAndTimeZone(
                          contact.checkin_date,
                          "LLL"
                        )
                      }}
                    </div>
                    <div v-show="contact.source == 'Checkin'">
                      <i class="bi bi-journal-check text-gray me-1"></i
                      >{{ contact.source }} {{ contact.trans_id }}
                    </div>
                  </div>
                </td>
                <td style="width: 25%" class="p-3 text-end">
                  <!-- MARK: user/student role functionality -->
                  <template
                    v-if="
                      (userRoles.includes(Role.User) &&
                        inUserAccessGroup(contact)) ||
                      (userRoles.includes(Role.Student) &&
                        inUserAccessGroup(contact))
                    "
                  >
                    <!-- MARK: check if user matches override. not overriding. -->
                    <template v-if="userName == userOverride">
                      <AddEditContact
                        v-if="contact.app_user.uwnetid == userName"
                        :button-type="'link'"
                        :person="person"
                        :contact-id="contact.id"
                        @contactUpdated="loadStudentContacts()"
                        ><i class="bi bi-pencil text-dark me-2"></i
                        >Edit</AddEditContact
                      >
                    </template>
                    <!-- MARK: if not, user is overriding. show edit button for override user. -->
                    <template v-else>
                      <AddEditContact
                        v-if="contact.app_user.uwnetid == userOverride"
                        :button-type="'link'"
                        :person="person"
                        :contact-id="contact.id"
                        @contactUpdated="loadStudentContacts()"
                        ><i class="bi bi-pencil text-dark me-2"></i
                        >Edit</AddEditContact
                      >
                    </template>
                  </template>

                  <!-- MARK: manager(ES) role funtionality -->
                  <template
                    v-if="
                      userRoles.includes(Role.Manager) &&
                      inUserAccessGroup(contact)
                    "
                  >
                    <ManagerEditContact
                      :button-type="'link'"
                      :person="person"
                      :contact-id="contact.id"
                      @contactUpdated="loadStudentContacts()"
                    >
                      <i class="bi bi-pencil text-danger me-2"></i
                      ><span class="text-danger">Edit</span>
                    </ManagerEditContact>
                    <DeleteContact
                      :button-type="'link'"
                      :person="person"
                      :contact-id="contact.id"
                      @contactDeleted="removeContact(contact.id)"
                      ><i class="bi bi-trash text-danger me-2"></i
                      ><span class="text-danger">Delete</span>
                    </DeleteContact>
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
      <template v-else>
        <p>No contacts found</p>
      </template>
    </template>
  </axdd-card>
</template>

<script>
import AddEditContact from "@/components/add-contact.vue";
import ManagerEditContact from "@/components/add-contact.vue";
import DeleteContact from "@/components/delete-contact.vue";
import { Role } from "@/utils/roles";
import { formatUTCToLocalDateAndTimeZone, getTimeFromNow } from "@/utils/dates";
import { getStudentContacts } from "@/utils/data";

export default {
  components: {
    AddEditContact,
    ManagerEditContact,
    DeleteContact,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      formatUTCToLocalDateAndTimeZone,
      getTimeFromNow,
      getStudentContacts,
    };
  },
  data() {
    return {
      contacts: {},
      userName: document.body.getAttribute("data-user-netid"),
      userOverride: document.body.getAttribute("data-user-override"),
      userRoles: document.body.getAttribute("data-user-role").split(","),
      userAccessGroup: document.body.getAttribute("data-user-access-group"),
      Role: Role,
    };
  },
  created() {
    this.loadStudentContacts();
  },
  methods: {
    loadStudentContacts: function () {
      this.getStudentContacts(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.contacts = response.data;
          }
        }
      );
    },
    inUserAccessGroup: function (contact) {
      return contact.access_group.some(
        (group) => group.access_group_id === this.userAccessGroup
      );
    },
    removeContact: function (contactId) {
      this.contacts = this.contacts.filter(
        (contact) => contact.id !== contactId
      );
    },
  },
};
</script>

<style lang="scss">
tbody {
  td {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
  }
}
</style>
