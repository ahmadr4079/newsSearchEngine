from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import whoosh
from .indexNews import IndexNews

# Create your views here.

@csrf_protect
def index(request):
    indexNewsObject = IndexNews()
    indexCount = indexNewsObject.getDocumentCount()
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
        context = {
            'indexCount' : indexCount
        }
        return render(request,'mainPage/index.html',context=context)