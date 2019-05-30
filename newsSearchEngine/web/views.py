from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import whoosh
from whoosh.qparser import QueryParser,OrGroup
from .indexNews import IndexNews

# Create your views here.

@csrf_protect
def index(request):
    indexNewsObject = IndexNews()
    indexCount = indexNewsObject.getDocumentCount()
    if request.method == 'POST':
        inputQuery = request.POST['inputQuery']
        if inputQuery == '':
            context = {
                'message' : 'لطفا عبارت مورد نظر خود را وارد کنید'
            }
            return render(request,'mainPage/index.html',context=context)
        else:
            ix = indexNewsObject.ix
            queryParser = QueryParser(fieldname='content',schema=ix.schema,group=OrGroup)
            query = queryParser.parse(inputQuery)
            with ix.searcher() as searcher:
                results = searcher.search(query,terms=True)
                context = {
                'indexCount' : indexCount,
                'results':results
                }
                return render(request,'mainPage/index.html',context=context)
    else:
        context = {
            'indexCount' : indexCount
        }
        return render(request,'mainPage/index.html',context=context)