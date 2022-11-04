from collections import deque
import sys
import os

# use 'utils' package
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# END use 'utils' package

import utils.read_inputs as read_inputs
from utils.tree import Node
from utils.chainings import backward_chaining


def main(argv):
    rules = []
    facts = {}
    variables = []

    try:
        read_inputs.get_rules(rules, variables, argv[1])
        read_inputs.get_facts(facts, variables, argv[1])
    except Exception as e:
        print(f'ERRO: {e.args[0]}')
        return 

    if len(facts) == 0:
        read_inputs.read_facts_from_user(facts, variables)

    print('-----------------------------')
    print('Regras inseridas: ')
    read_inputs.print_rules(rules)
    print('\nBase de Fatos: ')
    read_inputs.print_facts(facts)
    print('-----------------------------')

    print('Variáveis disponíveis: ' )
    read_inputs.print_variables(variables)

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

    #preciso olhar nas regras se a pergunta é consequente em mais de uma
    # e me parece que isso deve ser recursivo, porque não é só com a raiz

    print(f"Raiz: {root_q.name} | valor: {root_q.value} | objetivo: {root_q.goal}")
    ans = backward_chaining(root_q, rules ,facts)
    print('final:')
    print(f'{root_q.name}={root_q.value} | Children: ')
    root_q.print_children()

    # ans = encadeamento_para_tras(root_q, rules, facts)
    
    print(f'{question[0]}={question[1]}', end=' ')
    if ans:
        print('pode ser inferido a partir das regras e fatos')
    else:
        print('não pode ser inferido a partir das regras e fatos')


if len(sys.argv) <= 1: print("ERRO: Pasta de exemplos não foi fornecida")
else: main(sys.argv)
