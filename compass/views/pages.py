# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import TemplateView
from userservice.user import UserService
from compass.models import AccessGroup


@method_decorator(login_required, name='dispatch')
class LandingView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        roles = AccessGroup.objects.get_roles_for_user(self.request)

        context = super().get_context_data(**kwargs)
        context['user_netid'] = UserService().get_original_user()
        context['user_role'] = ','.join(sorted(roles))
        context['signout_url'] = reverse('saml_logout')
        context['ga_key'] = getattr(settings, 'GOOGLE_ANALYTICS_KEY', None)
        context['user_override'] = UserService().get_user()
        return context
