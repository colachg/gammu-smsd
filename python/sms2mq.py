#!/usr/bin/env python3
# encoding: utf-8
import os
import datetime
import pika

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = "sms"


def parse_message():
    numparts = int(os.environ["DECODED_PARTS"])
    text = ""
    # Are there any decoded parts?
    if numparts == 0:
        text = os.environ["SMS_1_TEXT"]
    # Get all text parts
    else:
        for i in range(1, numparts + 1):
            varname = "DECODED_%d_TEXT" % i
            if varname in os.environ:
                text = text + os.environ[varname]

    sender = os.environ['SMS_1_NUMBER']
    receive_time = datetime.datetime.now().strftime('%b %d, %y at %H:%M:%S')
    message = 'From：' + sender + '\n\n：' + text + '\n' + receive_time
    print("message is: \n", message)
    return message


def send2queue(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()

    channel.queue_declare(RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key='sms', body=message)
    connection.close()


if __name__ == "__main__":
    text = parse_message()
    send2queue(text)
