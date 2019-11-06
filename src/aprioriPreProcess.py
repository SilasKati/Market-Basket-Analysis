import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import OnehotTransactions

#The number of orders that will be used to build the train set
NUM_OF_ORDERS = 10000

#Reads the full order train dataset
source_data_frame = pd.read_csv ("../data/order_products__train.csv")

#Remove the columns that are useless
source_data_frame = source_data_frame.drop('add_to_cart_order', 1)
source_data_frame = source_data_frame.drop('reordered', 1)

#Randomize the rows, and select 10000 orders
array = source_data_frame.order_id.unique()
np.random.shuffle(array)
array = array[0:NUM_OF_ORDERS]

#Write the values to a csv file
trues = source_data_frame['order_id'].isin(array)
source_data_frame = source_data_frame.loc[trues]
source_data_frame.to_csv("../data/newTrainSet.csv", index=False)

#Now it writes file with some info about the containing data
avgProdPerOrder = len(source_data_frame)/NUM_OF_ORDERS
numOfProducts = len(source_data_frame.product_id.unique())
file = open("../out/characteristics.txt", 'w')
file.write("Total Purchases: " + str(NUM_OF_ORDERS));
file.write("\nTotal products: " + str(numOfProducts));
file.write("\nTotal products purchased: " + str(len(source_data_frame)));
file.write("\nAverage products per purchase: " + str(avgProdPerOrder));
file.write("\nAverage frequency of a product in a purchase: " + str(avgProdPerOrder/numOfProducts));
file.close()