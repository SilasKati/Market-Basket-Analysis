# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.patches import Circle
from sklearn.cluster import KMeans
from math import isnan
import numpy as np
from utils import *

def plotDistOrderForCustomer(clients):
    x = []
    for client in clients:
        x.append(client.norders)
    un, cnt = np.unique(x, return_counts=True)
    cnt = [x/len(clients) for x in cnt]
    plt.plot(un, cnt, c="r")
    plt.xlabel("Number of Orders (n)")
    plt.ylabel("Probability of a random client having n requests (Pn)")
    plt.show()
   
def plotDistProductsByOrder(orders):
	x = []
	for order in orders:
		x.append(len(order.products))
	un, cnt = np.unique(x, return_counts=True)
	cnt = [x/len(orders) for x in cnt]
	plt.plot(un, cnt, c="g")
	plt.xlabel("Number of products (n)")
	plt.ylabel("Probability of a random order having n products (Pn)")
	plt.show()

def plotDistRequiresBy(orders, w2):
	x = []
	col = []
	labels = []
	for order in orders:
		x.append(order.order_dow + (order.order_hod/24))
	un, cnt = np.unique(x, return_counts=True)
	for i in un:
		i = i%1
		if i >= 0 and i <= 0.25:
			col.append("plum")
			labels.append("manhã")
		elif i > 0.25 and i <= 0.5:
			col.append("skyblue")
			labels.append("dia")
		elif i > 0.5 and i <= 0.75:
			col.append("gold")
			labels.append("tarde")
		else:
			col.append("brown")
			labels.append("noite")
	cnt = [x/len(orders) for x in cnt]
	plt.bar(un, cnt, width=w2, color=col, label=labels)
	patches = [Circle((0,0),color="plum"), Circle((0,0),color="skyblue"), Circle((0,0),color="gold"), Circle((0,0),color="brown")]
	plt.legend(patches, ["morning", "day", "afternoon", "night"])
	plt.xticks(range(7), ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'))
	plt.xlabel("Day and time of week (d)")
	plt.ylabel("Probability of a random order on day and time d")
	plt.show()

def runKmeans(clients, nClients, nClusters):
    cmap = cm.get_cmap('rainbow', nClusters)
    clientColors = []
    clientValues = []
    print("Generating customer characteristics matrix ...")
    for i in range(0, nClients):
        client = clients[i]
        clientRecurrences = []
        clientPurchaseTimes = []
        for order in client.orders:
            clientPurchaseTimes.append(max(order.order_hod, 24-order.order_hod))
            if not isnan(order.days_spo):
                clientRecurrences.append(order.days_spo)
        clientValues.append([client.norders, np.median(clientRecurrences), np.median(clientPurchaseTimes)])
    print("Running Kmeans...")
    kmeans = KMeans(n_clusters=nClusters, random_state=0).fit(clientValues)
    for label in kmeans.labels_:
        clientColors.append(cmap(label))
    fig = plt.figure()
    ax = Axes3D(fig)
    zi = list(zip(*clientValues))
    ax.scatter(zi[0], zi[1], zi[2], c=clientColors)
    zi = list(zip(*kmeans.cluster_centers_))
    ax.scatter(zi[0], zi[1], zi[2], c="k", s=30, marker='*')
    ax.set_xlabel('Number of Orders')
    ax.set_ylabel('Average purchase recurrence (in days)')
    ax.set_zlabel('Average purchase time')
    ax.set_zticks((12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24))
    ax.set_zticklabels(('12h', '13|11h','14|10h', '15|9h', '16|8h', '17|7h', '18|6h', '19|5h', '20|4h', '21|3h', '22|2h', '23|1h', '24h'))
    plt.show()

def main():
	datasets_path = './data/'

	aisles = read_aisles(datasets_path)
	departments = read_departments(datasets_path)
	products = read_products(datasets_path)
	orders, clients = read_orders_clients(datasets_path, departments, products)
	
	opt = -1
	while opt != 0:
		opt = int(input("Choose one of the options below:\n\t\
1 - Plot order distribution by customer.\n\t\
2 - Plot product distribution by order.\n\t\
3 - Plot order distribution by day and time of week.\n\t\
4 - Execute K-means.\n\t\
0 - Exit\nYour option = "))
		if opt == 1:
			plotDistOrderForCustomer(clients)
		elif opt == 2:
			plotDistProductsByOrder(orders)
		elif opt == 3:
			plotDistRequiresBy(orders, 0.033)
		elif opt == 4:
			K = int(input("Defina um número de clusters para o K-means = "))
			print("Executando K-means com K =", K, "...")
			runKmeans(clients, len(clients), K)
			
if __name__ == "__main__":
	main()
