from django.http import *
from django.core.urlresolvers import reverse

def response(request):
    return HttpResponse('Done')

def notfound(request):
    return HttpResponseNotFound('Not found')

def error(request):
    return HttpResponseServerError('Error')

def redirect_response(request):
    return HttpResponseRedirect(reverse('response'))
    
def redirect_notfound(request):
    return HttpResponseRedirect(reverse('notfound'))

def redirect_redirect_response(request):
    return HttpResponseRedirect(reverse('redirect_response'))

def redirect_cicle(request):
    return HttpResponseRedirect(reverse('redirect_cicle'))

def permanent_redirect_response(request):
    return HttpResponsePermanentRedirect(reverse('response'))
    
def http404(request):
    raise Http404

def http500(request):
    raise Exception

def request_true_response(request):
    from urlmethods import local_check
    result = local_check(reverse('response'))
    if result:
        return HttpResponse('True')
    else:
        return HttpResponse('False')

def request_false_response(request):
    from urlmethods import local_check
    result = local_check(reverse('notfound'))
    if result:
        return HttpResponse('True')
    else:
        return HttpResponse('False')

