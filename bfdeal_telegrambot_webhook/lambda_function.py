import json
import os
import requests
# from botocore.vendored import requests
import boto3

TELE_TOKEN = os.environ['TELEBOT_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)

HELP_TEXT = """Supported commands are:
/getNewestDeal
/mySubscription
"""


def get_newest_deal_from_db():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dealmoon_deals')
    return table.scan(Limit=1)['Items'][0]


def send_message(text, chat_id):
    requests.post(URL + "sendMessage", {
        'text': text,
        'chat_id': chat_id
    })


def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    msg_text = message['message']['text'].strip()

    if msg_text == '/getNewestDeal':
        deal = get_newest_deal_from_db()
        send_message(f'Here are the newest deals from Dealmoon:\n'
                     f'{deal["title"]}', chat_id)
    elif msg_text == '/mySubscription':
        send_message('Your subscriptions: []', chat_id)
    else:
        send_message(HELP_TEXT, chat_id)

    return {
        'statusCode': 200
    }
