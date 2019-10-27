import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django import forms
from blobapp import models
from whatsmyblob import result_table
from whatsmyblob import util
from .forms import MapFileForm


def handle_req(request):
    form = MapFileForm()
    return render(request, 'blobapp/index.html', {
        'form': form, "show_form": True
        })


def submit(request):
    form = MapFileForm(request.POST, request.FILES)
    upload_status = False
    error_message = ""
    if form.is_valid():
        mapFileInstance = form.save()
        newJob = models.Job(query_map_file=mapFileInstance)
        newJob.save()
        # precheck = util.handle_upload_mrc(newJob, mapFileInstance)
        precheck = True
        if precheck:
            upload_status = True
        else:
            error_message = "We had trouble validating your .mrc file. Check its integrity and try again."
    else:
        return "Another error"
    timing = util.run_search(newJob)
    ajaxResp = json.dumps({'timing': timing,
                           'status': {"uploadStatus": upload_status,
                                      "errorMsg": error_message,
                                      "jobid": newJob.id}})
    return HttpResponse(ajaxResp, content_type="application/json")


def result(request, jobid):
    job = models.Job.objects.filter(id=jobid)[0]
    html = result_table.generate_html(jobid=jobid, title=job.name)
    return HttpResponse(html)


def status(request, jobid):
    pass
