from bs4 import BeautifulSoup
import requests

def get_price(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html5lib')
    results = soup.find('div', attrs={'class':'_3Z5yZS NDB7oB _12iFZG _3PG6Wd'})
    price = results.findAll('div', attrs = {'class':'_1vC4OE _3qQ9m1'})
    price = str(price)
    price_rate_lt = price.split("₹", 1)
    price_rate_rt = price_rate_lt[1].split("<",1)
    return price_rate_rt[0]

if __name__ == '__main__':
    op_price_list = []
    with open("wish_list/wish_list.txt") as fp: 
        for line in fp: 
            op_price_list.append(get_price(line))
    
    print(op_price_list)