data = [10,None,20,10,"",30,None,40]

cleaned_list = []
remove_count = 0
seen = {}

for item in data:
    if item is None or item =="":
        remove_count += 1
    elif item not in seen:
        seen[item] = True
        cleaned_list.append(item)
    else:
        remove_count += 1

cleaned_list.sort()

print("Clean List:",cleaned_list)
print("Removed values:",remove_count)