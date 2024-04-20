import json
import faker
import pika
from mongoengine import connect
from models import Contact

connect('web8', host='mongodb+srv://flairimoll:h4G2#6tAA$.s59Z@web8.jltbxwa.mongodb.net/?retryWrites=true&w=majority&appName=web8')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contacts_queue', durable=True)

fake = faker.Faker()

for _ in range(10):  
    fullname = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    
    contact = Contact(fullname=fullname, email=email, phone=phone)
    contact.save()
    
    channel.basic_publish(
        exchange='',
        routing_key='contacts_queue',
        body=str(contact.id),
        properties=pika.BasicProperties(
            delivery_mode=2,  
        )
    )

print("Фейкові контакти створено та опубліковано в черзі RabbitMQ")
connection.close()
