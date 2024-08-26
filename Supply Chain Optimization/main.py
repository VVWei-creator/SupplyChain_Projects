# Design Supply Chain Network with Python - https://towardsdatascience.com/supply-chain-optimization-with-python-23ae9b28fd0b
# Aims : to redefine the supply chain network for the next 5 years by considering the recent increase in shipping costs and the forecasts of customers' need

# Current Network:
# 5 markets - Brazil,USA,India,Japan,Germany
# 2 types of munifacturing facilities - low capacity, high capacity 
# shipping costs ($/container)
# customer's demand (units/year)

# Manufacturing facilities fixed costs (depands on markets & facility types):
# Capital Expenditure for Equipments (Machines, Storages...)
# Utilities (Electricity, Water...)
# Factory management, administractive staff
# Space Rental

# Production Variable Costs
# Production lines operators 
# Raw materials 

# Shipping Variable Costs
# Cost per container ($/Container)
# Assumption: 1 container can contain 1000 units

# Manufacturing Capacity by Site (Units/Month)

# Cutomers' demand per market (Units/Month)

################################################################
import pandas as pd 
from pulp import *

#import Production Variable Costs ($/Unit)
manvar_costs = pd.read_excel('/Users/veraph/Desktop/Supply Chain Projects/Supply Chain Optimization/variable_costs.xlsx',index_col=0)

#import Shipping Variable Costs ($/Container)(1000 Units/Container)
freight_costs = pd.read_excel('/Users/veraph/Desktop/Supply Chain Projects/Supply Chain Optimization/freight_costs.xlsx',index_col=0)

#calculate Overall Variable Costs
var_costs = freight_costs/1000 + manvar_costs 

#import Fixed Costs 
fixed_costs = pd.read_excel('/Users/veraph/Desktop/Supply Chain Projects/Supply Chain Optimization/fixed_cost.xlsx',index_col=0)

# import plants capacity
cap = pd.read_excel('/Users/veraph/Desktop/Supply Chain Projects/Supply Chain Optimization/capacity.xlsx',index_col=0)

# import customer demand (units/month)
demand = pd.read_excel('/Users/veraph/Desktop/Supply Chain Projects/Supply Chain Optimization/demand.xlsx',index_col=0)

# Market locaation 
loca = ['USA', 'Germany', 'Japan', 'Brazil', 'India'] #the tutorial code name this as loc which conflicts with the dataframe loc methods
type = ['Low', 'High']

# Model
model = LpProblem("Capacitated Plant location Model",LpMinimize) #Linear Optimization, in the case we want to minimize the cost so we choose LpMinimize here

# Create Variables 
x = LpVariable.dicts("production_",[(i,j) for i in loca for j in loca],lowBound=0,upBound=None,cat='continuous')
y = LpVariable.dicts("plant_",[(i,t) for t in type for i in loca],cat='Binary')
#print(x)

# Define Object Function 
model += (lpSum([fixed_costs.loc[i,s] * y[(i,s)] * 1000 for s in type for i in loca])
          + lpSum([var_costs.loc[i,j] * x[(i,j)]   for i in loca for j in loca]))

# Defind Contraints
for j in loca:
    model += lpSum([x[(i, j)] for i in loca]) == demand.loc[j,'Demand']
for i in loca:
    model += lpSum([x[(i, j)] for j in loca]) <= lpSum([cap.loc[i,s]*y[(i,s)] * 1000
                                                       for s in type])

# Solve Model
model.solve()
print("Total Costs = {:,} ($/Month)",format(int(value(model.objective))))
print('\n' + "Status: {}".format(LpStatus[model.status]))

# Analysis Output
dict_plant = {}
dict_prod = {}
for v in model.variables():
    if 'plant' in v.name:
        name = v.name.replace('plant__', '').replace('_', '')
        dict_plant[name] = int(v.varValue)
        p_name = name
    else:
        name = v.name.replace('production__', '').replace('_', '')
        dict_prod[name] = v.varValue
    print(name, "=", v.varValue)