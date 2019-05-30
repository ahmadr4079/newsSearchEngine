from whoosh.index import open_dir

class IndexNews:
    def __init__(self):
        ix = open_dir('../indexDir')
        self.ix = ix

    # return the number of document that exist
    def getDocumentCount(self):
        return self.ix.doc_count_all()
