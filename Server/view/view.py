from django.http import HttpResponse
from django.shortcuts import render
from database import connection,model
import json
import datetime
import functools

def cmp(a , b):
    if a.date < b.date:
        return 1
    elif a.date == b.date:
        return 0
    else:
        return -1

def hello(request):
    context= {}
    maxDate = datetime.datetime.today()
    oneDay = datetime.timedelta(days = 1)
    minDate = maxDate - oneDay
    oneHour = datetime.timedelta(hours=1)
    if 'minDate' in request.GET:
        minDate =  datetime.datetime.strptime(request.GET['minDate'] , '%Y-%m-%d')

    if 'maxDate' in request.GET:
        maxDate = datetime.datetime.strptime(request.GET['maxDate'] , '%Y-%m-%d')

    minDate -= oneHour
    maxDate += oneHour

    #Read the json.
    db = connection.DB()
    result = db.select('SELECT * FROM link WHERE dat >= ? AND dat <= ?' , [minDate.strftime('%Y-%m-%d') , maxDate.strftime('%Y-%m-%d')])
    #Delete elements not in the range.
    elements = []
    for item in result:
        elements.append(model.Element(title=item[1] , url=item[2] , date=item[3]))
    elements.sort(key=functools.cmp_to_key(cmp))
    minDate += oneHour
    context['min'] = minDate.strftime('%Y-%m-%d')
    context['max'] = maxDate.strftime('%Y-%m-%d')
    context['item_list'] = elements
    context['len'] = len(elements)
    return render(request , 'hello.html', context)