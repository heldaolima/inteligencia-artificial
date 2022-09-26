import csv

with open('./ex3/saque.csv') as file:
    saque_dict = csv.DictReader(file)

    for i in saque_dict:
        print(i)