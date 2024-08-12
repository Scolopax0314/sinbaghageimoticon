import pandas as pd

with open('images/imginf.txt', 'r') as file:
    lines = file.readlines()

results = []
for line in lines:
    numbers = [int(x) for x in line.replace(',', ' ').split() if x.isdigit()]
    if len(numbers) == 2:
        results.append(tuple(numbers)) 
    elif len(numbers) == 1:
        results.append(numbers[0])  

print(results)
