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
from utils.chainings import forward_chaining
from utils.chainings import backward_chaining


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

    ans = False
    method = ''
    
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
    
    if (argv[2] != "-misto"):
        methodDict: dict = {
            "-frente": {
                "method": "encadeamento para frente",
                "ans": forward_chaining(root_q, rules, facts)
            },
            "-tras": {
                "method": "encadeamento para trás",
                "ans": backward_chaining(root_q, rules, facts),
            }
        }
        for method in ["-frente", "-tras"]:
            if (argv[2]) != method: 
                continue

            print(f"'{question[0]}={question[1]}'", end=' ')
            if (methodDict[method]["ans"]): print('pode', end=' ')
            else: print('não pode', end=' ')
            print(f'ser concluído através do método {methodDict[method]["method"]}')
            return

    elif argv[2] == '-misto':
        method = 'misto'
        ans = forward_chaining(root_q, rules, facts)
        if not ans:
            ans = backward_chaining(root_q, rules, facts)    
    
    print(f"'{question[0]}={question[1]}'", end=' ')    
    if ans: print('pode', end=' ')
    else: print('não pode', end=' ')
    print(f'ser concluído através do método {method}')


if len(sys.argv) <= 1: print("ERRO: Pasta de exemplos não foi fornecida.")
elif len(sys.argv) <= 2 or sys.argv[2] not in ['-frente', '-tras','-misto']: 
    print('''ERRO: Método de resolução não fornecido ou inválido.
Métodos válidos:
    '-frente': resolve usando encadeamento para frente
    '-tras': resolve usando encadeamento para trás
    '-misto': resolve usando encademento misto''')

else: main(sys.argv)
