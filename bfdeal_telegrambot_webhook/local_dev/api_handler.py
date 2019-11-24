"""
Development env, substitute for AWS API Gateway
"""
import json
from pprint import pprint

from flask import request, Flask

from bfdeal_telegrambot_webhook import lambda_function

app = Flask(__name__)  # create the Flask app


@app.route('/telegram_bot/local', methods=['POST'])
def handle_telegram_bot_message():
    req_data = request.get_json()
    pprint(req_data)

    # Pass to lambda (simulating AWS API Gateway)
    lambda_function.lambda_handler(
        {'body': json.dumps(req_data)},
        {}
    )

    return '{"status": 200}'


if __name__ == '__main__':
    app.run(debug=True)
