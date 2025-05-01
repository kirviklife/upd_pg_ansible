import sys

print([0,1,2,3])
arr = eval(sys.argv[1])
for item in arr:
    print('id: %s\tval1: %s\tval2: %s'%(item['id'],item['val1'],item['val2']))