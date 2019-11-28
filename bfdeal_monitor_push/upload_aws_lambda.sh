#!/bin/bash
export BASE_DIR=~/projects/black-friday-deal
export LAMBDA_FUNCTION_NAME=bfdeal_monitor_push

pushd ${BASE_DIR}/venv/lib/python3.7/site-packages/ || exit
zip -r9 ${BASE_DIR}/bfdeal_monitor_push/deploy.zip .

pushd ${BASE_DIR}/bfdeal_monitor_push/ || exit
zip -g deploy.zip lambda_function.py
zip -g deploy.zip ../bfdeal_telegrambot_webhook/storage_user.py
zip -g deploy.zip ../bfdeal_telegrambot_webhook/telegram_api.py

echo "Uploading Lambda Function ${LAMBDA_FUNCTION_NAME}..."
aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --zip-file fileb://deploy.zip

