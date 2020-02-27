from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics

from rest_framework.views import APIView
from .serializer import TaskSerializer
from .models import tasks
from .taskScheduler import *
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = tasks.objects.all().order_by('coid')
    serializer_class = TaskSerializer

class TaskAPIView(APIView):
    def get_object(self, pk):
        print(pk)
        try:
            return tasks.objects.get(pk=pk)
        except:
            print(pk, status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            scheduleJob(request)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.is_valid())
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #52.168.183.147

    def put(self, request, pk=None, format=None):
        pk = request.data['coid']
        print("here")
        print(request)
        user = self.get_object(pk)
        serializer = TaskSerializer(user, data=request.data)
        if serializer.is_valid():
            updateJob(request)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.is_valid())
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def sched_list(request):
 schedules = []
 scl = scheduler.get_jobs()
#  xt = repr(scl[0].trigger)
#  jt = scl[0].trigger
#  print("XXXXXXXXXXXXXX",jt.start_date)
 for job in scl:
     jobdict = {}
    #  jt = type(job.trigger)
     print("job",job.name)
     jobdict['job_name'] = job.name
    #  jobdict['job_trigger'] = jt
     jobdict['next run'] = job.next_run_time    
     jobdict['coid'] = job.args
    #  jobdict['job'] = job
    #  for f in job.trigger.fields:
    #      curval = str(f)
    #      jobdict[f.name] = curval

     schedules.append(jobdict)
 return Response(schedules)

@api_view(['POST'])
def sched_state(request):
    
        r_state = request.data['status']
        print(r_state,"wwwwwwwww")
        scheduler_state = scheduler.state
        print(scheduler_state)
        if r_state == 'start':
            if scheduler_state != 1:
                scheduler.start()
                print("Scheduler Started")
                return Response("STARTED", status=status.HTTP_200_OK)
            else:
                print("Scheduler already running")
                return Response("Scheduler already running")
        elif r_state == 'stop':
            if scheduler_state != 0:
                scheduler.shutdown()
                print("Scheduler Stopped")
                return Response("STOPPED", status=status.HTTP_200_OK)
            else:
                print("Scheduler not running")
                return Response("Scheduler not running")
        elif r_state == 'state':
            if scheduler_state == 1:
                print("Scheduler Running")
                return Response(1, status=status.HTTP_200_OK)
            else:
                return Response(0, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def sched_remove(request):
    r_jobid = int(request.data['coid'])
    pk = request.data['coid']
    try:
        user = tasks.objects.get(pk=pk)
    except:
        print('Job not found', status.HTTP_400_BAD_REQUEST)
    serializer = TaskSerializer(user, data=request.data)
    if serializer.is_valid():
        d = scheduler.remove_job(r_jobid)
        return Response("Job Deleted", status=status.HTTP_200_OK)
    else:
        return Response("Job not found", status=status.HTTP_400_BAD_REQUEST)