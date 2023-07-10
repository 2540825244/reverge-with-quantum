result = {'x0': 6.0, 'x1': 1.0, 'x10': 11.0, 'x2': 6.0, 'x3': 5.0, 'x4': 5.0, 'x5': 11.0, 'x6': 1.0, 'x7': 4.0, 'x8': 10.0, 'x9': 7.0}

#put results into a qs
qs = [result['x' + str(i)] for i in range(11)]

print(((qs[0] + qs[1] + qs[4])**2 + (qs[1] + qs[2] + qs[5])**2 + (qs[2] + qs[3] + qs[6])**2 + (qs[4] + qs[7] + qs[8])**2 + (qs[5] + qs[8] + qs[9])**2 + (qs[6] + qs[9] + qs[10])**2)/6 - ((qs[0] + qs[1] + qs[4]) + (qs[1] + qs[2] + qs[5]) + (qs[2] + qs[3] + qs[6]) + (qs[4] + qs[7] + qs[8]) + (qs[5] + qs[8] + qs[9]) + (qs[6] + qs[9] + qs[10]))**2/36)