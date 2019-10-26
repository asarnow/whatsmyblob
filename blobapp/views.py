from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
#from utils.py import fileSaver



@require_http_methods(["GET", "POST"])
def handle_req(request):
    """Main handler function that accepts POST and GET requests only"""

    if request.method == "GET":
        #proceed with get request rendering
        return render(request, 'templates/index.html')
    if request.method == "POST":
        print("hi")
        #read formdata and make fileUpload object
        #send to fileSaver function
        return render(request, "templates/index.html", {"jobstatus": "Success"})
    else:
        return HttpResponseNotFound('<h1>The resource you requested was not available at this time.</h1>')


def submit():
    pass


def result():
    pass


def status():
    pass
