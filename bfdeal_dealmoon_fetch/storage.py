import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('dealmoon_deals')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)


def write_deal(deal_dict):
    table.put_item(
        Item={
            'deal_id': str(deal_dict['deal_id']),
            'timestamp': int(deal_dict['time']),
            'title': deal_dict['title'],
        }
    )


def write_deals_batch(deal_list):
    with table.batch_writer() as batch:
        for deal_dict in deal_list:
            batch.put_item(Item={
                'deal_id': str(deal_dict['deal_id']),
                'timestamp': int(deal_dict['time']),
                'title': deal_dict['title'],
            })


if __name__ == '__main__':
    write_deal({
        'deal_id': -1,
        'time': 0,
        'title': 'test2'
    })
