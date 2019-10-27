from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django import forms
from blobapp import models
from whatsmyblob import result_table
from whatsmyblob import util
from .forms import MapFileForm



@require_http_methods(["GET", "POST"])
def handle_req(request):
    """Main handler function that accepts POST and GET requests only"""

    #render website
    if request.method == "POST" and request.FILES:

        form = MapFileForm(request.POST, request.FILES)
        #create new JOB instance

        #send to fileSaver function

        upload_status = False
        error_message = "Uh oh. Something's wrong with your upload."


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

        return render(request, "blobapp/index.html",
                {"uploadStatus": upload_status, "errorMsg": error_message, "jobid": newJob.id, "show_form": False})
    else:
        form = MapFileForm()
        return render(request, 'blobapp/index.html', {
            'form': form, "show_form": True
            })


def submit():
    pass


def result(request, jobid):
    job = models.Job.objects.filter(id=jobid)[0]
    util.run_search(job)
    html = result_table.generate_html(
        jobid=jobid,
        title='Test title'
    )
    return HttpResponse(html)


def status():
    pass
