import json
import time

import storage_user
import telegram_api


def lambda_handler(event, context):
    """
    payload like:
        {
            "deal_text": "str",
            "deal_url": "str"
        }
    """
    # error = False
    # try:
    payload = json.loads(event['body'])
    deal_text = payload['title']
    deal_url = payload['deal_url']

    for user in storage_user.get_active_user_list():
        for kw in user['sub_list']:
            if kw == '':
                continue
            if kw in deal_text:
                telegram_api.send_message(f'Deal Alert: {deal_text} Source:<a href="{deal_url}">Dealmoon</a>',
                                          user['user_id'],
                                          parse_mode='HTML')
                break

    # except Exception as e:
    #     error_text = str(e)
    #     return {
    #         'statusCode': -1,
    #         'body': {
    #             'error': str(e),
    #             'timestamp': time.time()
    #         }
    #     }
    # else:
    return {
        'statusCode': 200,
        'body': {
            'timestamp': time.time()
        }
    }
