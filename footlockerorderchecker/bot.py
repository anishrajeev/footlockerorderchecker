import requests
from time import time
import json
def main():
    with requests.session() as request:
        milliseconds = int(time() * 1000)
        url = 'https://www.footlocker.com/api/v3/session?timestamp='+ str(milliseconds)
        headers = {
            'authority': 'www.footlocker.com',
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            'sec-fetch-site' : 'same-origin',
            'sec-fetch-mode' : 'cors',
            'sec-fetch-dest' : 'empty',
            'referer' : 'https://www.footlocker.com/order/search.html',
            'accept-language' : 'en-US,en;q=0.9'
        }
        response = request.get(url, headers=headers)
        response = json.loads(response.text)
        csrfToken = response['data']['csrfToken']
        jsessionid = request.cookies.get_dict()['JSESSIONID']
        f = open("orders.txt", "r")
        c = 0
        input = f.read()
        num = input[0]
        input = input[2:]
        while(c<int(num)):
            commaindex = input.index(',')
            email = input[:commaindex]
            ordernum = '';
            try:
                newlineindex = input.index('\n')
                ordernum = input[commaindex + 2:newlineindex]
                input = input[newlineindex + 1:]
            except:
                ordernum = input[commaindex + 2:]
            email = email.strip()
            ordernum = ordernum.strip()
            headers = {
                'authority': 'www.footlocker.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'accept': 'application/json',
                'x-csrf-token': csrfToken,
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
                'content-type': 'application/json',
                'origin': 'https://www.footlocker.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.footlocker.com/order/search.html',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'JSESSIONID=' + jsessionid + ';',
            }

            params = (
                ('timestamp', str(int(time() * 1000))),
            )
            data = '{"code":"'+ordernum+'","customerEmail":"'+email+'"}'
            response = requests.post('https://www.footlocker.com/api/users/orders/status', headers=headers, params=params, data=data)
            response = json.loads(response.text)
            try:
                print('Order Email: ' + email + ', Order Number: ' + ordernum + ', Order Status: ' + response['orderStatus'] + ' ,Order Total: ' + response['orderTotal'])
            except:
                print('Order Email: ' + email + ', Order Number: ' + ordernum + ", Order Status: Order not found \n")
            c=c+1
if __name__ == "__main__":
    main()
