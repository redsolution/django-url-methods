from django.conf.urls.defaults import *

urlpatterns = patterns('')

for view in ['response', 'notfound', 'error', 'redirect_response', 
    'redirect_notfound', 'redirect_redirect_response', 'redirect_cicle', 
    'permanent_redirect_response', 'http404', 'http500', 
    'request_true_response', 'request_false_response',]:
    urlpatterns += patterns('example.views', url('^%s$' % view, view, name=view))
