from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import whoosh
from whoosh.qparser import QueryParser,OrGroup,MultifieldParser
from whoosh import scoring
from .indexNews import IndexNews
from django.core.paginator import Paginator
from whoosh import highlight

# Create your views here.

@csrf_protect
def search(request):
    indexNewsObject = IndexNews()
    ix = indexNewsObject.ix
    if request.method == 'POST':
        inputQuery = request.POST['inputQuerySearchPage']
        request.session['inputQuery'] = inputQuery
        if inputQuery == '':
            context = {
                'message' : 'لطفا عبارت مورد نظر خود را وارد کنید'
            }
            return render(request,'searchPage/searchPage.html',context=context)
        else:
            # queryParser = QueryParser(fieldname='content',schema=ix.schema,group=OrGroup)
            # queryParser = MultifieldParser(['title','content'],schema=ix.schema,group=OrGroup)
            queryParser = MultifieldParser(['title','content','summary'],schema=ix.schema)
            query = queryParser.parse(inputQuery)
            with ix.searcher(weighting=scoring.BM25F()) as searcher:
                results = searcher.search(query,terms=True,limit=None)
                
                #for customize html tag form highlight matched terms 
                htmlFormat = highlight.HtmlFormatter('b')
                results.formatter = htmlFormat
                results.fragmenter.maxchars = 300
                results.fragmenter.surround = 150
                paginator = Paginator(results,15)
                page = request.GET.get('page')
                resultWithPage = paginator.get_page(page)
                context = {
                'results':resultWithPage,
                'inputQuery':inputQuery
                }
                return render(request,'searchPage/searchPage.html',context=context)
    else:
        inputQuery = request.session['inputQuery']
        # queryParser = QueryParser(fieldname='content',schema=ix.schema,group=OrGroup)
        queryParser = MultifieldParser(['title','content','summary'],schema=ix.schema)
        query = queryParser.parse(inputQuery)
        with ix.searcher(weighting=scoring.BM25F()) as searcher:
            results = searcher.search(query,terms=True,limit=None)

            #for customize html tag form highlight matched terms 
            htmlFormat = highlight.HtmlFormatter('b')
            results.formatter = htmlFormat
            results.fragmenter.maxchars = 300
            results.fragmenter.surround = 150
            paginator = Paginator(results,15)
            page = request.GET.get('page')
            resultWithPage = paginator.get_page(page)
            context = {
            'results':resultWithPage,
            'inputQuery':inputQuery
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