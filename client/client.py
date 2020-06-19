import pika
import os


class Client:

    # clears screen
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def callback(self, ch, method, properties, body):
        self.clear()
        print('Directory:')
        body = (body.decode('utf-8'))
        print(body.replace("[", '').replace("]", '').replace("'", '').replace(', ', '\n'))

    def start_client(self, broker_host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_host))
        channel = connection.channel()
        channel.queue_declare(queue='dir')

        channel.basic_consume(
            queue='dir', on_message_callback=self.callback, auto_ack=True)

        try:
            print('Waiting...')
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Exit...')


if __name__ == "__main__":
    file = open('client.conf', 'r')
    broker_host = file.readline().replace("\n", "").replace('host=', '')
    Client().start_client(broker_host)
