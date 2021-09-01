# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao import EdwDAO
from django.views.generic import TemplateView


class PageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        edw_dao = EdwDAO()
        enrolled_students_df = edw_dao.get_enrolled_students_df()
        context = super().get_context_data(**kwargs)
        context["enrolled_students"] = enrolled_students_df.to_dict('records')
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(PageView, self).render_to_response(context,
                                                            **response_kwargs)
        return response
