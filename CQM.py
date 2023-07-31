from dimod import ConstrainedQuadraticModel, Integer, QuadraticModel, BinaryQuadraticModel
from dimod.generators.constraints import combinations
from dwave.system import LeapHybridCQMSampler
import datetime

qs = [Integer(lower_bound=1, upper_bound=11, label='x' + str(i)) for i in range(11)] #question space

cqm = ConstrainedQuadraticModel()

cqm.set_objective(((qs[0] + qs[1] + qs[4])**2 + (qs[1] + qs[2] + qs[5])**2 + (qs[2] + qs[3] + qs[6])**2 + (qs[4] + qs[7] + qs[8])**2 + (qs[5] + qs[8] + qs[9])**2 + (qs[6] + qs[9] + qs[10])**2)/6 - ((qs[0] + qs[1] + qs[4]) + (qs[1] + qs[2] + qs[5]) + (qs[2] + qs[3] + qs[6]) + (qs[4] + qs[7] + qs[8]) + (qs[5] + qs[8] + qs[9]) + (qs[6] + qs[9] + qs[10]))**2/36)

#constraint to make sure every variable is unique, using difference squared greater than 0
for i in range(11):
    for j in range(i+1,11):
        cqm.add_constraint_from_comparison((qs[i]-qs[j])**2>=1, weight=1000)

#constraint pre-set values
cqm.add_constraint(qs[0] == 6)
cqm.add_constraint(qs[7] == 4)
cqm.add_constraint(qs[10] == 11)

#solve
print("Solving...")
sampler = LeapHybridCQMSampler()
start = datetime.datetime.now()
sampleset = sampler.sample_cqm(cqm, label = 'Reverge with Quantum')
feasible_sampleset = sampleset.filter(lambda d: d.is_feasible)
num_feasible = len(feasible_sampleset)
best_samples = \
    feasible_sampleset.truncate(min(10, num_feasible))
end = datetime.datetime.now()
print(f"Time used: {end - start}")

#store results
print(best_samples)
f_output = open(f"output.txt", "w")
f_output.write(str(best_samples))