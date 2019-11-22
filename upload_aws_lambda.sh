#!/bin/bash

pushd venv/lib/python3.7/site-packages/ || exit
zip -r9 ~/projects/black-friday-deal/function.zip .
popd
zip -g function.zip dealmoon_api.py
zip -g function.zip lambda_function.py
aws lambda update-function-code --function-name dealmoon_deals --zip-file fileb://function.zip
