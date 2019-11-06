import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import OnehotTransactions

#Reading CSV file
data_frame = pd.read_csv ("../data/newTrainSet.csv")

array = data_frame.order_id.unique()

data_list = []
for p in array:
    data_list.append((data_frame[data_frame['order_id'] == p].product_id).tolist())

#Rearrange the list so it can be read by apriori()
oht = OnehotTransactions()
oht_ary = oht.fit(data_list).transform(data_list)
one_hot_df = pd.DataFrame(oht_ary, columns=oht.columns_)
#Run apriori algorithm
apriori_result = apriori(one_hot_df, min_support=0.003)

#Finding the association rules
association = association_rules(apriori_result, metric="confidence", min_threshold=0.25)
association = association.drop('lift',1)

#Mapping ID to product name
product_names = pd.read_csv ("../data/products.csv")

for i in range(0,len(association)):
	nj=[]
	
	for j in association.antecedants.loc[i]:
		index = list(one_hot_df)[j]
		nj.append(product_names[product_names['product_id']==index].product_name.item())
	association.antecedants.loc[i]= nj
	
	nj=[]
	for j in association.consequents.loc[i]:
		index = list(one_hot_df)[j]
		nj.append(product_names[product_names['product_id']==index].product_name.item())
	association.consequents.loc[i]= nj

#Writing the results in a CSV file
association.to_csv(path_or_buf="../out/confidence.csv", index=False)
