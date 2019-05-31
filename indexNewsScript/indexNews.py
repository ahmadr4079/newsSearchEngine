import os.path
from whoosh.index import create_in, open_dir,exists_in
from schemaClass import NewsSchema
from newsClass import NewsData


class IndexNews:
    def __init__(self):
        newsFile = NewsData()
        self.data = newsFile.getData()
        schema = NewsSchema()
        if not os.path.exists('../indexDir'):
            os.mkdir('../indexDir')
        if exists_in('../indexDir'):
            ix = open_dir('../indexDir')
            self.ix = ix
            print('Index exist with schema : {}'.format(ix.schema))
            print('Number of document that indexed : {}'.format(ix.doc_count_all()))
        else:
            ix = create_in('../indexDir', schema)
            print('Index create with schema : {}'.format(ix.schema))
            print('Number of document that indexed : {}'.format(ix.doc_count_all()))
            self.ix = ix

    # return the number of document that exist
    def getDocumentCount(self):
        return self.ix.doc_count_all()

    def indexDocument(self):
        writer = self.ix.writer()
        for item in self.data:
            writer.add_document(newsAgency= item['newsagency'],
                                title= item['title'],
                                content= item['content'],
                                url = item['url'])
        writer.commit()
        return True
