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
                    variavel = var.split('=')
                    variavel[1] = variavel[1].upper()
                    if not variavel[1] in ['SIM', 'NAO']:
                        print(f"ERRO (regra {i+1}, variavel '{variavel[0]}'): O valor da variável deve ser 'SIM' ou 'NAO'")
                        exit(1)
                    rules[i]['antecedente'][variavel[0]] = variavel[1]
                    
                    if not variavel[0] in variables: 
                        variables.append(variavel[0])

                consequente = regra['consequente'].split('=')
                consequente[1] = consequente[1].upper()
                if not consequente[1] in ['SIM', 'NAO']:
                        print(f"ERRO (regra {i+1}, variavel '{consequente[0]}'): O valor da variável deve ser 'SIM' ou 'NAO'")
                        exit(1)

                rules[i]['consequente'][consequente[0]] = consequente[1]
                
                if not consequente[0] in variables:
                    variables.append(consequente[0])
                i += 1
    except IOError as error:
        raise FileNotFoundError("Pasta não econtrada")


def get_facts(facts:dict, variables:list, folder):
    try:
        with open(f'./{folder}/facts.csv') as facts_file:
            facts_dict = csv.DictReader(facts_file)
            
            i = 0
            for fact in facts_dict:
                variavel = fact['variavel'].split('=')
                variavel[1] = variavel[1].upper()
                if not variavel[1] in ['SIM', 'NAO']:
                    print(f"ERRO (fato {i+1}, variavel '{variavel[0]}'): O valor da variável deve ser 'SIM' ou 'NAO'")
                    exit(1)
                    
                facts[variavel[0]] = variavel[1]
                
                if not variavel[0] in variables: 
                        variables.append(variavel[0])
                i += 1
    except IOError as error:
        raise FileNotFoundError("Pasta não encontrada")


def print_variables(variables:list):
    for var in variables:
        print(f'{var}')
    print()


def print_rules(rules:list):
    for rule in rules:
        vars_ant = list(rule['antecedente'].keys())
        num_vars = len(vars_ant)
        var_cons = list(rule['consequente'].keys())
        for i in range(0, num_vars):
            print(f"{vars_ant[i]}={rule['antecedente'][vars_ant[i]]}", end=' ')
            if i == num_vars-1:
                print('->', end=' ')
            else:
                print('^', end=' ')
        print(f'{var_cons[0]}={rule["consequente"][var_cons[0]]}')


def print_facts(facts:dict):
    for key in facts:
        print(f"{key} = {facts[key]}")