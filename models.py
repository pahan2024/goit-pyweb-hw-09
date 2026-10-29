from mongoengine import Document, StringField, ListField, ReferenceField, CASCADE

class Author(Document):
    meta = {'collection': 'authors'}
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    meta = {'collection': 'quotes'}
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE, required=True)
    quote = StringField(required=True)
