from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django import forms
from blobapp import models
from .forms import MapFileForm



@require_http_methods(["GET", "POST"])
def handle_req(request):
    """Main handler function that accepts POST and GET requests only"""

    #render website
    if request.method == "POST" and request.FILES['input_file']:

        form = MapFileForm(request.POST, request.FILES)
        #create new JOB instance

        precheck = False
        #send to fileSaver function


        if form.is_valid() and precheck:
            form.save()
        
        #save
        return render(request, "blobapp/index.html", {"jobstatus": "Success"})
    else:
        form = MapFileForm()
        return render(request, 'blobapp/index.html', {
            'form': form
            })


def submit():
    pass


def result():
    pass


def status():
    pass
