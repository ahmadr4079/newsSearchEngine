 <div dir='rtl'>

تابع زیر که به search/ متصل است با هر GET request یک object از کلاس که دایرکتوری index ساخته شده را open می کند.<b>

<div dir='ltr'>

```python

@csrf_protect
def search(request):
    #object of indexNews class for open index direcotory
    indexNewsObject = IndexNews()
    #object of open_dir index direcotory in indexNews class
    ix = indexNewsObject.ix
    if request.method == 'POST':
	#get the user query
        inputQuery = request.POST['inputQuerySearchPage']
	#added query to request session
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

```

</div>
