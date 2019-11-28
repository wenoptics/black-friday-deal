import decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('dealmoon_user_sub')


def add_user_keyword(user_id, keyword):
    user_id = str(user_id)
    keyword = str(keyword)
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    user = response.get('Item')
    if user:
        # user['sub_list'].add(keyword)
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="ADD sub_list :k",
            ExpressionAttributeValues={
                ':k': {keyword}
            }
        )
    else:
        # No user yet. Add user
        table.put_item(Item={
            'user_id': user_id,
            'sub_list': set([keyword])
        })


def get_user_keywords(user_id):
    user_id = str(user_id)
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    user = response.get('Item')
    if user:
        return list(user['sub_list'])

    return []


def get_active_user_list():
    r = table.scan(FilterExpression=Attr('is_active').eq(True))
    return r['Items']
