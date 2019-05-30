from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

# Create your views here.

@csrf_protect
def index(request):
    if request.method == 'POST':
        query = request.POST['inputQuery']
        if query == '':
            context = {
                'message' : 'لطفا عبارت مورد نظر خود را وارد کنید'
            }
            return render(request,'mainPage/index.html',context=context)
        else:
            return render(request,'mainPage/index.html')
    else:
        return render(request,'mainPage/index.html')
