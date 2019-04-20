import sys
import json

standard = "label.txt"
result = sys.argv[1]
print("standard input: ", standard)
print("compare input: ", result)
limit = None
if len(sys.argv) > 2:
    limit = int(sys.argv[2])

d = {}
with open(standard) as fr:
    for line in fr:
        tokens = line.split(' ')
        id = tokens[0]
        d[int(id)] = tokens[1].strip()

total = 0
errorset = {}
with open(result) as fr:
    i = 1
    for line in fr:
        if limit != None and i >= limit:
            break
        tokens = line.split(' ')
        if i not in d:
            print("Can't find id {} in result".format(i))
            continue
        if tokens[2].strip() != d[i]:
            print("id {} expected {} found {}".format(i, d[i], tokens[2].strip()))
            errorset[i] = (i, d[i], tokens[2].strip())
        else:
            total += 1
        i += 1
with open(result + '.info', 'w') as fw:
    json.dump(errorset, fw)
print("ACCURACY: ", total / len(d))
