import pika
import json
from mongoengine import connect
from models import Contact

def connect_to_database():
    connect('web8', host='mongodb+srv://flairimoll:h4G2#6tAA$.s59Z@web8.jltbxwa.mongodb.net/?retryWrites=true&w=majority&appName=web8')

def send_contacts_to_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='contacts_queue')

    contacts = []
    for i in range(5):
        contact = Contact(
            fullname=f"John Doe {i}",
            email=f"john.doe{i}@example.com",
            subject="Hello",
            message="This is a test message."
        )
        contact.save()
        contacts.append(str(contact.id))

    for contact_id in contacts:
        channel.basic_publish(exchange='', routing_key='contacts_queue', body=contact_id)
        print(f" [x] Відправлено {contact_id}")

    connection.close()

if __name__ == "__main__":
    connect_to_database()
    send_contacts_to_queue()
