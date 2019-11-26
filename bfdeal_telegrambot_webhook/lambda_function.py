import json
import os
import requests
# from botocore.vendored import requests
import boto3

import storage_user

TELE_TOKEN = os.environ['TELEBOT_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)

HELP_TEXT = """Supported commands are:
/getNewestDeal
/mySubscription
/addOneKeyword
"""


def get_newest_deal_from_db():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dealmoon_deals')
    return table.scan(Limit=1)['Items'][0]


def send_message(text, chat_id, **kwargs):
    data = {
        'text': text,
        'chat_id': chat_id
    }
    data.update(kwargs)
    requests.post(URL + "sendMessage", data)


def parse_command(raw_text: str):
    # try:
        raw_text = raw_text.strip()
        if not raw_text.startswith('/'):
            return True, None, None
        _arr = raw_text.split(' ')
        if len(_arr) == 1:
            return False, _arr[0], ''
        return False, _arr[0], ' '.join(_arr[1:])
    # except Exception:
    #     return True, None, None


def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    msg_text = message['message']['text'].strip()

    error, cmd, text = parse_command(msg_text)
    if error:
        send_message(HELP_TEXT, chat_id)
        return {
            'statusCode': 200,
            'msg': 'parse cmd error'
        }

    print(cmd, text)

    if cmd == '/getNewestDeal':
        deal = get_newest_deal_from_db()
        send_message(f'Here are the newest deals from Dealmoon:\n'
                     f'{deal["title"]}', chat_id)
    elif cmd == '/mySubscription':
        subs = storage_user.get_user_keywords(chat_id)
        if not subs:
            msg = 'You have not any subscriptions yet. ' \
                  'Use /addOneKeyword to add one keyword.'
        else:
            msg = 'Your subscriptions: ' +\
                  ', '.join([f'<b>{s}</b>' for s in subs])
        print(msg)
        send_message(msg, chat_id, parse_mode='HTML')
    elif cmd == '/addOneKeyword':
        keyword = text
        if not keyword:
            send_message(f'Usage: {cmd} _<your-monitoring-keyword>_', chat_id, parse_mode='Markdown')
            return
        storage_user.add_user_keyword(chat_id, keyword)
        send_message(f'Keyword <b>{keyword}</b> added.', chat_id, parse_mode='HTML')
    else:
        send_message(HELP_TEXT, chat_id)

    return {
        'statusCode': 200
    }
