'''
Instead of counting with sticks (forgot the exact terminology for that number system), let's use binary
each position would have 4 bits
labels in the format p{position}b{bit}, position is 1-11, bit is 0-3
and for the sum just full add the interactions and clamp them together!

interactions:
125
236
347
589
69 10
7 10 11
'''

from dimod import ConstrainedQuadraticModel, Integer, QuadraticModel, BinaryQuadraticModel
from dimod.generators.constraints import combinations
from dwave.system import LeapHybridSampler
import datetime

var_list = [f'p{n}b{m}' for n in range(1, 12) for m in range(4)]
print(var_list)
bqm = BinaryQuadraticModel('BINARY')
for i in var_list:
    bqm.add_variable(i, 0)

#add constraint that each position can only have one value
for pos in range(1, 12):
