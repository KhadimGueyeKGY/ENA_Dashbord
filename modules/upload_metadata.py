# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:36:03 2023

@author: khadim
"""

import os

query = "https://www.ebi.ac.uk/ebisearch/ws/rest/embl-covid19/download?query=&format=tsv&fields=acc,lineage,cross_references,collection_date,country,center_name,host,TAXON,coverage,phylogeny,who"
size = "&size=10000"

os.system("curl '"+query+"' --output data/meatadata.tsv")
