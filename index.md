<div dir='rtl'>

### آماده سازی داکیومنت برای index

داکیومنت های index شده توسط framework whoosh یک schema لازم دارند تا ساختار هر داکیومنت را درک کنند.<br>
هر فیلد در این shcema دو حالت دارد یا می تواند index شود یعنی توانایی search روی آن فیلدها فراهم می شود یا می تواند store شود که همان نتایجی است که هنگام search برگردانده می شود و ما توانایی نمایش آن را برای کاربر داریم. <br>
با دستورات زیر یک کلاس schema میسازیم که بیان کننده ساختار هر داکیومنت در موتور جسنجوی ما خواهد بود. <br>

<div dir='ltr'>

```python

from whoosh.fields import SchemaClass,TEXT,DATETIME,ID

# the structure of document in search engine
class NewsSchema(SchemaClass): 
	newsAgency = TEXT
	# the title of news that save with indexed and return as result to user
	title = TEXT(stored=True)
	# the summary of news that save with indexed document and return as result to user
	summary = TEXT(stored=True) 
	# the url of news that save with indexed document and return as result to user
	url = ID(stored=True)
	content = TEXT

```

</div>

داده های ما که بصورت فایل json و بصورت دستی index می شود نیاز به یک تابع دارد تا تمام داده های در یک فایل json تجمیع گردنند. این تابع تمامی فایل های json در شاخه ای که وجود دارد را در یک ساختار json ذخیره و آنها را بر میگردانند.

<div dir='ltr'>

```python

import json
import glob

class NewsData:
    # return the data of all .json file in one variable
    def getData(self): 
        result = []
        for f in glob.glob('*.json'):
            with open(f) as jsonFile:
                result = result + json.load(jsonFile)
        return result

```

</div>

هر ساختار index در این framework به یک پوشه نیاز دارد که به ما توانایی ایجاد index های مختلف با schema های مختلف را می دهد.<br>
در این قطعه کد در صورتی که فایل index از قبل وجود داشته باشد آن را بر میگرداند و از آن در طول برنامه استفاده می کند، اگر وجود نداشته باشد یک فایل ساخته و از آن استفاده می کند.<br>
شما می توانید به کمک آرگومان indexname در توابع open_dir و create_in وجه تمایزی میان index ها قائل شوید و این توانایی را به شما می دهد تا index های مختلف در این پوشه را طراحی و از آنها استفاده کنید.<br>

<div dir='ltr'>

```python

class IndexNews:
def __init__(self):
	#object of news data for use getdata method for get data from json files
	newsFile = NewsData()
	#put data in self to use in all class method that give self as argument
	self.data = newsFile.getData()
	#the schema object for create index
	schema = NewsSchema()
	#check if the directort dose not exist create it
	if not os.path.exists('../indexDir'):
		os.mkdir('../indexDir')
	if exists_in('../indexDir'):
		#open directory and put in ix variable this variable use for all parts of index documant in this framework and you can use indexname argument to open that index you want
		ix = open_dir('../indexDir')
		#put ix in self to use in all class method that give self as argument
		self.ix = ix
		print('Index exist with schema : {}'.format(ix.schema))
		print('Number of document that indexed : {}'.format(ix.doc_count_all()))
	else:
		#create an index in indexDir with schema that we have in __init__
		ix = create_in('../indexDir', schema)
		print('Index create with schema : {}'.format(ix.schema))
		#doc_count_all is a method of  use for get the number of document that indexed
		print('Number of document that indexed : {}'.format(ix.doc_count_all()))
		self.ix = ix

```

</div>

برای index کردن doeument ها طبق قطعه کد زیر پیش میرویم که تمام اطلاعات موجود در self.data که اخبار ما را شامل می شد را با کمک متغیر writer که یک object از کلاس writer است و به کمک تابع add_docment آن اخبار را  index می کنیم و در آخر با دستور writer.commit این متغیر را می بندیم و در صورت استفاده دوباره باید متغیر جدید را بسازیم.<br>
و یک تابع برای استفاده از تعداد document های index شده در این کلاس قرار می دهیم.<br>


<div dir='ltr'>

```python
import os.path
from whoosh.index import create_in, open_dir,exists_in
from schemaClass import NewsSchema
from newsClass import NewsData


class IndexNews:
	def __init__(self):
		#object of news data for use getdata method for get data from json files
		newsFile = NewsData()
		#put data in self to use in all class method that give self as argument
		self.data = newsFile.getData()
		#the schema object for create index
		schema = NewsSchema()
		#check if the directort dose not exist create it
		if not os.path.exists('../indexDir'):
			os.mkdir('../indexDir')
		if exists_in('../indexDir'):
			#open directory and put in ix variable this variable use for all parts of index documant in this framework and you can use indexname argument to open that index you want
			ix = open_dir('../indexDir')
			#put ix in self to use in all class method that give self as argument
			self.ix = ix
			print('Index exist with schema : {}'.format(ix.schema))
			print('Number of document that indexed : {}'.format(ix.doc_count_all()))
		else:
			#create an index in indexDir with schema that we have in __init__
			ix = create_in('../indexDir', schema)
			print('Index create with schema : {}'.format(ix.schema))
			#doc_count_all is a method of  use for get the number of document that indexed
			print('Number of document that indexed : {}'.format(ix.doc_count_all()))
			self.ix = ix

	def indexDocument(self):
		#writer object for index document
		writer = self.ix.writer()
		for item in self.data:
		  writer.add_document(newsAgency= item['newsagency'],
				  title= item['title'],
				  summary = item['summary'],
				  content= item['content'],
				  url = item['url'])
		#exit the process of index document 
		writer.commit()
		return True

	# return the number of document that indexed
	def getDocumentCount(self):
		return self.ix.doc_count_all()

```

</div>

در آخرین مرحله از index کردن document ها object  این کلاس را در یک فایل جداگانه قرار داده و با استفاده از تابع indexDocument تمامی اطلاعات را index می کنیم.<br>

<div dir='ltr'>

```python

from indexNews import IndexNews

indexNewsObject = IndexNews()
indexNewsObject.indexDocument()
print('document indexed : {}'.format(indexNewsObject.getDocumentCount()))

```

</div>







