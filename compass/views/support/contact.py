# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import OMADContactQueue
from compass.views.support import CompassSupportAPI


def build_omad_contact_queue():
    return [
        {
            'id': c.id,
            'created': c.created.isoformat() if c.created else None,
            'processing_attempts': c.processing_attempts,
            'process_attempted_date': (
                c.process_attempted_date.isoformat()
                if c.process_attempted_date else None
            ),
            'processing_error': c.processing_error,
            'json': c.json,
            'stack_trace': c.stack_trace,
        }
        for c in OMADContactQueue.objects.all().order_by('created')
    ]


class OMADContactQueueView(CompassSupportAPI):
    '''
    API endpoint returning queued OMAD contacts for support admins.

    /api/internal/support/omad_contact_queue/
    '''

    def get(self, request):
        return self.response_ok(build_omad_contact_queue())
