"""
Development env, substitute for AWS API Gateway
"""
import json
from pprint import pprint

from bfdeal_monitor_push import lambda_function


def test_deal(deal_text, url):

    # Pass to lambda (simulating AWS API Gateway)
    lambda_function.lambda_handler({
        'body': json.dumps({
            'title': deal_text,
            'deal_url': url
        })}, {}
    )

    return '{"status": 200}'


if __name__ == '__main__':
    test_deal('a123相机b123', 'https://google.com/')
