import sys
arr = eval(sys.argv[1])
for item in arr[1]['data']:
    print(item['emoji'])

print(arr)

