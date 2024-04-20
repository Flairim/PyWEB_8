from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, Document, StringField, EmailField, BooleanField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    is_sent = BooleanField(default=False)
    phone = StringField()
