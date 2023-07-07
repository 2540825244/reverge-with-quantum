from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler
import datetime

# Define the variables
variables = ['x' + str(i) for i in range(11)]
num_variables = len(variables)

# Create the BinaryQuadraticModel (QUBO)
qubo = BinaryQuadraticModel('BINARY')

# Add variables to the QUBO
for var in variables:
    qubo.add_variable(var)

# Set the objective function (variance of the sums)
qubo.set_objective(
    (qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x0', 'x1', 'x4']]) ** 2 +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x1', 'x2', 'x5']]) ** 2 +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x2', 'x3', 'x6']]) ** 2 +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x4', 'x7', 'x8']]) ** 2 +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x5', 'x8', 'x9']]) ** 2 / 6 +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x6', 'x9', 'x10']]) ** 2) / 6 -
    (qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x0', 'x1', 'x4']]) +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x1', 'x2', 'x5']]) +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x2', 'x3', 'x6']]) +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x4', 'x7', 'x8']]) +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x5', 'x8', 'x9']]) +
     qubo.sum([(qubo.get_variable(v) if v in variables else 0) for v in ['x6', 'x9', 'x10']])) ** 2 / 36
)

# Set the constraints

# Constraint: Ensure every variable is unique
for i in range(num_variables - 1):
    for j in range(i + 1, num_variables):
        qubo.add_constraint(variables[i] + ' + ' + variables[j] + ' <= 1')

# Solve the QUBO
print("Solving...")
sampler = LeapHybridSampler()
start = datetime.datetime.now()
sampleset = sampler.sample_qubo(qubo, num_reads=10)
end = datetime.datetime.now()
print(f"Time used: {end - start}")
print(sampleset.first.sample)
print(sampleset.first.energy)

# Store results
results = sampleset.first.sample
f_output = open("output.txt", "w")
f_output.write(str(results))
