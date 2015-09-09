from django.shortcuts import render,render_to_response
from django.template import Context, RequestContext

from home import strings as home_string

# Create your views here.
def main(request):
    variables = RequestContext(request, {
        'home_string' : home_string,
    })
    return render_to_response('home/index.html', variables)