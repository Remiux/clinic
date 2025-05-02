from apps.symptom.models import GroupsPSRSections

hours={
    'AM':{
        '1':{
            'min_1':'8:00',
            'min_2':'8:05',
            'max_1':'8:55',
            'max_2':'9:00'
        },
        '2':{
            'min_1':'9:00',
            'min_2':'9:05',
            'max_1':'9:55',
            'max_2':'10:00'
        },
        '3':{
            'min_1':'10:30',
            'min_2':'10:35',
            'max_1':'11:25',
            'max_2':'11:30'
        },
        '4':{
            'min_1':'11:30',
            'min_2':'11:35',
            'max_1':'12:25',
            'max_2':'12:30'
        }
        
    },
    'PM':{
        '1':{
            'min_1':'12:45',
            'min_2':'12:50',
            'max_1':'13:40',
            'max_2':'13:45'
        },
        '2':{
            'min_1':'13:45',
            'min_2':'13:50',
            'max_1':'14:40',
            'max_2':'14:45'
        },
        '3':{
            'min_1':'15:00',
            'min_2':'15:05',
            'max_1':'15:55',
            'max_2':'16:00'
        },
        '4':{
            'min_1':'16:00',
            'min_2':'16:05',
            'max_1':'16:55',
            'max_2':'17:00'
        }
        
    }
}

from django.utils import timezone

def dateValues(group):
    section = GroupsPSRSections.objects.filter(group_pk=str(group.pk),create_at=timezone.now().date())
    type='AM'
    if not group.type:
        type = 'PM'
    if len(section) == 1:
        return hours[type]['1'] 
    elif len(section) == 2:
        return hours[type]['2'] 
    elif len(section) == 3:
        return hours[type]['3'] 
    else:
        return hours[type]['4'] 
    
def individual_therapy_dateValues(individual_therapy):
    current_time = timezone.now().time()
    hour = current_time.hour
    minute = current_time.minute
    type='AM'
    am_pm = current_time.strftime("%p")
    if am_pm == "AM":
        if 8 <= hour < 9:
            return hours[type]['1'] 
        elif 9 <= hour < 10:
            return hours[type]['2'] 
        elif hour == 10 or (hour == 11 and minute < 30):
            return hours[type]['3'] 
        elif (hour == 11 and minute >= 30) or (hour == 12 and minute <= 30):
            return hours[type]['4'] 
        else:
            return hours[type]['1'] 
    else:
        type='PM'
        if  (hour == 12 and minute >= 45) or (hour == 1 and minute <= 45):
            return hours[type]['1'] 
        elif  (hour == 1 and minute >= 45) or (hour == 2 and minute <= 45):
            return hours[type]['2'] 
        elif 3 <= hour < 4:
            return hours[type]['3'] 
        elif 4 <= hour < 5:
            return hours[type]['4'] 
        else:
            return hours[type]['1'] 