'''
Back to using CQM
'''

from dimod import ConstrainedQuadraticModel, Integer, QuadraticModel, BinaryQuadraticModel
from dimod.generators.constraints import combinations
from dwave.system import LeapHybridCQMSampler
import datetime

qs = [Integer(lower_bound=1, upper_bound=11, label='x' + str(i)) for i in range(11)] #question space
possible_values = range(1, 12)

cqm = ConstrainedQuadraticModel()

cqm.set_objective(((qs[0] + qs[1] + qs[4])**2 + (qs[1] + qs[2] + qs[5])**2 + (qs[2] + qs[3] + qs[6])**2 + (qs[4] + qs[7] + qs[8])**2 + (qs[5] + qs[8] + qs[9])**2/6 + (qs[6] + qs[9] + qs[10])**2)/6 - ((qs[0] + qs[1] + qs[4]) + (qs[1] + qs[2] + qs[5]) + (qs[2] + qs[3] + qs[6]) + (qs[4] + qs[7] + qs[8]) + (qs[5] + qs[8] + qs[9]) + (qs[6] + qs[9] + qs[10]))**2/36 
                  + 0 * ((qs[0] + qs[1] + qs[2] + qs[3] + qs[4] + qs[5] + qs[6] + qs[7] + qs[8] + qs[9] + qs[10])/11-6)**2 
                  + 0 * ((qs[0]**2+qs[1]**2+qs[2]**2+qs[3]**2+qs[4]**2+qs[5]**2+qs[6]**2+qs[7]**2+qs[8]**2+qs[9]**2+qs[10]**2)/11 - (qs[0]+qs[1]+qs[2]+qs[3]+qs[4]+qs[5]+qs[6]+qs[7]+qs[8]+qs[9]+qs[10])**2/121-10)) #just the variance of the sums, simple, also added constraint from comparison as objective

# cqm.add_constraint(qs[0] + qs[1] + qs[4] == qs[1] + qs[2] + qs[5])
# cqm.add_constraint(qs[1] + qs[2] + qs[5] == qs[2] + qs[3] + qs[6])
# cqm.add_constraint(qs[4] + qs[7] + qs[8] == qs[5] + qs[8] + qs[9])
# cqm.add_constraint(qs[5] + qs[8] + qs[9] == qs[6] + qs[9] + qs[10])

#constraint to make sure every variable is unique, using mean and variance
# cqm.add_constraint_from_comparison((qs[0] + qs[1] + qs[2] + qs[3] + qs[4] + qs[5] + qs[6] + qs[7] + qs[8] + qs[9] + qs[10])/11 == 6)
# cqm.add_constraint_from_comparison((qs[0]**2+qs[1]**2+qs[2]**2+qs[3]**2+qs[4]**2+qs[5]**2+qs[6]**2+qs[7]**2+qs[8]**2+qs[9]**2+qs[10]**2)/11 - (qs[0]+qs[1]+qs[2]+qs[3]+qs[4]+qs[5]+qs[6]+qs[7]+qs[8]+qs[9]+qs[10])**2/121 == 10)

#constraint pre-set values
cqm.add_constraint(qs[0] == 6)
cqm.add_constraint(qs[7] == 4)
cqm.add_constraint(qs[10] == 11)

#solve
print("Solving...")
sampler = LeapHybridCQMSampler()
start = datetime.datetime.now()
sampleset = sampler.sample_cqm(cqm)
end = datetime.datetime.now()
print(f"Time used: {end - start}")
print(sampleset.first.sample)
print(sampleset.first.energy)

#store results
results = sampleset.first.sample
f_output = open(f"output.txt", "w")
f_output.write(str(results))