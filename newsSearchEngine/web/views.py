from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import whoosh
from whoosh.qparser import QueryParser,OrGroup,MultifieldParser
from .indexNews import IndexNews

# Create your views here.

@csrf_protect
def search(request):
    print('you are in search function')
    indexNewsObject = IndexNews()
    ix = indexNewsObject.ix
    if request.method == 'POST':
        print('request is post')
        inputQuery = request.POST['inputQuerySearchPage']
        if inputQuery == '':
            context = {
                'message' : 'لطفا عبارت مورد نظر خود را وارد کنید'
            }
            return render(request,'searchPage/searchPage.html',context=context)
        else:
            # queryParser = QueryParser(fieldname='content',schema=ix.schema,group=OrGroup)
            queryParser = MultifieldParser(['title','content'],schema=ix.schema,group=OrGroup)
            query = queryParser.parse(inputQuery)
            with ix.searcher() as searcher:
                results = searcher.search(query,terms=True)
                context = {
                'results':results
                }
                return render(request,'searchPage/searchPage.html',context=context)
    else:
        inputQuery = request.session['inputQuery']
        inputQuery = inputQuery
        # queryParser = QueryParser(fieldname='content',schema=ix.schema,group=OrGroup)
        queryParser = MultifieldParser(['title','content'],schema=ix.schema,group=OrGroup)
        query = queryParser.parse(inputQuery)
        with ix.searcher() as searcher:
            results = searcher.search(query,terms=True)
            context = {
            'results':results
            }
            return render(request,'searchPage/searchPage.html',context=context)


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
            request.session['inputQuery'] = inputQuery
            return redirect(search)
    else:
        context = {
            'indexCount' : indexCount
        }
    return render(request,'mainPage/index.html',context=context)