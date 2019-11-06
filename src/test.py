from utils import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from sklearn.cluster import KMeans

def howSimilar1(client1, client2):
    c1Products = set([])
    c2Products = set([])
    for order in client1.orders:
        c1Products = c1Products | set(order.products)
    for order in client2.orders:
        c2Products = c2Products | set(order.products)
    return len(c1Products & c2Products)/len(c1Products | c2Products)

def howSimilar2(client1, client2, products):
    c1Departments = set([])
    c2Departments = set([])
    for order in client1.orders:
        X = []
        for product in order.products:
            X.append(products[product].aisle)
        c1Departments = c1Departments | set(X)
    for order in client2.orders:
        X = []
        for product in order.products:
            X.append(products[product].aisle)
        c2Departments = c2Departments | set(X)
    return len(c1Departments & c2Departments)/len(c1Departments | c2Departments)

def howSimilar3(client1, client2, products):
    c1Departments = set([])
    c2Departments = set([])
    for order in client1.orders:
        X = []
        for product in order.products:
            X.append(products[product].department)
        c1Departments = c1Departments | set(X)
    for order in client2.orders:
        X = []
        for product in order.products:
            X.append(products[product].department)
        c2Departments = c2Departments | set(X)
    return len(c1Departments & c2Departments)/len(c1Departments | c2Departments)

def plotXY(clients, products, idxBaseClient):
    x = []
    y = []
    baseClient = clients[idxBaseClient]
    maxNorders = 100
    for client in clients:
        x.append(client.norders)
        y.append(howSimilar3(client, baseClient, products))
    #x = np.linspace(0, maxNorders, maxNorders+1)
    plt.scatter(x, y)
    plt.xlabel('Number of Orders')
    plt.ylabel('Similarity to the customer' + str(int(idxBaseClient)))
    plt.title('A chart \nThe chart caption')
    plt.legend()
    plt.show()

def plotXYZ(clients, products, nClients):
    z = []
    x = list(range(0, nClients))*nClients
    y = np.array([])
    for i in range(0, nClients):
        y = np.append(y, [i]*nClients)
    y = list(y)
    for j in range(0, nClients):
        for i in range(0, nClients):
            z.append(howSimilar2(clients[i], clients[j], products))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    plt.show()

def weirdPlot1(clients, products, departments):
    x = np.linspace(0, len(clients)-1, len(clients))
    y = []
    for client in clients:
        deps = np.zeros(len(departments))
        for order in client.orders:
            for productId in order.products:
                deps[products[productId].department] += 1
        y.append(np.argmax(deps))
    plt.scatter(x, y)
    plt.show()

def weirdPlot2(clients, products, aisles):
    x = np.linspace(0, len(clients)-1, len(clients))
    y = []
    for client in clients:
        aisles = np.zeros(len(aisles))
        for order in client.orders:
            for productId in order.products:
                aisles[products[productId].aisle] += 1
        y.append(np.argmax(aisles))
    plt.scatter(x, y)
    plt.show()

def weirdPlot3(clients, products, aisles):
    x = []
    y = []
    for client in clients:
        ais = np.zeros(len(aisles))
        for order in client.orders:
            for productId in order.products:
                ais[products[productId].aisle] += 1
        y.append(np.argmax(ais))
        x.append(np.max(ais))
    plt.scatter(x, y)
    plt.show()

def weirdPlot4(clients, products, aisles):
    x = []
    y = []
    for client in clients:
        x.append(client.norders)
        c = []
        for order in client.orders:
            if not math.isnan(order.days_spo):
                c.append(order.days_spo)
        y.append(np.mean(c))
    plt.scatter(x, y)
    plt.show()

def weirdPlot5(clients, products, aisles):
    x = []
    y = []
    for client in clients:
        x.append(client.identifier)
        c = []
        for order in client.orders:
            c.append(max(order.order_hod, 24-order.order_hod))
        y.append(np.mean(c))
    plt.scatter(x, y)
    plt.show()

def plotXYZ2(clients, nClients):
    x = []
    y = []
    z = []
    for i in range(0, nClients):
        client = clients[i]
        x.append(client.norders)
        c = []
        d = []
        for order in client.orders:
            d.append(max(order.order_hod, 24-order.order_hod))
            if not math.isnan(order.days_spo):
                c.append(order.days_spo)
        y.append(np.median(c))
        z.append(np.median(d))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    plt.show()

def runKmeans(clients, nClients, nClusters):
    X = []
    x = []
    y = []
    z = []
    colors = ["r", "b", "m", "y", "g"]
    col = []
    for i in range(0, nClients):
        client = clients[i]
        c = []
        d = []
        for order in client.orders:
            d.append(max(order.order_hod, 24-order.order_hod))
            if not math.isnan(order.days_spo):
                c.append(order.days_spo)
        x.append(client.norders)
        y.append(np.median(c))
        z.append(np.median(d))
        X.append([client.norders, np.median(c), np.median(d)])
    print("Running Kmeans...")
    kmeans = KMeans(n_clusters=nClusters, random_state=0).fit(X)
    for label in kmeans.labels_:
        col.append(colors[label])
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, c=col)
    x = []
    y = []
    z = []
    for centroid in kmeans.cluster_centers_:
        x.append(centroid[0])
        y.append(centroid[1])
        z.append(centroid[2])
    ax.scatter(x, y, z, c="k", s=30, marker='*')
    plt.show()

datasets_path = '../data/'

aisles = read_aisles(datasets_path)
departments = read_departments(datasets_path)
products = read_products(datasets_path)
orders, clients = read_orders_clients(datasets_path, departments, products)
