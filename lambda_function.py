import json

from dealmoon_api import get_dealmoon_deal_list


def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': {
            'dealList': json.dumps(get_dealmoon_deal_list())
        }
    }
