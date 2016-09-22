from django.conf.urls import patterns, url
from visitorManagement.mapi.views import LoginView, RegistrationView, VisitorView, WorkBookView, WorkBookTypeView, \
    SearchView, SearchTermView

'''
urlpatterns = patterns('',
                       # Version 1.0.0 of the mobile API

                       (r'^v1.0.0/login/?$', LoginView.as_view()),
                       (r'^v1.0.0/get-workbook/?$', WorkBookView.as_view()),

                       #(r'^v1.0.0/register/?$', RegistrationView.as_view()),
                       (r'^v1.0.0/create-workbook/?$', WorkBookView.as_view()),

                       (r'^v1.0.0/create-visitor/?$', VisitorView.as_view()),
                       (r'^v1.0.0/get-visitors/?$', VisitorView.as_view()),
                       )
'''

urlpatterns = [
    # Version 1.0.0 of the mobile API
    url(r'^v1.0.0/login/?$', LoginView.as_view()),
    url(r'^v1.0.0/get-workbook/?$', WorkBookView.as_view()),
    url(r'^v1.0.0/get-workbook-type/?$', WorkBookTypeView.as_view()),
    url(r'^v1.0.0/create-workbook/?$', WorkBookView.as_view()),

    # (r'^v1.0.0/register/?$', RegistrationView.as_view()),

    url(r'^v1.0.0/create-visitor/?$', VisitorView.as_view()),
    url(r'^v1.0.0/get-visitors/?$', VisitorView.as_view()),

    url(r'^v1.0.0/search-tc/?$', SearchTermView.as_view()),

    url(r'^v1.0.0/search/?$', SearchView.as_view()),
]
