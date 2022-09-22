from collections import deque
import csv

class Node(object):
    def __init__(self, name:str, value:bool) -> None:
        self.name = name 
        self.value = value
        self.children = []


    def print_children(self) -> None:
        for child in self.children:
            print(f"{child.name}: {child.value}")


    def has_children(self) -> bool:
        return len(self.children) > 0


    def add_child(self, obj) -> None:
        self.children.append(obj)

    
    def is_child(self, name:str) -> bool:
        for child in self.children:
            if child.name == name:
                return True
        return False


# util functions from here
def is_in_facts(var:str, facts:dict) -> bool:
    return var in list(facts.keys())


def add_in_facts(var: str, facts:dict):
    facts[var] = True


def get_new_facts(root:Node, facts:dict):
    for child in root.children:
        if child.value:
            add_in_facts(facts, child.name)


def look_rules(root:Node, rules):
    for rule in rules:
        consequente = rule.get('consequente')
        if root.name in list(consequente.keys()):
            for antecedente in rule.get('antecedente'):
                child = Node(antecedente, False)
                root.add_child(child)


def look_facts(root:Node, facts):
    for fact in list(facts.keys()):
        if fact == root.name and facts[fact]:
            root.value = True
            
            if not is_in_facts(root.name, facts):
                add_in_facts(root.name, facts)
            return True
    
    return False

def check_root_and_children(root:Node, facts) -> bool:
    if root.value:
        if not is_in_facts(root.name, facts):
            add_in_facts(root.name, facts)
        return True

    if root.has_children():
        flag = True
        for child in root.children:        
            if not child.value:
                flag = False
                break

        if flag and not is_in_facts(root.name, facts):
            add_in_facts(root.name, facts)
        root.value = flag
        return flag
    else:
        return False

def verification(root:Node, rules:dict, facts:dict):
    root.value = look_facts(root, facts)
    
    if root.value:
        return True
    
    if check_root_and_children(root, facts):
        return True

    look_rules(root, rules)


def encadeamento_para_tras(root:Node, rules:dict, facts:dict):
    if not root: return
    
    Stack = deque([root])
    preorder_visited = []

    while Stack:
        top = Stack.pop()
        preorder_visited.append(top)

        found = verification(top, rules, facts)

        if found:
            for previous in preorder_visited:
                if previous.is_child(top.name): 
                    check_root_and_children(previous, facts)

        for child in top.children:
            Stack.append(child)

    return root.value



def get_rules(rules:list, variables:list): 
    with open('rules.csv') as rules_file:
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
            for var in regra['consequente']:
                rules[i]['consequente'][var] = True
                if var not in variables: 
                    variables.append(var)
            i += 1


def get_facts(facts:dict, variables:list):
    with open('facts.csv') as facts_file:
        facts_dict = csv.DictReader(facts_file)
        
        for fact in facts_dict:
            facts[fact['variavel']] = True
            if fact['variavel'] not in variables: 
                    variables.append(fact['variavel'])

def print_rules(rules:list):
    for rule in rules:
        vars_ant = list(rule['antecedente'].keys())
        num_vars = len(vars_ant)
        var_cons = list(rule['consequente'].keys())

        for i in range(0, num_vars):
            if i == num_vars-1:
                print(f'{vars_ant[i]} ->', end='')
            else:
                print(f'{vars_ant[i]} ^', end='')
            print(' ', end='')
        print(f'{var_cons[0]}')


def print_facts(facts):
    for key in list(facts.keys()):
        print(f'{key}: {True}')


def main():
    rules = []
    facts = {}
    variables = []

    get_rules(rules, variables)
    get_facts(facts, variables)
    
    print('-----------------------------')
    print('Regras inseridas: ')
    print_rules(rules)
    print('\nBase de Fatos: ')
    print_facts(facts)
    print('-----------------------------')

    print('Variáveis disponíveis: ', end='')
    for var in variables:
        print(f'{var} ', end='')
    print()

    question = str(input("Faça a sua pergunta: ")).upper()
    root_q = Node(question, False)
    ans = encadeamento_para_tras(root_q, rules, facts)
    
    if ans:
        print('Found')
    else:
        print('not found')
    # num_rules = int(input("Insira a quantidade de regras: "))
    
    # for i in range(0, num_rules):
    #     print(f"Regra {i+1}")
    #     rules.append({})
        
    #     print("Atencedente:")
    #     while (True):
    #         var = str(input("Variável: ")).upper()
            
    #         rules[i]['antecedente'][var] = True
    #         conj = str(input("Conjução? [S/N]")).upper()
    #         if conj == 'N': break
        
    #     print("Consequente:")
    #     var = str(input("Variável: ")).upper()
    #     rules[i]['consequente'] = {var: True}
    
    # print(rules)

    # num_facts = int(input("Insira a quantidade de fatos: "))
    # for i in range(0, num_facts):
    #     var = str(input("Insira o fato: ")).upper()
    #     facts[var] = True

    # root_var = str(input("Faça a sua pergunta: ")).upper()
    
    # root = Node(root_var, False)

    
    # if (ans): 
    #     print(f"Podemos concluir ", end='')
    # else: 
    #     print(f"Não podemos concluir ", end='')
    
    # print(root.name)

main()
