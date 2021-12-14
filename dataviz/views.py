from django.http import HttpResponse
from .models import Building, Meter, HalfHourly
import csv, io
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.dateparse import parse_datetime
import dateutil.parser

from django.views.generic import View
   
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum
from django.http import JsonResponse
# Create your views here.


def consumation_chart(request):
    labels = []
    data = []

    queryset = HalfHourly.objects.values('meter__building__name').annotate(meter_consumption=Sum('consumption')).order_by('-meter_consumption')
    for entry in queryset:
        labels.append(entry['meter__building__name'])
        data.append(entry['meter_consumption'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dataviz/home.html')


def pie_chart(request):
    labels = []
    data = []
    queryset = HalfHourly.objects.order_by('-consumption')[:10]
    for obj in queryset:
        labels.append(obj.meter.building.name)
        data.append(obj.consumption)

    return render(request, 'dataviz/pie_chart.html', {
        'labels': labels,
        'data': data,
    })


def building_upload(request):
    # declaring template
    template = "dataviz/building_upload.html"
    data = {
        'objects': Building.objects.all()

    }
    if request.method == "GET":
        return render(request, template, data)
    try:     # if not GET, then proceed
        csv_file = request.FILES["file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("building_upload"))
    
        # if csv_file.multiple_chunks(): #if file is too large, return
        #     messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponseRedirect(reverse("halfhourly_upload"))

        file_data = csv_file.read().decode("utf-8-sig")	
        lines = file_data.split("\n")
        # next(lines)
        #loop over the lines and save them in db. If error , store as string and then display
        objects = []
        for line in lines: #range(len(lines)): #						
            fields = line.split(",")

            created = Building.objects.update_or_create(
                id=fields[0],
                name=fields[1]
            )
            # created = Building(
            #     id=fields[0],
            #     name=fields[1],
            # )
            objects.append(created)
            if len(objects) > 5000:
                Building.objects.bulk_create(objects)
                print("Entered 5000 entries") 
                objects = []

        if objects:
            Building.objects.bulk_create(objects)
            objects = []

    except Exception as e:
        # logging.getLogger("error_logger").error(repr(e))					
        print(e)
        pass
    context = {
        'objects': HalfHourly.objects.all()
    }
    return render(request, template, context)






def meter_upload(request):
    # declaring template
    template = "dataviz/meter_upload.html"
    data = {}

    if request.method == "GET":
        return render(request, template, data)
    try:     # if not GET, then proceed
        csv_file = request.FILES["file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("meter_upload"))
    
        if csv_file.multiple_chunks(): #if file is too large, return
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("meter_upload"))

        file_data = csv_file.read().decode("utf-8")	
        lines = file_data.split("\n")
        # next(lines)
        #loop over the lines and save them in db. If error , store as string and then display
        print("Success")
        for line in lines:						
            fields = line.split(",")
            # data_dict = {}
            # data_dict["building_id"] = fields[0]
            # data_dict["id"] = fields[1]
            # data_dict["fuel"] = fields[2]
            # data_dict["unit"] = fields[3]

            created = Meter.objects.update_or_create(
                id=int(fields[1]),
                building_id=fields[0],
                fuel=fields[2],
                unit=fields[3]
            )
            # Meter.objects.update_or_create(
            #     id=(data_dict["id"]),
            #     building_id=data_dict["building_id"],
            #     fuel=(data_dict["fuel"]),
            #     unit=(data_dict["unit"])
            # )
    except Exception as e:
        print(e)
        pass
    context = {
        'objects': Meter.objects.all()
    }
    return render(request, template, context)



def halfhourly_upload(request):
    # declaring template
    template = "dataviz/halfhourly_upload.html"
    data = {}

    if request.method == "GET":
        return render(request, template, data)
    try:     # if not GET, then proceed
        csv_file = request.FILES["file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("halfhourly_upload"))
    
        # if csv_file.multiple_chunks(): #if file is too large, return
        #     messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponseRedirect(reverse("halfhourly_upload"))

        file_data = csv_file.read().decode("utf-8-sig")	
        lines = file_data.split("\n")
        # next(lines)
        #loop over the lines and save them in db. If error , store as string and then display
        objects = []
        for line in lines: #range(len(lines)): #						
            fields = line.split(",")

            # created = HalfHourly.objects.update_or_create(
            #     consumption=fields[0],
            #     meter_id=fields[1],
            #     reading_date_time=fields[2],
            # )
            created = HalfHourly(
                consumption=fields[0],
                meter_id=fields[1],
                reading_date_time=dateutil.parser.parse(fields[2]),
            )
            objects.append(created)
            if len(objects) > 5000:
                HalfHourly.objects.bulk_create(objects)
                print("Entered 5000 entries") 
                objects = []

        if objects:
            HalfHourly.objects.bulk_create(objects)
            objects = []

    except Exception as e:
        # logging.getLogger("error_logger").error(repr(e))					
        print(e)
        pass
    context = {
        # 'objects': HalfHourly.objects.all()
    }
    return render(request, template, context)
