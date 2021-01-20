
from django.http import HttpResponse
from .models import Maintanence

under_maintanence = False

mid = Maintanence.objects.all()
for m in mid:
    if m.under_maintanence == True:
        under_maintanence = True
class ExecutionFlowMiddleWare(object):
    # pass
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print('This line is printed before view is called!')
        response = self.get_response(request)
        print('This line is printed with post processing of request')
        return response
        

class AppMaintenance(object):
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if under_maintanence == True and str(request.user) not in ['sai',]:

            return HttpResponse('<h1>Currently app under maintanence')
        else:
            print('This line is printed before view is called!')
            response = self.get_response(request)
            print('This line is printed with post processing of request')
            return response
        

class InternalServer(object):

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        return self.get_response(request)

    def process_exception(self,request,exception):
        s = '<h1>Internal server error</h1>' + str(exception.__class__.__name__)
        return HttpResponse(s)


