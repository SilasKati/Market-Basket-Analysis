import pandas as pd
import numpy as np

def find_order_products(datasets_path, orders_list, departments, products):
    print("Reading order_products__prior dataset.")
    prior_db = pd.read_csv(datasets_path + 'order_products__prior.csv').values
    print("Reading order_products__train dataset.")
    train_db = pd.read_csv(datasets_path + 'order_products__train.csv').values

    max_dep = np.zeros(len(departments)+1)
    last_order_id = prior_db[0][0]-1
    print("Processing prior_db...")
    cntP = 0
    for item in prior_db:
        order_id = item[0]-1
        product_id = item[1]-1
        reordered = item[3]
        order = orders_list[order_id]
        order.products.append(product_id)
        order.reordered.append(reordered)
        if (order_id != last_order_id):
            last_order_id = order_id
            order.major_dep = np.argmax(max_dep)
            max_dep = np.zeros(len(departments)+1)
        else:
            max_dep[products[product_id].department] += 1
        cntP += 1

    max_dep = np.zeros(len(departments)+1)
    last_order_id = train_db[0][0]-1
    print("Processing train_db...")
    cntT = 0
    for item in train_db:
        order_id = item[0]-1
        product_id = item[1]-1
        reordered = item[3]
        order = orders_list[order_id]
        order.products.append(product_id)
        order.reordered.append(reordered)
        if (order_id != last_order_id):
            last_order_id = order_id
            order.major_dep = np.argmax(max_dep)
            max_dep = np.zeros(len(departments)+1)
        else:
            max_dep[products[product_id].department] += 1
        cntT += 1

class Order:
    def __init__(self, order_id, user_id, eval_set, order_number, order_dow, order_hod, days_spo):
        self.order_id = order_id
        self.user_id = user_id
        self.eval_set = eval_set
        self.order_number = order_number
        self.order_dow = order_dow  #day of the week
        self.order_hod = order_hod  #time of day
        self.days_spo = days_spo    #days since last order
        self.products = []          #product ids
        self.reordered = []         #if the customer has already purchased this product before
        self.major_dep = -1
