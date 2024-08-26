import pandas as pd

demand = pd.read_excel("/Users/veraph/Desktop/Supply Chain Projects/Supply Chain Optimization/demand.xlsx",index_col=0)

loca = ['USA', 'Germany', 'Japan', 'Brazil', 'India']

print(demand)

print(demand.loc['USA','Demand'])

