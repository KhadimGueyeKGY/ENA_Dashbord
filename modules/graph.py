# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 09:59:03 2023

@author: khadim
"""


import plotly.express as px
import plotly.graph_objects as go


class Graph:
    def __init__(self):
        init = 0 
        
    def pie(self,data,names):
        nm = list(data[names].unique())
        val = []
        for i in nm:
            val.append(list(data[names]).count(i))
        pull_val = []
        for i in val:
            if int(i)/sum(val) > 0.01:
                pull_val.append(0)
            else:
                pull_val.append(0.2)
        fig = go.Figure(data=[go.Pie(labels=nm, values=val, pull=pull_val)])
        fig.update_layout(
            autosize=False,
            width=650,
            height=650,)
        return fig 
        
        
        
