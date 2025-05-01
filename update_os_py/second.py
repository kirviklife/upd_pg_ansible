import sys
arr = eval(sys.argv[1])
for item in arr[1]:
    print('id: %s\tval1: %s\tval2: %s'%(item['id'],item['val1'],item['val2']))

print(arr)

