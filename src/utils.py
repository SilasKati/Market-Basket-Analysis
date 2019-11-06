import pandas as pd
import numpy as np

from aisle import *
from department import *
from product import *
from order import *
from client import *

def read_aisles(datasets_path):
    aisles = []
    print("Reading aisles dataset.")
    aisles_db = pd.read_csv(datasets_path + 'aisles.csv').values
    for i in range(0, aisles_db.shape[0]):
        aisle = Aisle(aisles_db[i][0]-1, aisles_db[i][1])
        aisles.append(aisle)

    return aisles

def read_departments(datasets_path):
    departments = []
    print("Reading departments dataset.")
    departments_db = pd.read_csv(datasets_path + 'departments.csv').values
    for i in range(0, departments_db.shape[0]):
        department = Department(departments_db[i][0]-1, departments_db[i][1])
        departments.append(department)

    return departments

def read_products(datasets_path):
    products = []
    print("Reading products dataset.")
    products_db = pd.read_csv(datasets_path + 'products.csv').values
    for i in range(0, products_db.shape[0]):
        product = Product(products_db[i][0]-1, products_db[i][1], products_db[i][2]-1, products_db[i][3]-1)
        products.append(product)

    return products

def read_orders_clients(datasets_path, departments, products):
    print("Reading orders dataset.")
    orders_df = pd.read_csv(datasets_path + 'orders.csv')   #data frame
    orders_db = orders_df.values
    norders = orders_db.shape[0]
    orders = [None]*norders
    clients = []

    last_userID = 0
    cur_orders = []
    for i in range(0, orders_db.shape[0]):
        cur_userID = orders_db[i][1]-1
        if cur_userID != last_userID:
            client = Client(cur_userID, cur_orders)
            clients.append(client)
            cur_orders = []
            last_userID = cur_userID

        order = Order(orders_db[i][0]-1, cur_userID, orders_db[i][2], orders_db[i][3], orders_db[i][4], orders_db[i][5], orders_db[i][6])
        cur_orders.append(order)
        orders[order.order_id] = order

    find_order_products(datasets_path, orders, departments, products)
    
    orders = [x for x in orders if len(x.products) != 0]		

    return (orders, clients)
