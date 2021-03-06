#!/bin/bash
export BASE_DIR=~/projects/black-friday-deal
export LAMBDA_FUNCTION_NAME=dealmoon_deals

pushd ${BASE_DIR}/venv/lib/python3.7/site-packages/ || exit
zip -r9 ${BASE_DIR}/bfdeal_dealmoon_fetch/deploy.zip .

pushd ${BASE_DIR}/bfdeal_dealmoon_fetch/ || exit
zip -g deploy.zip dealmoon_api.py
zip -g deploy.zip lambda_function.py
zip -g deploy.zip storage.py

echo "Uploading Lambda Function ${LAMBDA_FUNCTION_NAME}..."
aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --zip-file fileb://deploy.zip

