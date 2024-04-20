import pika
from mongoengine import connect
from models import Contact

connect('web8', host='mongodb+srv://flairimoll:h4G2#6tAA$.s59Z@web8.jltbxwa.mongodb.net/?retryWrites=true&w=majority&appName=web8')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue', durable=True)

def send_email(contact_id):
    print(f"Відправлено email контакту з ID: {contact_id}")
    
    contact = Contact.objects.get(id=contact_id)
    contact.is_sent = True
    contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='contacts_queue', on_message_callback=callback)

print('Чекаю на повідомлення. Для виходу натисніть CTRL+C')
channel.start_consuming()
