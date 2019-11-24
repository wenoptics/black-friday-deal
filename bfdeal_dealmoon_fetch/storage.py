import decimal

import boto3

# Get the service resource.
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('dealmoon_deals_table')


def update_deal(deal_dict):
    """
    Create a deal or update one
    """

    try:
        table.put_item(
            Item={
                'deal_id': str(deal_dict['deal_id']),
                'update_time': int(deal_dict['time']),
                'title': deal_dict['title'],
            },
            ConditionExpression=Attr('deal_id').ne(str(deal_dict['deal_id']))
        )
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ConditionalCheckFailedException':
            # print("Key already exists")
            table.update_item(
                Key={
                    'deal_id': str(deal_dict['deal_id']),
                },
                UpdateExpression="SET update_time = :t , title = :p",
                ExpressionAttributeValues={
                    ':t': decimal.Decimal(deal_dict['time']),
                    ':p': deal_dict['title'],
                }
            )
        else:
            raise ce


def write_deal(deal_dict):
    table.put_item(
        Item={
            'deal_id': str(deal_dict['deal_id']),
            'timestamp_': int(deal_dict['time']),
            'title': deal_dict['title'],
        }
    )


def write_deals_batch(deal_list):
    with table.batch_writer() as batch:
        for deal_dict in deal_list:
            batch.put_item(Item={
                'deal_id': str(deal_dict['deal_id']),
                'timestamp_': int(deal_dict['time']),
                'title': deal_dict['title'],
            })


if __name__ == '__main__':
    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    print(table.creation_date_time)

    # write_deal({
    #     'deal_id': -1,
    #     'time': 0,
    #     'title': 'test2'
    # })

    print(table.scan(Limit=1))
