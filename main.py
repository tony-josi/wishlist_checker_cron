from bs4 import BeautifulSoup
import requests
import threading

def get_price(link, op_id):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html5lib')
    results = soup.find('div', attrs={'class':'_3Z5yZS NDB7oB _12iFZG _3PG6Wd'})
    price = results.findAll('div', attrs = {'class':'_1vC4OE _3qQ9m1'})
    price = str(price)
    price_rate_lt = price.split("₹", 1)
    price_rate_rt = price_rate_lt[1].split("<",1)
    op_price_list[op_id] = price_rate_rt[0]
    # print(price_rate_rt[0])

def file_len(fname):
    with open(fname) as fp:
        for i, l in enumerate(fp):
            pass
    return i + 1

if __name__ == '__main__':

    ip_filepath = "wish_list/wish_list.txt"

    f_obj_r = open(ip_filepath, 'r') 
    ip_count = file_len(ip_filepath)
    #print(ip_count)

    op_price_list = [0] * ip_count
    exit_flag = 0

    worker_1 = None
    worker_2 = None
    worker_3 = None
    worker_4 = None

    ip_cntr = 0
    while True:

        if exit_flag:
            try:
                # print("Exit")
                worker_1.join()
                worker_2.join()
                worker_3.join()
                worker_4.join()
                break
            except:
                break

        line1 = f_obj_r.readline()
        # print(line1)
        if not line1:
            # print("here")
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_1 = threading.Thread(target = get_price, args=(line1, ip_cntr,))
            worker_1.start()
        ip_cntr += 1
        line2 = f_obj_r.readline()
        # print(line1)
        if not line2:
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_2 = threading.Thread(target = get_price, args=(line2, ip_cntr,))
            worker_2.start()
        ip_cntr += 1
        line3 = f_obj_r.readline()
        if not line3:
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_3 = threading.Thread(target = get_price, args=(line3, ip_cntr,))
            worker_3.start()
        ip_cntr += 1
        line4 = f_obj_r.readline()
        if not line4:
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_4 = threading.Thread(target = get_price, args=(line4, ip_cntr,))
            worker_4.start()
        ip_cntr += 1
        
    
    print(op_price_list)