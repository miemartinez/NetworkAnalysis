#!/usr/bin/env python
"""
Specify file path of a weighted edgelist as a csv file containing three columns named "nodeA", "nodeB" and "weight". Also, specify a threshold for filtering based on weight. Optionally, specify whether to include labels in visualization. Draw and save a network visualization as png in viz folder. Measure degree, betweenness and eigenvector centrality and save as a csv file in output folder.

Parameters:
    input_file: str <filepath-of-csv-file>, default = "../data/weighted_edgelist.csv"
    weight_threshold: int <filtering-threshold>, default = 500
    include_labels: str <True-or-False>, default = False
Usage:
    network.py -f <filepath-of-csv-file> -w <filtering-threshold> -l <True-or-False>
Example:
    $ python3 network.py -f ../data/weighted_edgelist.csv -w 300 -l True
    
## Task
- It should take any weighted edgelist as an input, providing that edgelist is saved as a CSV with the column headers "nodeA", "nodeB" and "weight".
- For any given weighted edgelist given as an input, the script should be used to create a network visualization, which will be saved in a folder called viz.
- It should also create a data frame showing the degree, betweenness, and eigenvector centrality for each node. It should save this as a CSV in a folder called output.
"""

# importing libraries
import os
import argparse
import pandas as pd
from tqdm import tqdm
from collections import Counter

# tool for plotting
import networkx as nx
import matplotlib.pyplot as plt

# spacy
import spacy
# initialise spacy 
nlp = spacy.load("en_core_web_sm")

# argparse 
ap = argparse.ArgumentParser()

# adding argument
# filepath to weighted edgelist
ap.add_argument("-f", "--filepath", 
                default = "../data/weighted_edgelist.csv", 
                help= "Path to the csv-file")

# threshold for filtering out edge pairs based on weight
ap.add_argument("-w", "--weight_threshold", 
                default = 500, 
                help = "Cut-off point to filter data below the specified edge weight")

# including labels for network visualization
ap.add_argument("-l", "--include_labels", 
                default = False, 
                help = "Set to True to include labels on the visualization")
# parsing arguments
args = vars(ap.parse_args())


def main(args):
    '''
    Main function:
    
    '''
    # get path to the csv file
    filepath = args["filepath"]
    
    # define and make threshold integer
    threshold = int(args["weight_threshold"])
    
    # define label
    labels = args["include_labels"]
    
    # Create Network class object
    network = Network(filepath = filepath, 
                      threshold = threshold, 
                      labels = labels)
    
    # use load_and_filter function to make the filtered df
    filtered_df = network.load_and_filter()
    
    # use method network_viz
    G = network.network_viz(filtered_df = filtered_df)
    
    # use method calc_centrality
    network.calc_centrality(G = G)
    
    print("\n[INFO] The script has been completed succesfully. Have a nice day!")

class Network:
    def __init__(self, filepath, threshold, labels):
        '''
        Constructing the Network object
        '''
        self.filepath = filepath
        self.weight_threshold = threshold
        self.labels = labels
        
    def load_and_filter(self):
        '''
        Loading the input data frame and filtering based on weight threshold.
        Returns a filtered data frame
        '''
        print("\n[INFO] Loading weighted edgelist and filtering")
        # read csv file
        weighted_edgelist = pd.read_csv(self.filepath)
        # filtering the weights by user defined threshold
        filtered_df = weighted_edgelist[weighted_edgelist["weight"]>self.weight_threshold]
        
        return filtered_df
    
    def network_viz(self, filtered_df):
        '''
        Makes a viz directory if this doesn't exist already.
        Makes a network visualization based on the filtered data frame. If labels are specified as True labels will be added for each edge
        in the network. Otherwise, these will not be included in the graph. The visualization will be saved as a png file in the viz folder.
        '''    
        # Create viz directory if it doesn't exist
        viz_dir = os.path.join("..", "viz")
        create_dir(dirName = viz_dir)
        
        # suppling the edges and nodes to the graph from pandas data frame
        G = nx.from_pandas_edgelist(filtered_df, "nodeA", "nodeB", ["weight"])
        # creating node positions for G using Graphviz
        pos = nx.nx_agraph.graphviz_layout(G, prog = "neato")
    
        # if user wants labels draw graph with labels and save
        if self.labels == "True":
            # add that to the filename
            viz_filepath = os.path.join(viz_dir, "network_w_labels.png")
            # drawing the graph with labels
            nx.draw(G, pos, with_labels=True, node_size = 20, font_size = 10)
            # saving the graph
            plt.savefig(viz_filepath, dpi = 300, bbox_inches = "tight")
            # printing that it has saved
            print(f"\n[INFO] Network visualization with labels is saved as {viz_filepath}")
        else:
            # define filename
            viz_filepath = os.path.join(viz_dir, "network.png")
            # drawing the graph without labels
            nx.draw(G, pos, with_labels=False, node_size = 20, font_size = 10)
            # saving graph
            plt.savefig(viz_filepath, dpi = 300, bbox_inches = "tight")
            # printing that it has saved
            print(f"\n[INFO] Network visualization without labels is saved as {viz_filepath}")
        
        return G
    
    def calc_centrality(self, G):
        '''
        Making an output directory if this doesn't already exists.
        Calculating three measures of centrality (degree, betweenness and eigenvector)
        Saving these in a csv file in the output folder.
        '''
        # Create output directory if it doesn't exist
        outputDir = os.path.join("..", "output")
        create_dir(outputDir)

        # suppling the edges and nodes to the graph from pandas data frame
        #G = nx.from_pandas_edgelist(filtered_df, "nodeA", "nodeB", ["weight"])
        
        # calculate the degree centrality and save as dataframe
        d_metric = nx.degree_centrality(G)
        degree_df = pd.DataFrame(d_metric.items(), columns = ["node", "degree"])
    
        # calculate betweenness centrality and save as dataframe
        bc_metric = nx.betweenness_centrality(G)
        between_df = pd.DataFrame(bc_metric.items(), columns = ["node", "betweenness"])
    
        # calculate eigenvector centrality
        ev_metric = nx.eigenvector_centrality(G)
        eigen_df = pd.DataFrame(ev_metric.items(), columns = ["node", "eigenvector"])
    
        # merging degree and betweenness centrality dataframes
        centrality_df = pd.merge(degree_df, between_df, on='node')
        # merging the eigenvector centrality dataframe to the previously merged dataframe
        centrality_df = pd.merge(centrality_df, eigen_df, on = 'node')
    
    
        # save centrality dataframe in output directory
        df_path = os.path.join(outputDir, "centrality_measures.csv")
        centrality_df.to_csv(df_path, index = False)
        print(f"\n[INFO] Centrality measures are saved as {df_path}")
        
def create_dir(dirName):
    '''
    Create directory if it doesn't exist
    '''
    # if the path does not exist
    if not os.path.exists(dirName):
        # make directory
        os.mkdir(dirName)
        print("\n[INFO] Directory " , dirName ,  " Created ")
    else:   
        # print that it already exists
        print("\n[INFO] Directory " , dirName ,  " already exists")
        
if __name__ == "__main__":
    main(args)
        
        