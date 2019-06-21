from whoosh.fields import SchemaClass,TEXT,DATETIME,ID

class NewsSchema(SchemaClass):
    newsAgency = TEXT
    title = TEXT(stored=True)
    summary = TEXT(stored=True)
    url = ID(stored=True)
    content = TEXT
    # date = DATETIME
    # time = DATETIME
    