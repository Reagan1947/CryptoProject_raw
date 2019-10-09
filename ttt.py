dict={"a":"apple","b":"banana","o":"orange"}

for i in dict:
    temple = dict[i]
    dict[i] = temple + '1'
print(dict)