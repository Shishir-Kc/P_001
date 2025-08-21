import datetime
from student import models as std
from data_class.models import YEAR_MONTH


def is_std_data_filled(pk):
    is_done = std.Attendence.objects.filter(
        student=pk,
        date_month=datetime.date.today(),
    ).exists()
    if is_done:
        return True
    else:
        return False


def filtered_month(date):
    month = str(date)
    filtered_month = int((month[6:][:-3]))
    return filtered_month


def total_days():
    current_month = YEAR_MONTH.objects.get(
        current_year=datetime.date.today().year,
        month=filtered_month(date=datetime.date.today())
    )
    data = {
        'number_of_days': current_month.number_of_days,
        'number_of_holidays': current_month.holiday,
        'number_of_unexpected_holidays': current_month.unexpected_holiday,
    }
    return data


def current_month(date):
    MONTH = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    return MONTH.get(date, "invalid month")


def total_class_attained_missed_this_month(pk, type_request):
    student = std.Student_info.objects.get(id=pk)
    today = datetime.date.today()
    year_month_obj = YEAR_MONTH.objects.get(
        month=today.month,
        current_year=today.year
    )

    if type_request == "attained":
        data = std.Attendence.objects.filter(
            student=student,
            attendence=year_month_obj,
            attended_class=True
        ).count()
        return data

    elif type_request == "missed":
        data = std.Attendence.objects.filter(
            student=student,
            attendence=year_month_obj,
            attended_class=False
        ).count()
        return data
