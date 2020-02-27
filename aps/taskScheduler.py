from .scheduler import scheduler
from datetime import  datetime
from rest_framework.response import Response
from rest_framework import status

# DATEFORMAT - "2009-11-06 16:30:05"
# sessionTimeout, API Versioning header based,
''' curl -d '{
     "coid":"3",
     "starttime":"26-02-2020 19:40:11",
     "command":"get-ip",
     "jobtype":"interval",
     "intv_seconds":"20"
 }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/'''

# curl -d '{
#      "coid" : "469",
#      "starttime" : "2020-02-24 13:20:10",
#      "command" : "commandID",
#      "jobtype" :
#     }'

''' curl -d '{
   "coid":"3",
     "starttime":"29-02-2020 19:40:11",
     "command":"netstat",
     "jobtype":"interval",
     "intv_seconds":"40"
 }' -H "Content-Type: application/json" -X PUT http://localhost:8001/schedule/'''


# '{
#     "coid":"320",
#     "startime":"09-02-2019 19:40:11",
#     "command":"get-ip",
#     "jobtype":"interval",
#     "interval": "{
#                 "seconds":"10",
#                 "hours":"22"
#                 }"
# }'
# curl -d '{"job_id":"210"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/remove/
# curl -d '{"status":"state"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status/
# curl -d '{"status":"start"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status/
# curl  -H "Content-Type: application/json" -X GET localhost:8000/schedule/tasks/



def sendRequest(coid):
    # headers = {'Content-Type': 'application/json'}
    # data = {
    #     "correlationID" : coid,
    # }
    # url = 'localhost:8000/' 
    print(coid,"sendRequest()")


def sendRequest2(coid):
    # headers = {'Content-Type': 'application/json'}
    # data = {
    #     "correlationID" : coid,
    # }
    # url = 'localhost:8000/' 
    print(coid,"sendRequest2()")


def dateformatter(cur_date):
    date_time = {
    "day": "",
    "date": "",
    "month": "",
    "year": "",
    "hour": "",
    "minutes": "",
    "seconds": ""
    }
    dt_obj = datetime.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
    date_time["date"] = dt_obj.strftime('%d')
    date_time["month"] = dt_obj.strftime('%m')
    date_time["year"] = dt_obj.strftime('%Y')
    date_time["hour"] = dt_obj.strftime('%H')
    date_time["minutes"] = dt_obj.strftime('%M')
    date_time["seconds"] = dt_obj.strftime('%S')


def scheduleJob(data):
    print("=========",data.data)
    r_data = data.data
    coid = r_data['coid'] if "coid" in r_data else 0
    starttime = r_data['starttime'] if "starttime" in r_data else None
    endtime = r_data['endtime'] if "endtime" in r_data else None
    cmd = r_data['command'] if "command" in r_data else None
    jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    
    ## INTERVAL JOB VARIABLES 
    intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
    intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
    intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
    intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0

    
    ## CRONJOB VARIABLES
    job_month = r_data['job_month'] if "job_month" in r_data else None
    job_day = r_data['job_day'] if "job_day" in r_data else None
    job_week = r_data['job_week'] if "job_week" in r_data else None
    job_year = r_data['job_year'] if "job_year" in r_data else None
    job_dow = r_data['job_dow'] if "job_dow" in r_data else None
    job_sec = int(r_data['job_seconds']) if "job_seconds" in r_data else None
    job_min = int(r_data['job_minutes']) if "job_minutes" in r_data else None
    job_hrs = int(r_data['job_hours'])if "job_hours" in r_data else None
    enddate = r_data['enddate'] if "enddate" in r_data else None


    # start date
    if jobtype == 'date':
        if starttime != 'None':
            job = scheduler.add_job(sendRequest, trigger='date', run_date=starttime,args=[coid], id=str(coid))
            return Response("Date job scheduled!", status=status.HTTP_201_CREATED)
        elif starttime == 'None':
            return Response("Date field can't be empty for date jobs", status=status.HTTP_400_BAD_REQUEST)

    elif jobtype == 'interval':
        # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
        
        job = scheduler.add_job(sendRequest, trigger='interval',
                            seconds=intv_sec,
                            minutes=intv_min,
                            hours = intv_hrs,
                            weeks = intv_weeks,
                            id=str(coid), args=[coid],
                            replace_existing=True)
        
        return Response("Interval job scheduled!", status=status.HTTP_201_CREATED)
        # return "job details: %s" % job
    elif jobtype == 'cron':
        # hour,min,sec -> int // year,month,day,week,dayofweek
        
        job = scheduler.add_job(sendRequest, trigger='cron',
                            year=job_year,
                            month=job_month, 
                            day=job_day, 
                            week=job_week,
                            day_of_week=job_dow,
                            hour=job_hrs,
                            minute=job_min,
                            second=job_sec,
                            start_date=starttime,
                            end_date=enddate,
                            id=str(coid), args=[coid],
                            replace_existing=True)
        return Response("Cron job scheduled!", status=status.HTTP_201_CREATED)


def updateJob(data):
    print("=========",data.data)
    r_data = data.data
    coid = r_data['coid'] if "coid" in r_data else 0
    starttime = r_data['starttime'] if "starttime" in r_data else None
    endtime = r_data['endtime'] if "endtime" in r_data else None
    cmd = r_data['command'] if "command" in r_data else None
    jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    
    ## INTERVAL JOB VARIABLES 
    intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
    intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
    intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
    intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0

    
    ## CRONJOB VARIABLES
    job_month = r_data['job_month'] if "job_month" in r_data else None
    job_day = r_data['job_day'] if "job_day" in r_data else None
    job_week = r_data['job_week'] if "job_week" in r_data else None
    job_year = r_data['job_year'] if "job_year" in r_data else None
    job_dow = r_data['job_dow'] if "job_dow" in r_data else None
    job_sec = int(r_data['job_seconds']) if "job_seconds" in r_data else None
    job_min = int(r_data['job_minutes']) if "job_minutes" in r_data else None
    job_hrs = int(r_data['job_hours'])if "job_hours" in r_data else None
    enddate = r_data['enddate'] if "enddate" in r_data else None


    # start date
    if jobtype == 'date':
        if starttime != 'None':
            job = scheduler.reschedule_job(job_id=str(coid),run_date=starttime)
            return Response("Date job updated!", status=status.HTTP_201_CREATED)
        elif starttime == 'None':
            return Response("Date field can't be empty for date jobs", status=status.HTTP_400_BAD_REQUEST)

    elif jobtype == 'interval':
        # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
        
        job = scheduler.reschedule_job(trigger='interval',
                            seconds=intv_sec,
                            minutes=intv_min,
                            hours = intv_hrs,
                            weeks = intv_weeks,
                            job_id=str(coid))
        
        return Response("Interval job updated!", status=status.HTTP_201_CREATED)
        # return "job details: %s" % job
    elif jobtype == 'cron':
        # hour,min,sec -> int // year,month,day,week,dayofweek
        
        job = scheduler.reschedule_job(trigger='cron',
                            year=job_year,
                            month=job_month, 
                            day=job_day, 
                            week=job_week,
                            day_of_week=job_dow,
                            hour=job_hrs,
                            minute=job_min,
                            second=job_sec,
                            start_date=starttime,
                            end_date=enddate,
                            job_id=str(coid))
        return Response("Cron job updated!", status=status.HTTP_201_CREATED)

   