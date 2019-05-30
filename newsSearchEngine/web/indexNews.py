from whoosh.index import open_dir

class IndexNews:
    def __init__(self):
        ix = open_dir('../indexDir')
        self.ix = ix
        print('Index exist with schema : {}'.format(ix.schema))
        print('Number of document that indexed : {}'.format(ix.doc_count_all()))

    # return the number of document that exist
    def getDocumentCount(self):
        return self.ix.doc_count_all()
