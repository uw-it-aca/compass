# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_sws.term import get_term_by_date, get_term_after
from compass.dao import current_datetime
import datetime


def current_term():
    return get_term_by_date(current_datetime().date())


def week_of_term(term, current_date):
    """
    Returns the calendar week of the term for the given date.
    """
    start_date = term.first_day_quarter
    start_of_first_week = start_date - datetime.timedelta(
        days=start_date.isoweekday() % 7)
    difference = (current_date - start_of_first_week).days
    return difference // 7 + 1


def current_week():
    curr_term = current_term()
    current_dt = current_datetime()
    return week_of_term(curr_term, current_dt.date())

def term_context():
    curr_term = current_term()
    next_term = get_term_after(curr_term)
    current_dt = current_datetime()
    is_break = False
    is_finals = False

    break_term = curr_term
    if current_dt.date() > curr_term.last_final_exam_date:
        is_break = True
        break_term = next_term

    if (current_dt.date() > curr_term.last_day_instruction and
            current_dt.date() <= curr_term.last_final_exam_date):
        is_finals = True

    return {
        'current_date': current_dt.date().isoformat(),
        'current_term_year': curr_term.year,
        'current_term_quarter': curr_term.quarter,
        'next_term_year': next_term.year,
        'next_term_quarter': next_term.quarter,
        'term_first_day': curr_term.first_day_quarter.isoformat(),
        'term_last_day': curr_term.last_day_instruction.isoformat(),
        'aterm_last_day': curr_term.aterm_last_date.isoformat() if (
            curr_term.aterm_last_date is not None) else None,
        'bterm_first_day': curr_term.bterm_first_date.isoformat() if (
            curr_term.bterm_first_date) else None,
        'last_final_exam_date': curr_term.last_final_exam_date.isoformat(),
        'term_week': week_of_term(curr_term, current_dt.date()),
        'is_finals': is_finals,
        'is_break': is_break,
        'break_term_year': break_term.year,
        'break_term_quarter': break_term.quarter,
    }
