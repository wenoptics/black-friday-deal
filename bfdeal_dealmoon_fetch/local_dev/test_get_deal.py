"""
Development env, substitute for AWS API Gateway
"""
import json
from pprint import pprint

import lambda_function


def test_fetch():

    # Pass to lambda (simulating AWS API Gateway)
    lambda_function.lambda_handler({
        'body': ""
    }, {})

    return '{"status": 200}'


if __name__ == '__main__':
    test_fetch()
