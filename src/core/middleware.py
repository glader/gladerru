from datetime import datetime


class UserReferer:
    def process_request(self, request):
        if request.META.get('HTTP_REFERER') and not request.user.is_authenticated() \
                and 'referer' not in request.session:
            request.session['referer'] = request.META['HTTP_REFERER']


class LastLogin:
    def process_request(self, request):
        if request.user.is_authenticated():
            user = request.user.get_profile()
            user.last_visit = datetime.now()
            user.save()
