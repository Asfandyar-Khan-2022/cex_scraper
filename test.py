# import json
 
# with open('data.json', 'r') as f:
#     data = json.load(f)

# new_price = 150.0

# for i in data:
#     if ['EE'] in i.values():
#         i['price'].append(new_price)
#         print(i['price'])


thistuple = ("apple", "banana", "cherry")
y = ("orange",)
thistuple += y

print(thistuple)