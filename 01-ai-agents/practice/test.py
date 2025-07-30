names = ["nasir", "ahmed", "affan", "affan", "test"]
names_count = {}

for name in names:
    if names_count.get(name) == 1:
        names_count[name] += 1

    else:
        names_count[name] = 1
        names_count[name] = {}

for n in names_count:
    for char in n:
        if char not in names_count[n]: 
            names_count[n][char] = 1
        else:
            names_count[n][char] += 1

print(names_count)

