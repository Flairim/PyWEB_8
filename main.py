import json
from mongoengine import connect
from models import Author, Quote

def connect_to_database():
    connect('web8', host='mongodb+srv://flairimoll:h4G2#6tAA$.s59Z@web8.jltbxwa.mongodb.net/?retryWrites=true&w=majority&appName=web8')

def load_data_from_files():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
    
    with open('qoutes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        
    return authors_data, quotes_data

def save_authors_to_db(authors_data):
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

def save_quotes_to_db(quotes_data):
    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Author.objects.get(fullname=author_name)
        quote_data['author'] = author
        quote = Quote(**quote_data)
        quote.save()

def search_quotes():
    while True:
        command = input("Введіть команду (напр. name: Steve Martin, tag:life, tags:life,live, exit): ")
        
        if command == 'exit':
            break
        
        if command.startswith('name:'):
            _, author_name = command.split(':', 1)
            author = Author.objects.get(fullname=author_name.strip())
            quotes = Quote.objects.filter(author=author)
            
        elif command.startswith('tag:'):
            _, tag = command.split(':', 1)
            quotes = Quote.objects.filter(tags__contains=tag.strip())
            
        elif command.startswith('tags:'):
            _, tags = command.split(':', 1)
            tags_list = [tag.strip() for tag in tags.split(',')]
            quotes = Quote.objects.filter(tags__in=tags_list)
            
        else:
            print("Невірна команда")
            continue
        
        for quote in quotes:
            print(quote.quote)

if __name__ == "__main__":
    connect_to_database()
    authors_data, quotes_data = load_data_from_files()
    save_authors_to_db(authors_data)
    save_quotes_to_db(quotes_data)
    search_quotes()
