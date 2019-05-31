from indexNews import IndexNews

indexNewsObject = IndexNews()
indexNewsObject.indexDocument()
print('document indexed : {}'.format(indexNewsObject.getDocumentCount()))