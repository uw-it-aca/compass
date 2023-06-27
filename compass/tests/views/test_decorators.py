# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from userservice.user import UserServiceMiddleware
from compass.views.decorators import uw_person_required
import mock


@method_decorator(uw_person_required, name='dispatch')
class PersonRequiredView(View):
    def get(request, *args, **kwargs):
        return HttpResponse('OK')


class DecoratorTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user = User()
        self.request.session = {}
        UserServiceMiddleware().process_request(self.request)
        get_response = mock.MagicMock()
        middleware = SessionMiddleware(get_response)
        response = middleware(self.request)
        self.request.session.save()

    @mock.patch('compass.context_processors.auth_user')
    def test_person_required_noauth(self, mock_auth_user):
        mock_auth_user.return_value = {}
        self.request.user = AnonymousUser()

        view_instance = PersonRequiredView.as_view()
        response = view_instance(self.request)
        self.assertEquals(response.status_code, 302)
        self.assertIn('%s?next=/' % settings.LOGIN_URL, response.url,
                      'Login required')

    @mock.patch('compass.context_processors.auth_user')
    @mock.patch('compass.views.decorators.get_user')
    def test_person_required_fail(self, mock_get_user, mock_auth_user):
        mock_get_user.return_value = 'fake'
        mock_auth_user.return_value = {}
        view_instance = PersonRequiredView.as_view()
        response = view_instance(self.request)
        self.assertEquals(response.status_code, 401)

    @mock.patch('compass.views.decorators.get_user')
    def test_person_required_success(self, mock_get_user):
        mock_get_user.return_value = 'javerage'
        view_instance = PersonRequiredView.as_view()
        response = view_instance(self.request)
        self.assertEquals(response.status_code, 200)
