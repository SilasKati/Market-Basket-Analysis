import pandas as pd
import os
import sys
import pyfim
from fim import fpgrowth

def concat_files(init, end):
    name = 'res'
    extension = '.out'
    filenames = []

    for i in range(init, end):
        filenames.append(name + str(i) + extension)

    with open('./results/out.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
            
                outfile.write('\n') 
                outfile.write('\n')

    for i in range(init, end):
        os.remove(name + str(i) + extension)
    return             

def id_to_name_pyfim():
    products = pd.read_csv("./data/products.csv")
        
    #opening a new file with product names instead of ids
    with open ('./results/results.txt', 'w') as outfile:
        #opening the result of the associations
        with open('./results/out.txt', 'r') as infile:
            #traverses all lines of associations file
            for line in infile:
                
                if line != '\n':
                    #remove parentheses and commas          
                    line = line.replace("(", "")
                    line = line.replace(")", "")
                    line = line.replace(",", "")
                    
                    #create a list containing each string
                    temp_list = line.split(' ')
                    #take the consequent item
                    left_int = int(temp_list[0])
                    left_items = (products.loc[products['product_id'] == left_int]['product_name'].values[0])
                    
                    #taking the confidence separately
                    conf = float(temp_list[len(temp_list) - 1])
                    supp = float(temp_list[len(temp_list) - 2])
                    #removing the confidence (float value) and the consequent item
                    temp_list = temp_list[1:len(temp_list) - 2]
                    #taking the integers for the preceding items
                    right_int = [int(s) for s in temp_list]
                    
                    #transform ids into product name
                    right_items = []
                    for val in right_int:
                        right_items.append(products.loc[products['product_id'] == val]['product_name'].values[0])
                
                    #writing into the file
                    outfile.write(str(left_items) + ' <- ' + str(right_items) + ' ' + str(supp) + ' ' +str(conf) + '\n\n')
            
    return       

#read minimum support and confidence
min_sup = float(sys.argv[1])
min_conf = float(sys.argv[2]) 

#reading the csv file
data_frame = pd.read_csv ("./data/newTrainSet.csv")

#get all unique order ids
array = data_frame.order_id.unique()

#make a list of all orders
data_list = []
for p in data_frame.order_id.unique():
    data_list.append((data_frame[data_frame['order_id'] == p].product_id).tolist())

#execute FP Growth algorithm
result = fpgrowth(data_list, supp=min_sup, conf=min_conf, target='r', report='XC')

#rite the results into a file
i = 0
for p in result:
    filename = "res"
    filename = filename + str(i) + ".out"
    i = i + 1
    f = open(filename, 'w' )
    f.write(repr(p))
    f.close()

concat_files (0, i)
id_to_name_pyfim()
