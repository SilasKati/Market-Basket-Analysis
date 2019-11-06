# Clustering customers and Market basket analysis on Instacart dataset
Finding buying patterns through clustering and association rule methods on Instacart data set.

Before running any script, download all datasets provided [on Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis/data) and put them under the folder *data/* of this project. **Do not** change the original names of the datasets.


## Clustering customers
Install python 3 and the following dependences: *matplotlib*, *numpy* and *sklearn*.

While in the root folder of the project, type in a terminal `python3 src/clustering.py`.

After the complete execution of the script, a textual interface will ask which option you want to execute. The results are showed using charts.

**Important**: to execute this script, it's advised that your computer has at least 8GB of RAM.

## Association rules with Apriori
Install python 3 and the following dependences: *pandas*, *numpy* and *mlxtend*.

### How to preprocess the dataset:
While in the root folder of the project, type in a terminal `python3 src/aprioriPreProcess.py`.

As a result, the script will create a file named *newTrainSet.csv* in the *data/* folder, and a file named *caracteristicas.txt* in the *out/* folder. They represent, respectively, the train dataset and a file with information about it.

### How to run the apriori algorithm
While in the root folder of the project, type in a terminal `python3 src/apriori.py`.

The output of the script will be placed under the *out/* folder. It is a file called *confidence.csv* where you'll find the association rules along with the support and confidence levels.

## Association rules with FP-Growth
Install python 3 and the following dependences: *pandas* and *pyfim*.

While in the root folder of the project, type in a terminal `python3 fpgrowth_pyfim.py <min_supp> <min_conf>`, where *min_supp* is the minimum support threshold (0-100), and *min_conf* is the minimum confidence (0-100).

The output of the script is a file called *results.txt* in the *results/* folder. Inside this file you'll find the association rules along with the support and confidence levels.
