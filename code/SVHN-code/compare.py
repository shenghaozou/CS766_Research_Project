import sys
standard = "label.txt"
result = sys.argv[1]
print("standard input: ", standard)
print("compare input: ", result)

d = {}
with open(standard) as fr:
    for line in fr:
        tokens = line.split(' ')
        id = tokens[0]
        d[int(id)] = tokens[1].strip()

total = 0
with open(result) as fr:
    i = 1
    for line in fr:
        tokens = line.split(' ')
        if i not in d:
            print("Can't find id {} in result".format(i))
            continue
        if tokens[1].strip() != d[i]:
            print("id {} expected {} found {}".format(i, d[i], tokens[1].strip()))
        else:
            total += 1
        i += 1

print("ACCURACY: ", total / len(d))
