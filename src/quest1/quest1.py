from collections import deque
import sys
import os

# use 'utils' package
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# END use 'utils' package

import utils.read_csv as read_csv
from utils.tree import Node


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


def verification(root:Node, rules:list, facts:dict):
    root.value = look_facts(root, facts)
    
    if root.value:
        return True
    
    if check_root_and_children(root, facts):
        return True

    look_rules(root, rules)


def encadeamento_para_tras(root:Node, rules:list, facts:dict):
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
            if i == num_vars-1:
                print(f'{vars_ant[i]} ->', end='')
            else:
                print(f'{vars_ant[i]} ^', end='')
            print(' ', end='')
        print(f'{var_cons[0]}')


def print_facts(facts):
    for key in list(facts.keys()):
        print(f'{key}: {True}')


def read_facts_from_user(facts:dict, variables):
    print("A base de conhecimento foi deixada vazia. Insira alguns fatos baseado nas variáveis até o momento:")
    print_variables(variables)
    
    n_facts = int(input('Insira o número de fatos: '))
    for i in range(0, n_facts):
        fact = str(input('Fato: '))
        if fact not in variables:
            variables.append(fact)
        facts[fact] = True

def main(argv):
    rules = []
    facts = {}
    variables = []

    try:
        read_csv.get_rules(rules, variables, argv[1])
        read_csv.get_facts(facts, variables, argv[1])
    except Exception as e:
        print(f'ERRO: {e.args[0]}')
        return 

    if len(facts) == 0:
        read_facts_from_user(facts, variables)

    print('-----------------------------')
    print('Regras inseridas: ')
    print_rules(rules)
    print('\nBase de Fatos: ')
    print_facts(facts)
    print('-----------------------------')

    print('Variáveis disponíveis: ' )
    print_variables(variables)

    question = str(input("Faça a sua pergunta: "))
    
    if question not in variables:
        print("ERRO: A variável não se encontra nos fatos nem nas regras")
        return
    
    root_q = Node(question, False)
    ans = encadeamento_para_tras(root_q, rules, facts)
    
    print(question, end=' ')
    if ans:
        print('pode ser inferido a partir das regras e fatos')
    else:
        print('não pode ser inferido a partir das regras e fatos')


if len(sys.argv) <= 1: print("USAGE: python3 ques1.py <pasta_de_exemplo>")
else: main(sys.argv)
