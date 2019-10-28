import json
import os.path
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
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


# def result(request, jobid):
#     job = models.Job.objects.filter(id=jobid)[0]
#     html = result_table.generate_html(jobid=jobid, title=job.query_map_file.name)
#     return HttpResponse(html)


def result(request, jobid):
    job = models.Job.objects.filter(id=jobid)[0]
    html = result_table.generate_html(
        jobid=jobid,
        title='Test title'
    )
    divs = [d for d in html[1]]
    df_results = result_table.make_dataframe(jobid=jobid)
    jobdir = os.path.join(settings.TEMP_ROOT, str(jobid))
    pdb_target = df_results.CATH_domain[0][:4]
    pdbFileName = "get_job_pdb/" + str(jobid) + "/" + pdb_target + "_fit.pdb"
    densityPath = "get_map/" + str(jobid)
    return render(request, 'blobapp/results.html',
                  {"scripts": html[0], "divs": html[1],
                   "densityMap": densityPath,
                   "pdb": pdbFileName})


def status(request, jobid):
    pass


def get_job_pdb(request, jobid, pdb):
    jobdir = os.path.join(settings.TEMP_ROOT, str(jobid))
    with open(os.path.join(jobdir, pdb)) as f:
        pdb_str = f.read()
    return pdb_str


def get_map(request, jobid):
    job = models.Job.objects.filter(id=jobid)[0]
    map_file = job.query_map_file.path
    with open(map_file) as f:
        map_bytes = f.read()
    return map_bytes
