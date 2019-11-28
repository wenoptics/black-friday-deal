import json

from bs4 import BeautifulSoup
import requests

import storage

url_dealmoon = 'https://www.dealmoon.com/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}


import boto3

lambda_client = boto3.client('lambda')


def get_dealmoon_deal_list():
    r = requests.get(url_dealmoon, headers=headers, timeout=3)

    # Parse the deal list
    soup = BeautifulSoup(r.content, 'html.parser')
    del r
    deal_list_container = soup.select('body div.main_wrap section#dealsList')
    deals = deal_list_container[0].select('div.mlist[data-dmt-d-deal-id]')
    del soup

    ret_list = []
    for d in deals:
        # print(d.get('data-dmt-d-deal-id'), d.get('data-ad-type'), d.get('data-dmt-d-value'))
        deal_dict = {
            'title': d.get('data-dmt-d-value'),
            'deal_id': d.get('data-dmt-d-deal-id'),
            'time': d.get('t')
        }
        ret_list.append(deal_dict)

        lambda_client.invoke(
            FunctionName='bfdeal_monitor_push',
            InvocationType='Event',
            LogType='Tail',
            Payload=bytes(json.dumps(deal_dict), encoding='utf8'),
            # Qualifier='1'
        )

        # Persistent to DynamoDB
        storage.update_deal(deal_dict)

    return ret_list


if __name__ == '__main__':
    # Quick test
    print(get_dealmoon_deal_list())
