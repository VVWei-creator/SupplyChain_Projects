import pulp as p

# Create a LP Minimization problem
lp_prod = p.LpProblem('Problem', p.LpMinimize)

#Create Variables
x = p.LpVariable("x",lowBound=0) #lowest boundary is 0 so no negative values involve here
y = p.LpVariable("y",lowBound=0)

#Object Function
lp_prod += 3 * x + 5 * y


#Contraints
lp_prod += 2 * x + 3 * y >= 12
lp_prod += -x + y <= 3
lp_prod += x >= 4
lp_prod += y <= 3

# Display the problem 
print(lp_prod)

# Solver
status = lp_prod.solve()
print(p.LpStatus[status])

# Printing the final solution 
print(p.value(x), p.value(y), p.value(lp_prod.objective)) 

# Optimal
# 6.0 0.0 18.0
# 6 is optimal value for x
# 0.0 is optimal value for y
# 18.0 is the optimised objective function value