import pika
from mongoengine import connect
from models import Contact

def connect_to_database():
    connect('web8', host='mongodb+srv://flairimoll:h4G2#6tAA$.s59Z@web8.jltbxwa.mongodb.net/?retryWrites=true&w=majority&appName=web8')

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    print(f" [x] Отримано {contact_id}")

    send_email_stub(contact)

    contact.is_sent = True
    contact.save()
    print(f" [x] Позначено {contact_id} як відправлено")

def send_email_stub(contact):
    print(f" [x] Надсилаємо email на {contact.email} з темою '{contact.subject}' та повідомленням '{contact.message}'")

if __name__ == "__main__":
    connect_to_database()

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='contacts_queue')

    channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Очікування повідомлень. Для виходу натисніть CTRL+C')
    channel.start_consuming()
