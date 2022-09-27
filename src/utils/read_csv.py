import csv

def get_rules(rules:list, variables:list, folder): 
    try:
        with open(f'./{folder}/rules.csv') as rules_file:
            rules_dict = csv.DictReader(rules_file)
            i = 0

            for regra in rules_dict:
                rules.append({})
                rules[i]['antecedente'] = {}
                rules[i]['consequente'] = {}
                for var in regra['antecedente'].split(' and '):
                    rules[i]['antecedente'][var] = True
                    if var not in variables: 
                        variables.append(var)
                rules[i]['consequente'][regra['consequente']] = True
                if regra['consequente'] not in variables: 
                        variables.append(regra['consequente'])
                i += 1
    except IOError as error:
        raise FileNotFoundError("Pasta não econtrada")


def get_facts(facts:dict, variables:list, folder):
    try:
        with open(f'./{folder}/facts.csv') as facts_file:
            facts_dict = csv.DictReader(facts_file)
            
            for fact in facts_dict:
                facts[fact['variavel']] = True
                if fact['variavel'] not in variables: 
                        variables.append(fact['variavel'])
    except IOError as error:
        raise FileNotFoundError("Pasta não encontrada")