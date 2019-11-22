from bs4 import BeautifulSoup
import requests


def get_dealmoon_deal_list():
    url_dealmoon = 'https://www.dealmoon.com/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    r = requests.get(url_dealmoon, headers=headers, timeout=3)

    soup = BeautifulSoup(r.content, 'html.parser')
    deal_list_container = soup.select('body div.main_wrap section#dealsList')
    deals = deal_list_container[0].select('div.mlist[data-dmt-d-deal-id]')

    ret = []
    for d in deals:
        # print(d.get('data-dmt-d-deal-id'), d.get('data-ad-type'), d.get('data-dmt-d-value'))
        ret.append({
            'title': d.get('data-dmt-d-value'),
            'deal-id': d.get('data-dmt-d-deal-id'),
            'time': d.get('t')
        })

    return ret


if __name__ == '__main__':
    print(get_dealmoon_deal_list())
