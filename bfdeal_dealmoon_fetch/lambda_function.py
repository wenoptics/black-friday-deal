import json
import time

from dealmoon_api import get_dealmoon_deal_list


def lambda_handler(event, context):
    # error = False
    # try:
        deal_list = get_dealmoon_deal_list()

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
                'dealList': json.dumps(deal_list),
                'timestamp': time.time()
            }
        }

