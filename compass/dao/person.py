# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from uw_pws import PWS
from restclients_core.exceptions import DataFailureException, InvalidNetID


def is_netid(username):
    pws = PWS()
    error_msg = "No override user supplied, please enter a UWNetID"
    if username is not None and len(username) > 0:
        try:
            user = pws.get_entity_by_netid(username.lower())
            if username.lower() == user.uwnetid:
                error_msg = None
            else:
                error_msg = "Current netid: {}, Prior netid: ".format(
                    user.uwnetid)
        except InvalidNetID:
            error_msg = "Not a valid UWNetID: "
        except DataFailureException as err:
            error_msg = "Error ({}) {}: ".format(err.status, err.msg)
    return error_msg
