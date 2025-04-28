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
            'max_1':'1:40',
            'max_2':'1:45'
        },
        '2':{
            'min_1':'1:45',
            'min_2':'1:50',
            'max_1':'2:40',
            'max_2':'2:45'
        },
        '3':{
            'min_1':'3:00',
            'min_2':'3:05',
            'max_1':'3:55',
            'max_2':'4:00'
        },
        '4':{
            'min_1':'4:00',
            'min_2':'4:05',
            'max_1':'4:55',
            'max_2':'5:00'
        }
        
    }
}

from django.utils import timezone

def dateValues(group):
    section = GroupsPSRSections.objects.filter(group_pk=str(group.pk),create_at=timezone.now().date())
    type='AM'
    if  group.type:
        type = 'PM'
    if len(section) == 1:
        return hours[type]['1'] 
    elif len(section) == 2:
        return hours[type]['2'] 
    elif len(section) == 3:
        return hours[type]['3'] 
    else:
        return hours[type]['4'] 