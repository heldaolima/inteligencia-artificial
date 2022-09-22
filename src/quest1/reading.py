import csv

with open('rules.csv') as rules:
    reader = csv.DictReader(rules)
    for row in reader:
        print(f"{row['antecedente']} | {row['consequente']}")

with open('facts.csv') as facts:
    r_facts = csv.DictReader(facts, delimiter=',')
    for row in r_facts:
        print(f'{row["variavel"]}: TRUE')