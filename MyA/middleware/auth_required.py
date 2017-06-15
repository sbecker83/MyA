from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import resolve

class AuthRequiredMiddleware(object):
    """ This middleware redirects all requests to the login page if a user is not logged in (all but those defined as
     public urls - login for obvious reasons)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_urls = ['login']

    def __call__(self, request):
        current_url =  resolve(request.path_info).url_name

        # redirect all requests which are non public if not logged in
        if not request.user.is_authenticated() and not current_url in self.public_urls:
            return HttpResponseRedirect(reverse('login'))

        response = self.get_response(request)
        return response