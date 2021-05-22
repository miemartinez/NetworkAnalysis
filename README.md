# Network Analysis
### Creating reusable network analysis pipeline
**This project was developed as part of the spring 2021 elective course Cultural Data Science - Language Analytics at Aarhus University.** <br>

__Task:__ The task for this project is to build a command-line tool which will take any weighted edgelist as input, providing that edgelist is saved 
as a CSV with the column headers "nodeA", "nodeB" and perform a simple network analysis. The network will be based on entities appearing together in 
the same documents. For any weighted edgelist given as an input, the script should be used to create a network visualization, which will be saved in 
a folder called viz. It should also create a data frame showing the degree, betweenness, and eigenvector centrality for each node. It should save this 
as a CSV in a folder called output. <br>

A weighted edgelist of the data fake-or-real-news.csv (from Kaggle https://www.kaggle.com/rchitic17/real-or-fake) can be found in the data folder.
Using spacy, all mentions of persons was extracted and it was counted how many times two names co-occured. 
So, the weighted edgelist hold the name of two people (nodeA and nodeB) and number of times they co-occured in a document (weight).

The script is located in the src folder and can be run without specifying further parameters. 
The repository also contains the results from running the network analysis. 
In the viz folder, two plots can be found visualizing the network of the edgelist with and without labels when filtered at 500. 
In the output folder, the centralities measures for the network are saved as a csv. <br> 

__Dependencies:__ <br>
To ensure dependencies are in accordance with the ones used for the script, you can create the virtual environment ‘network_environment"’ from the command line by executing the bash script ‘create_network_venv.sh’. 
```
    $ bash ./create_sentiment_venv.sh
```
This will install an interactive command-line terminal for Python and Jupyter as well as all packages specified in the ‘requirements.txt’ in a virtual environment. 
After creating the environment, it will have to be activated before running the network analysis script.
```    
    $ source network_environment/bin/activate
```
After running these two lines of code, the user can commence running the script. <br>

### How to run network.py <br>
The script network.py can run from command line without additional input. 
However, the user can specify path to the weighted edgelist csv file, a minimum threshold for filtering away edge pairs and 
whether to include labels or not on the network visualization.
The output of the script is a png file of the network and a csv file with three centrality measures (degree, betweenness and eigenvector).

__Parameters:__ <br>
```
    filepath: str <filepath-of-csv-file>, default = "../data/weighted_edgelist.csv"
    weight_threshold: int <filtering-threshold>, default = 500
    include_labels: str <True-or-False>, default = False

```
    
__Usage:__ <br>
```
    network.py -f <filepath-of-csv-file> -w <filtering-threshold> -l <True-or-False>
```
    
__Example:__ <br>
```
    $ cd src
    $ python3 network.py -p -f ../data/weighted_edgelist.csv -w 300 -l True

```

The code has been developed in Jupyter Notebook and tested in the terminal on Jupyter Hub on worker02. I therefore recommend cloning the Github repository to worker02 and running the scripts from there. 

### Results:
The results of the network analysis can be seen in the output and viz folders. Looking at the centrality measures one can see three measures: degree, betweenness and eigenvector centrality. These measures refer to how central the persons are to the network. The most central person seems to be Clinton as it is the node with the most edges/ties (degree centrality = 0.79). Similarly, it is the most important node for the flow of the network since it is the one that best connects many of the other nodes (betweenness centrality = 0.73). Lastly, it is also the node connected to the most central nodes in the network (eigenvector centrality = 0.53). <br>
However, in the csv file of the centrality measures the problem of coreference becomes very apparent. For instance, Hillary Clinton is referred to as “Hillary Rodham Clinton”, “Hillary Clinton”, “Hillary Rodham”, “Hillary”, “Hillary Clinton’s”, “Rodham”, “Clintons” and “Clinton” (which might also refer to Bill Clinton). As these are all connected to the Clinton node this greatly influence the results of the analysis as they all refer to the same person and therefore should constitute only one node and not eight. The only way to solve this problem is to resolve all mentions of the same person entity within a document. <br>

Here, you can see what the network looks like without labels:
![alt text](https://github.com/miemartinez/NetworkAnalysis/blob/main/viz/network.png?raw=true)

And with labels:
![alt text](https://github.com/miemartinez/NetworkAnalysis/blob/main/viz/network_w_labels.png?raw=true)

