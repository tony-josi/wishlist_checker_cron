from bs4 import BeautifulSoup
import requests
import threading
import time
import datetime
import sys
import platform


def get_price(link, op_id):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html5lib')
    results = soup.find(
        'div', attrs={'class': '_3Z5yZS NDB7oB _12iFZG _3PG6Wd'})

    price = results.findAll('div', attrs={'class': '_1vC4OE _3qQ9m1'})
    price = str(price)
    price_rate_lt = price.split("₹", 1)
    price_rate_rt = price_rate_lt[1].split("<", 1)

    brand_tags = results.findAll('span', attrs={'class': '_2J4LW6'})
    brand_tags = str(brand_tags)
    brand_tags_list_lt = [0] * 2
    if len(brand_tags) > 2:
        try:
            brand_tags_list = brand_tags.split(">", 1)
            brand_tags_list_lt = brand_tags_list[1].split("<", 1)
        except:
            brand_tags_list_lt[0] = brand_tags
    else:
        brand_tags_list_lt[0] = "brand_name_null"

    item_tags = results.findAll('span', attrs={'class': '_35KyD6'})
    item_tags = str(item_tags)
    item_tags_list = item_tags.split(">", 1)
    item_tags_list_lt = item_tags_list[1].split("<", 1)

    op_price_list[op_id] = [brand_tags_list_lt[0],
                            item_tags_list_lt[0], "₹ " + price_rate_rt[0]]
    # print(price_rate_rt[0])


def file_len(fname):
    with open(fname) as fp:
        for i, _ in enumerate(fp):
            pass
    return i + 1


def op_to_file(dest):
    if (dest == 0):
        time_stmp = str(hex(int(time.time())))
        op_file_name = "wl_prices_s_" + time_stmp[2:] + ".txt"
        op_mode = 'w'
    else:
        op_file_name = "wl_prices_master.txt"
        op_mode = 'r+'

    old_data = ''

    ''' check if file exists '''
    try:
        f = open(op_file_name)
    except FileNotFoundError:
        f = open(op_file_name, 'w+')
    finally:
        f.close()

    with open(op_file_name, op_mode) as f:
        if (dest != 0):
            old_data = f.read()
            f.seek(0)
            f.write("\n\n")
            f.write(
                "|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n")
            date_time = "|  / / / / / / / / / / / / / / / / / / / / / /      " + \
                str(datetime.datetime.now()) + \
                "     / / / / / / / / / / / / / / / / / / / / / /  |"
            f.write("%s\n" % date_time)
            f.write(
                "|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n")

        f.write("\n")
        for i in range(ip_count):
            f.write("{:3s} {:13s} {:18s} {:80s} \n".format(
                str(i + 1), op_price_list[i][2], op_price_list[i][0], op_price_list[i][1]))

        f.write("\n\n")
        f.write("Exec. time:      {}\n".format(time_spend))
        f.write(str(platform.uname()) + "\n")
        f.write("\n\n")

        if (dest != 0):
            f.write(
                "|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n")
            f.write(old_data)


if __name__ == '__main__':

    ip_filepath = "wish_list/wish_list.txt"

    f_obj_r = open(ip_filepath, 'r')
    ip_count = file_len(ip_filepath)
    # print(ip_count)

    op_price_list = {}
    exit_flag = 0

    worker_1 = None
    worker_2 = None
    worker_3 = None
    worker_4 = None

    ip_cntr = 0
    start_time = time.time()
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
            worker_1 = threading.Thread(
                target=get_price, args=(line1, ip_cntr,))
            worker_1.start()
        ip_cntr += 1
        line2 = f_obj_r.readline()
        # print(line1)
        if not line2:
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_2 = threading.Thread(
                target=get_price, args=(line2, ip_cntr,))
            worker_2.start()
        ip_cntr += 1
        line3 = f_obj_r.readline()
        if not line3:
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_3 = threading.Thread(
                target=get_price, args=(line3, ip_cntr,))
            worker_3.start()
        ip_cntr += 1
        line4 = f_obj_r.readline()
        if not line4:
            exit_flag = 1
            continue
        else:
            # print("work 1")
            worker_4 = threading.Thread(
                target=get_price, args=(line4, ip_cntr,))
            worker_4.start()
        ip_cntr += 1

        try:
            # print("Exit")
            worker_1.join()
            worker_2.join()
            worker_3.join()
            worker_4.join()
        except:
            pass

    time_spend = time.time() - start_time
    print("Exec. time:      {}".format(time_spend))
    if (len(sys.argv) > 1):
        if (sys.argv[1] == 's'):
            op_to_file(0)
        else:
            op_to_file(1)
    else:
        op_to_file(1)
    # print(op_price_list)