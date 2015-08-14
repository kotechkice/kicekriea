from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from stdnt import strings as stdnt_string
from home import strings as home_string


# Create your views here.
def login(request):
    variables = RequestContext(request, {
        'home_string' : home_string,
    })
    return render_to_response('tch/login.html', variables)