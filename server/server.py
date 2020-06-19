import pika
import os
import time


def server(path, broker_host):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_host))
        channel = connection.channel()

        channel.queue_declare(queue='dir')
        before = [f for f in os.listdir(path)]
        # lists changes in directory
        while 1:
            time.sleep(1)
            channel.basic_publish(exchange='', routing_key='dir',
                                  body=str(before))
            after = [f for f in os.listdir(path)]
            added = [f for f in after if f not in before]
            removed = [f for f in before if f not in after]
            if added:
                channel.basic_publish(exchange='', routing_key='dir',
                                      body=str(after))
                print('Directory status send!')
            if removed:
                channel.basic_publish(exchange='', routing_key='dir',
                                      body=str(after))
                print('Directory status send!')
            before = after
    except KeyboardInterrupt:
        print('Exit...')


if __name__ == "__main__":
    file = open('server.conf', 'r')
    arg = file.readline().replace("\n", "").replace('path=', '')
    broker_host = file.readline().replace("\n", "").replace('host=', '')
    server(arg, broker_host)
