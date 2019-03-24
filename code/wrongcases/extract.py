
with open('result.txt','r') as fr:
    for line in fr:
        tokens = line.replace('\n','').split('\t')
        if tokens[1] != tokens[2]:
            print("ID: {}, prediction: {}, label: {}".format(tokens[0], tokens[1], tokens[2]))
