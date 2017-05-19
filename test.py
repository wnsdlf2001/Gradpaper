listoflists = []

f = open('data/clevedataset.txt')
for line in f:
    inner_list = []
    inner_list += ([elt.strip() for elt in line.split(' ')])
    for lines in range(9):
        x = f.readline()
        inner_list += ([elt.strip() for elt in x.split(' ')])
    listoflists.append(inner_list)

tmp = ' '.join(listoflists[1])
print(tmp)