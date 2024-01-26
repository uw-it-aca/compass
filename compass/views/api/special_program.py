# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.dao.person import valid_system_key
from compass.dao import current_datetime_utc
from compass.models import AccessGroup, Student, AppUser, SpecialProgram
from compass.serializers import SpecialProgramSerializer
from compass.exceptions import OverrideNotPermitted
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError
import json
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


class SpecialProgramView(BaseAPIView):
    '''
    API endpoint to retrieve and modify SpecialProgram metadata

    /api/internal/student/[systemkey]/special_program/[program_code]
    '''
    def get(self, request, systemkey, program_code):
        data = {}
        try:
            access_group = self.get_access_group(request)

            if not valid_system_key(systemkey):
                return self.response_badrequest('Invalid systemkey')

            sps = SpecialProgram.objects.get(
                access_group=access_group, student__system_key=systemkey,
                program_code=int(program_code))

            serializer = SpecialProgramSerializer(sps)
            data = serializer.data
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except ValueError:
            return self.response_badrequest('Invalid program code')
        except SpecialProgram.DoesNotExist:
            return self.response_notfound("No Metadata found.")

        return self.response_ok(data)

    def post(self, request, systemkey, program_code):
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

            ssp = SpecialProgram(
                access_group=access_group, student=student,
                program_code=int(program_code), program_date=program_date,
                modified_by=app_user, modified_date=current_datetime_utc())
            ssp.save()
                
            serializer = SpecialProgramSerializer(ssp)
            logger.info(f"SpecialProgram for {systemkey} saved: "
                        f"{serializer.data}")
            return self.response_created(serializer.data)
        except Student.DoesNotExist:
            return self.response_notfound("Unknown student")
        except ValueError:
            return self.response_badrequest('Invalid Request Data')
        except (PermissionDenied, AccessGroup.DoesNotExist):
            return self.response_unauthorized()
        except IntegrityError:
            return self.response_badrequest("Prior Special Program Record")
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

    def put(self, request, systemkey, program_code):
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
                access_group=access_group, student=student,
                program_code=int(program_code))
            ssp.program_date = program_date
            ssp.modified_by = app_user
            ssp.modified_date = current_datetime_utc()
            ssp.save()

            serializer = SpecialProgramSerializer(ssp)
            logger.info(f"SpecialProgram for {systemkey} updated: "
                        f"{serializer.data}")
            return self.response_ok(serializer.data)
        except Student.DoesNotExist:
            return self.response_notfound("Unknown student")
        except (SpecialProgram.DoesNotExist, ValueError):
            return self.response_badrequest('Invalid Request Data')
        except (PermissionDenied, AccessGroup.DoesNotExist):
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

    def delete(self, request, systemkey, program_code):
        try:
            access_group = self.get_access_group(request)

            self.valid_user_override()

            if not valid_system_key(systemkey):
                return self.response_badrequest('Invalid systemkey')

            sps = SpecialProgram.objects.get(
                access_group=access_group, student__system_key=systemkey,
                program_code=int(program_code))

            sps.delete()
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except (ValueError, SpecialProgram.DoesNotExist):
            return self.response_badrequest('Invalid student or program codee')
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

        return self.response_ok("Metadata deleted.")
