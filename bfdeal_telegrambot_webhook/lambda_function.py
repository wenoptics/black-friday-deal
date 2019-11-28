import json
import os
import requests
# from botocore.vendored import requests
import boto3

import storage_user
import telegram_api

HELP_TEXT = """Supported commands are:
/getNewestDeal
/mySubscription
/addOneKeyword
"""


def get_newest_deal_from_db():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dealmoon_deals')
    return table.scan(Limit=1)['Items'][0]


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
    """
    Lambda entrance
    """
    try:
        message = json.loads(event['body'])
        chat_id = message['message']['chat']['id']
        msg_text = message['message']['text'].strip()

        error, cmd, text = parse_command(msg_text)
        if error:
            telegram_api.send_message(HELP_TEXT, chat_id)
            return {
                'statusCode': 200,
                'body': 'parse cmd error'
            }

        print(cmd, text)

        if cmd == '/start':
            telegram_api.send_message(f"""Welcome! You can use this bot to subscribe the deals you interested in.""",
                                      chat_id, parse_mode='HTML')
            telegram_api.send_message(HELP_TEXT,
                                      chat_id, parse_mode='HTML')
        elif cmd == '/getNewestDeal':
            deal = get_newest_deal_from_db()
            telegram_api.send_message(f'Here are the newest deals from Dealmoon:\n'
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
            telegram_api.send_message(msg, chat_id, parse_mode='HTML')
        elif cmd == '/addOneKeyword':
            keyword = text
            if not keyword:
                telegram_api.send_message(f'Usage: {cmd} _<your-monitoring-keyword>_', chat_id, parse_mode='Markdown')
                return {
                    'statusCode': 200,
                    'body': 'error'
                }
            storage_user.add_user_keyword(chat_id, keyword)
            telegram_api.send_message(f'Keyword <b>{keyword}</b> added.', chat_id, parse_mode='HTML')
        else:
            telegram_api.send_message(HELP_TEXT, chat_id)
    except Exception:
        return {
            'statusCode': 200,
            'body': 'error'
        }
    else:
        return {
            'statusCode': 200,
            'body': 'ok'
        }
    finally:
        return {
            'statusCode': 200,
            'body': 'finally'
        }
