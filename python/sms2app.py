#!/usr/bin/env python3
# encoding: utf-8
import os
import pika
import sys
import requests

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = "sms"
TELEGRAM_API = "https://api.telegram.org/bot%s/sendMessage" % os.environ['TELEGRAM_BOT_TOKEN']
CHANIFY_API = "https://api.chanify.net/v1/sender/%s" % os.environ['CHANIFY_TOKEN']


def send2telegram(content):
    req = requests.post(TELEGRAM_API, data={'chat_id': os.environ['TELEGRAM_CHAT_ID'], 'text': content})
    return True if req.status_code == 200 else False


def send2chanify(content):
    req = requests.post(CHANIFY_API, data={'text': content})
    return True if req.status_code == 200 else False


def notify():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        if not send2telegram(body.decode()):
            send2telegram(body.decode())

    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        notify()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
