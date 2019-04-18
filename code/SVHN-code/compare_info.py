import json
import sys
f1 = sys.argv[1]
f2 = sys.argv[2]
print("Please make sure you run compare.py first to generate info file")
with open(f1) as fw:
    d1 = json.load(fw)

with open(f2) as fw:
    d2 = json.load(fw)

keys = set()
for k in d1:
    keys.add(k)
for k in d2:
    keys.add(k)

for k in keys:
    exp = None
    id = None
    err1 = None
    err2 = None
    if k in d1:
        id, exp, err1 = d1[k]
    if k in d2:
        id, exp, err2 = d2[k]

    if err1 == None:
        print("+ file 2 found extra error, id {} expected {} found {}".format(id, exp, err2))
    elif err2 == None:
        print("- file 1 found extra error, id {} expected {} found {}".format(id, exp, err1))
    elif err1 != err2:
        print("* both files found different errors, id {} expected {} file 1 found {} file 2 found {}".format(id, exp, err1, err2))



