# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.dao.person import valid_system_key
from compass.dao import current_datetime_utc
from compass.models import AccessGroup, Student, AppUser, SpecialProgram
from compass.serializers import SpecialProgramSerializer
from compass.exceptions import OverrideNotPermitted, InvalidSystemKey
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError
import json
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


class SpecialProgramView(BaseAPIView):
    '''
    API endpoint to retrieve and modify SpecialProgram metadata

    /api/internal/student/[systemkey]/special_program/
    '''
    def get(self, request, systemkey):
        data = {}
        try:
            access_group = self.get_access_group(request)
            student = self._get_student(systemkey)

            sps = SpecialProgram.objects.get(
                access_group=access_group, student=student)

            serializer = SpecialProgramSerializer(sps)
            return self.response_ok(serializer.data)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except InvalidSystemKey:
            return self.response_badrequest('Invalid systemkey')
        except ValueError:
            return self.response_badrequest('Invalid program code')
        except SpecialProgram.DoesNotExist:
            return self.response_notfound("No Metadata found.")

    def post(self, request, systemkey):
        try:
            self.valid_user_permission(request, require_manager=True)
            student = self._get_student(systemkey)
            access_group = self.get_access_group(request)
            app_user = self.get_app_user()

            special_program = request.data.get('special_program')
            program_date = datetime.strptime(
                special_program.get("program_date"), '%Y-%m-%d').date()

            ssp = SpecialProgram(
                access_group=access_group, student=student,
                program_date=program_date, modified_by=app_user,
                modified_date=current_datetime_utc())
            ssp.save()

            serializer = SpecialProgramSerializer(ssp)
            logger.info(f"SpecialProgram for {systemkey} saved: "
                        f"{serializer.data}")
            return self.response_created(serializer.data)
        except InvalidSystemKey:
            return self.response_badrequest('Invalid systemkey')
        except ValueError:
            return self.response_badrequest('Invalid Request Data')
        except (PermissionDenied, AccessGroup.DoesNotExist):
            return self.response_unauthorized()
        except IntegrityError:
            return self.response_badrequest("Prior Special Program Record")
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

    def put(self, request, systemkey):
        if not valid_system_key(systemkey):
            return self.response_badrequest("Invalid systemkey")

        try:
            self.valid_user_permission(request, require_manager=True)
            access_group = self.get_access_group(request)
            app_user = self.get_app_user()
            student = Student.objects.get(system_key=systemkey)

            special_program = request.data.get('special_program')
            program_date = datetime.strptime(
                special_program.get("program_date"), '%Y-%m-%d').date()

            ssp = SpecialProgram.objects.get(
                access_group=access_group, student=student)
            ssp.program_date = program_date
            ssp.modified_by = app_user
            ssp.modified_date = current_datetime_utc()
            ssp.save()

            serializer = SpecialProgramSerializer(ssp)
            logger.info(f"SpecialProgram for {systemkey} updated: "
                        f"{serializer.data}")
            return self.response_ok(serializer.data)
        except InvalidSystemKey:
            return self.response_badrequest('Invalid systemkey')
        except (SpecialProgram.DoesNotExist, ValueError):
            return self.response_badrequest('Invalid Request Data')
        except (PermissionDenied, AccessGroup.DoesNotExist):
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

    def delete(self, request, systemkey):
        try:
            self.valid_user_override()

            sps = SpecialProgram.objects.get(
                access_group=self.get_access_group(request),
                student=self._get_student(systemkey))

            sps.delete()
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except InvalidSystemKey:
            return self.response_badrequest('Invalid systemkey')
        except (ValueError, SpecialProgram.DoesNotExist):
            return self.response_badrequest('No Special Program')
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

        return self.response_ok("Metadata deleted.")

    def _get_student(self, systemkey):
        if not valid_system_key(systemkey):
            raise InvalidSystemKey()

        student, _ = Student.objects.get_or_create(system_key=systemkey)

        return student
