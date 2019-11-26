#!/bin/bash
export BASE_DIR=~/projects/black-friday-deal
export LAMBDA_FUNCTION_NAME=dealmoon_bot_handler

pushd ${BASE_DIR}/venv/lib/python3.7/site-packages/ || exit
zip -r9 ${BASE_DIR}/bfdeal_telegrambot_webhook/deploy.zip .

pushd ${BASE_DIR}/bfdeal_telegrambot_webhook/ || exit
zip -g deploy.zip lambda_function.py
zip -g deploy.zip storage_user.py

echo 'Uploading Lambda Function...'
aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --zip-file fileb://deploy.zip

