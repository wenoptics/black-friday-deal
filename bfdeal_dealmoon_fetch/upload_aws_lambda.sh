#!/bin/bash

pushd venv/lib/python3.7/site-packages/ || exit
zip -r9 ~/projects/black-friday-deal/bfdeal_dealmoon_fetch/deploy.zip .
popd

pushd bfdeal_dealmoon_fetch/ || exit
zip -g deploy.zip dealmoon_api.py
zip -g deploy.zip lambda_function.py
zip -g deploy.zip storage.py

echo 'Uploading Lambda Function...'
aws lambda update-function-code --function-name dealmoon_deals --zip-file fileb://function.zip
popd
