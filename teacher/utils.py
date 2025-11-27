import datetime
from student import models as std
import nepali_datetime



def get_date():
    return nepali_datetime.datetime.now().strftime("%d")

def get_month():
    return nepali_datetime.datetime.now().strftime("%B")

def get_year():
    return nepali_datetime.datetime.now().strftime("%Y")

def get_day():
    day = nepali_datetime.datetime.now().strftime("%A")
    return day[:3]

def get_todays_date():
    return f"{get_date()} {get_month()} {get_year()} {get_day()}"

def number_of_absent_students(student_obj):
    from data_class.models import Attendance
    attendance = Attendance.objects.get(year=get_year(),month=get_month(),date=get_date())
    num_of_absent_std = std.Student_Attendance.objects.filter(student__in=student_obj,attendance=attendance,attended=False).count()
    return num_of_absent_std


def number_of_present_students(student_obj):
    from data_class.models import Attendance
    attendance = Attendance.objects.get(year=get_year(),month=get_month(),date=get_date())
    num_of_present_std = std.Student_Attendance.objects.filter(student__in=student_obj,attendance=attendance,attended=True).count()
    return num_of_present_std

def total_days_absent(student_id):
    """
        returns total number of days a student was absent in a month 
    
    """
    try:
        from data_class.models import Attendance
        student = std.Student_info.objects.get(id=student_id)
        attendance_rec = Attendance.objects.filter(year=get_year(),month=get_month())
        total_absent_days = std.Student_Attendance.objects.filter(student=student,attendance__in=attendance_rec,attended=False).count()
        return total_absent_days
    except Exception as e:
        print("Error in total_days_absent util func")
        print(e)
        return 0


def total_days_present(student_id):
    """
        returns total number of days a student was present in a month 
    
    """
    try: 
        from data_class.models import Attendance
        student = std.Student_info.objects.get(id=student_id)
        attendance_rec = Attendance.objects.filter(year=get_year(),month=get_month())
        total_present_days = std.Student_Attendance.objects.filter(student=student,attendance__in=attendance_rec,attended=True).count()
        return total_present_days
    except Exception as e:
     print("Error in total_days_present util func")
     print(e)
     return 0

def calculate_attendance_percentage(student_id):
    try:
        total_present = total_days_present(student_id)
        total_absent = total_days_absent(student_id)
        total_days = total_present + total_absent
        if total_days == 0:
            return 0
        percentage = (total_present / total_days) * 100
        return round(percentage,2)
    except Exception as e:
        print("Error in calculate_attendance_percentage util func")
        print(e)
        return 0

def is_today_date_created(): # - >  use better naming convention ! 
    from data_class.models import Attendance
    year = Attendance.objects.filter(year=get_year(), month=get_month(), date=get_date()).exists()
    if year:
        print ("Date exists")
    else:
        year = Attendance.objects.create(year=get_year(), month=get_month(), date=get_date())
        print ("Date does not exist")

def is_attendance_taken(student_id):
    from data_class.models import Attendance
    try:
        attendance = Attendance.objects.get(year=get_year(),month=get_month(),date=get_date())
        is_taken = std.Student_Attendance.objects.filter(student=student_id,attendance=attendance).exists()
        return is_taken
    except Attendance.DoesNotExist:
        return False
    except Exception as e:
        print("Error in is_attendance_taken util func")
        print(e)
        return False

def get_calendar_data(year, month, student_id):
    """
    Generates calendar data for a specific student, year, and month.
    Returns a list of dictionaries representing days in the calendar.
    """
    try:
        from data_class.models import Attendance
        attendance_objs = Attendance.objects.filter(year=year, month=month).order_by('date')
        student_records = std.Student_Attendance.objects.filter(
            student=student_id, 
            attendance__in=attendance_objs
        ).select_related('attendance').order_by('attendance__date')
    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        attendance_objs = []
        student_records = []

    # Helper to map day name to index
    day_map = {
        "Sun": 0, "Sunday": 0,
        "Mon": 1, "Monday": 1,
        "Tue": 2, "Tuesday": 2,
        "Wed": 3, "Wednesday": 3,
        "Thu": 4, "Thursday": 4,
        "Fri": 5, "Friday": 5,
        "Sat": 6, "Saturday": 6
    }

    now = nepali_datetime.date.today()
    current_year = now.year
    current_month = now.month

    # 1. Determine Start Weekday of the Month
    start_weekday = 0
    if attendance_objs.exists():
        first_record = attendance_objs.first()
        try:
            rec_date = int(first_record.date)
            rec_day_idx = day_map.get(first_record.day, 0)
            start_weekday = (rec_day_idx - (rec_date - 1)) % 7
        except ValueError:
            # Fallback logic if date conversion fails
            pass 
    
    # Fallback if start_weekday is still 0 (and potentially incorrect) or no records
    if not attendance_objs.exists() or start_weekday == 0: 
         # Note: This fallback might need adjustment based on exact Nepali calendar logic
         # but serves as a reasonable default if DB data is missing/malformed.
         # For strict accuracy, one might need a full Nepali calendar library.
         pass


    # 2. Determine Range of Days to Show
    max_day = 32 # Default safe upper bound for Nepali months
    # If it's the current month, we might want to cap at today, 
    # but usually calendars show the whole month or up to recorded data.
    # The original code capped at `now.day` if it was the current month.
    
    # Check if it is the current month
    # month argument can be a name (str) or index (int/str)
    is_current_month = False
    current_month_name = now.strftime("%B")
    
    if str(year) == str(current_year):
        if str(month) == current_month_name:
            is_current_month = True
        elif str(month).isdigit() and int(month) == current_month:
            is_current_month = True

    if is_current_month:
         max_day = int(now.day)
    
    if attendance_objs.exists():
        try:
            last_rec_date = int(attendance_objs.last().date)
            if last_rec_date > max_day:
                max_day = last_rec_date
        except ValueError:
            pass

    # Map records
    records_by_date = {}
    for record in student_records:
        try:
            d = int(record.attendance.date)
            records_by_date[d] = record
        except ValueError:
            pass

    calendar_data = []
    
    # 3. Add Prefix Empty Slots
    for _ in range(start_weekday):
        calendar_data.append({
            'type': 'empty',
            'day': '',
            'status': '',
            'is_today': False
        })

    # 4. Generate Days
    for day_num in range(1, max_day + 1):
        record = records_by_date.get(day_num)
        day_str = f"{day_num:02d}"
        
        status = "no_record"
        if record:
            if record.attended:
                status = "present"
            else:
                status = "absent"
        
        is_today = (is_current_month and day_num == int(now.day))
        
        calendar_data.append({
            'type': 'day',
            'day': day_str,
            'status': status,
            'record': record,
            'is_today': is_today
        })
        
    return calendar_data