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
        if child.value == root.goal:
            add_in_facts(child.name, facts)


def look_rules(root:Node, rules):
    print("---- IN LOOK RULES ----")
    for rule in rules:
        consequente = rule.get('consequente')
        # print(f"Consequente: {consequente}")
        if root.name in list(consequente.keys()):
            # print("Root found in consequente")
            # print(f"Antecedente acima: {rule['antecedente']} ")
            for antecedente in rule['antecedente']:
                # print(f"Antecedente var: {antecedente} = {rule['antecedente'][antecedente]}")
                value = 'SIM' if rule['antecedente'][antecedente] == 'NAO' else 'NAO'
                root.add_child(Node(antecedente, value, rule['antecedente'][antecedente]))


def look_facts(root:Node, facts):
    print("---- IN LOOK FACTS ----")
    for fact in list(facts.keys()):
        print(f"fact {fact}={facts[fact]} ")
        if fact == root.name and facts[fact] == root.goal:
            root.value = root.goal
            if not is_in_facts(root.name, facts):
                add_in_facts(root.name, facts)

    return root.value == root.goal


def check_root_and_children(root:Node, facts) -> bool:
    if root.value == root.goal:
        if not is_in_facts(root.name, facts):
            add_in_facts(root.name, facts)
        return True

    if root.has_children():
        flag = True
        for child in root.children:
            if root.goal == 'SIM':
                # todos devem ser sim
                if child.value == 'NAO':
                    flag = False
                    break
            
            if root.goal == 'NAO':
                # se pelo menos um for nao
                if child.value == 'NAO':
                    flag = True
                    break            
        
        if flag:
            root.value = root.goal
            if not is_in_facts(root.name, facts):
                add_in_facts(root.name, facts)
        return flag
    else:
        return False


def verification(root:Node, rules:list, facts:dict):
    if look_facts(root, facts):
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

    for node in preorder_visited:
        print(f'Node: {node.name}. Children: ')
        for child in node.children:
            print(f"{child.name} = {child.value}")
        print()

    return root.value == root.goal


def read_facts_from_user(facts:dict, variables):
    print("A base de conhecimento foi deixada vazia. Insira alguns fatos baseado nas variáveis até o momento:")
    read_csv.print_variables(variables)
    
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
    read_csv.print_rules(rules)
    print('\nBase de Fatos: ')
    read_csv.print_facts(facts)
    print('-----------------------------')

    print('Variáveis disponíveis: ' )
    read_csv.print_variables(variables)

    question = str(input("Escolha a variável (<var>=<SIM/NAO>): ")).replace(' ', '').split('=')
    
    while len(question) != 2:
        question = str(input("Entrada inválida. Escolha a variável (<var>=<SIM/NAO>): ")).split('=')
    
    question[1] = question[1].upper()

    if question[1] != 'SIM' and question[1] != 'NAO':
        print("ERRO: O valor da variável deve ser 'SIM' ou 'NAO'")
        return


    if question[0] not in variables:
        print("ERRO: A variável não se encontra nos fatos nem nas regras")
        return
    
    value = 'SIM' if question[1] == 'NAO' else 'NAO'
    root_q = Node(question[0], value, question[1])
    print(f"Raiz: {root_q.name} | valor: {root_q.value} | objetivo: {root_q.goal}")
    ans = encadeamento_para_tras(root_q, rules, facts)
    
    print(f'{question[0]}={question[1]}', end=' ')
    if ans:
        print('pode ser inferido a partir das regras e fatos')
    else:
        print('não pode ser inferido a partir das regras e fatos')


if len(sys.argv) <= 1: print("ERRO: Pasta de exemplos não foi fornecida")
else: main(sys.argv)
