'''
Dev notes:
6 sums all same
all unique
1-11

11 numbers in total
index from 0 to 10 in a list
sums:
014
125
236
478
589
69 10
sum of these must be the same

0 is 6
7 is 4
10 is 11

objective is the variance of the sums

there are 11 position and 11 possible values,
so 121 variables
also 25 sums
so 146 variables
named by p{n}v{m} where n is the position and m is the value
s{sum} for the sum variables
'''

from dimod import ConstrainedQuadraticModel, Integer, QuadraticModel, BinaryQuadraticModel
from dimod.generators.constraints import combinations
from dwave.system import LeapHybridSampler
import datetime

'''
cqm = ConstrainedQuadraticModel()
possible_values = range(1, 12)
qs = [Integer(lower_bound=1, upper_bound=11, label='x' + str(i)) for i in range(11)] #question space
unique_bpm = combinations(possible_values, 1)

cqm.set_objective(((qs[0] + qs[1] + qs[4])**2 + (qs[1] + qs[2] + qs[5])**2 + (qs[2] + qs[3] + qs[6])**2 + (qs[4] + qs[7] + qs[8])**2 + (qs[5] + qs[8] + qs[9])**2 + (qs[6] + qs[9] + qs[10])**2)/6 - ((qs[0] + qs[1] + qs[4]) + (qs[1] + qs[2] + qs[5]) + (qs[2] + qs[3] + qs[6]) + (qs[4] + qs[7] + qs[8]) + (qs[5] + qs[8] + qs[9]) + (qs[6] + qs[9] + qs[10]))**2/36) #just the variance of the sums, simple

cqm.add_constraint()
'''
'''
variable_list = ['x' + str(i) for i in range(11)]
qm = QuadraticModel()
for i in variable_list:
    qm.add_variable(label=i, vartype='INTEGER', upper_bound=11)
'''

#asked chatgpt for this so just trust it, probably ripping off someone else's code with no credit, but still really simple naive algorithm so I got lazy
def find_triplets(lst, target_sum):
    triplets = []
    for i in range(len(lst) - 2):
        for j in range(i + 1, len(lst) - 1):
            for k in range(j + 1, len(lst)):
                if lst[i] + lst[j] + lst[k] == target_sum:
                    triplet = [lst[i], lst[j], lst[k]]
                    triplets.append(triplet)
    return triplets

interactions = [[0, 1, 4], [1, 2, 5], [2, 3, 6], [4, 7, 8], [5, 8, 9], [6, 9, 10]] #list of list of positions that sums must be the same

#initialize BQM with position-value variables
var_list = [f'p{n}v{m}' for n in range(11) for m in range(1, 12)]
print(var_list)
bqm = BinaryQuadraticModel('BINARY')
for i in var_list:
    bqm.add_variable(i, 0)

#add sum variables
for sum in range(6, 31):
    bqm.add_variable(f's{sum}', 0)

#add constraint that each position can only have one value
for pos in range(11):
    one_digit_bqm = combinations([f'p{pos}v{val}' for val in range(1, 12)], 1)
    bqm.update(one_digit_bqm)

#add constraint that each value can only be in one position
for val in range(1, 12):
    one_pos_bqm = combinations([f'p{pos}v{val}' for pos in range(11)], 1)
    bqm.update(one_pos_bqm)
    
#add constraint that there is only one sum
one_sum_bqm = combinations([f's{sum}' for sum in range(6, 31)], 1)

#add constraint that the sum of each 3 adjacent hexagons must be the same WIP
#for this I think I can maybe just correlate a bunch of variables to the sum?
for sum in range(6, 31):
    triplets = find_triplets(range(1, 12), sum) #find all possible triplets that sum to the target sum



#fix known values
bqm.fix_variable('p0v6', 1)
bqm.fix_variable('p7v4', 1)
bqm.fix_variable('p10v11', 1)

print(bqm)
print("Solving...")
sampler = LeapHybridSampler()
sampleset = sampler.sample(bqm, time_limit=180)
print(sampleset)

#store sampleset as file with timestamp
now = datetime.datetime.now()
output_file = open(f'{now}.txt', 'w')
output_file.write(str(sampleset))
output_file.close()