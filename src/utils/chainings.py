from utils.tree import Node
from collections import deque

class Question:
    def __init__(self, name:str, curr_value:str):
        self.name = name
        self.curr_value = curr_value


def is_in_facts(var:str, facts:dict) -> bool:
        return var in list(facts.keys())


def add_in_facts(node:Node, facts:dict):
    facts[node.name] = node.value


def modus_ponens_facts(root:Node, facts:dict) -> bool:
    # print('\nat modus_ponens_facts')
    # # print(f'root: {root.name}: {root.value} objetivo: {root.goal}')
    # # print(f'facts: {facts}')
    print(f'modus ponens facts with {root.name}')
    if root.name in list(facts.keys()) and facts[root.name] == root.goal:
        print('could do modus ponens')
        root.value = root.goal
    
    return root.value == root.goal


def backward_chaining(root:Node, rules:list, facts:dict):
    
    def look_rules(root:Node, rules):
        for rule in rules:
            consequente = rule.get('consequente')
            if root.name in list(consequente.keys()):
                for antecedente in rule['antecedente']:
                    value = 'SIM' if rule['antecedente'][antecedente] == 'NAO' else 'NAO'
                    root.add_child(Node(antecedente, value, rule['antecedente'][antecedente]))


    def modus_ponens_backward(root:Node, facts) -> bool:
        print(f'modus ponens backward with {root.name}')
        if root.value == root.goal:
            if not is_in_facts(root.name, facts):
                add_in_facts(root, facts)
            return True

        if root.has_children():
            flag = True if root.goal == 'SIM' else False
            for child in root.children:
                if child.value == 'NAO':
                    if root.goal == 'SIM':
                        flag = False
                        break
                    
                    elif root.goal == 'NAO':
                        flag = True
                        break            
            
            if flag:
                root.value = root.goal
                if not is_in_facts(root.name, facts):
                    add_in_facts(root, facts)
            return flag
        else:
            return False


    def verification(root:Node, rules:list, facts:dict):
        if modus_ponens_facts(root, facts):
            return True
        
        if modus_ponens_backward(root, facts):
            return True

        look_rules(root, rules)

    
    def check_children(root:Node, rules:list, facts:dict) -> bool:
        flag:bool = True
        print(f'cheking children of {root.name}')
        
        for child in root.children:
            if not modus_ponens_facts(child, facts):
                flag = False
        
        return flag


    def encadeamento_para_tras(root:Node, rules:list, facts:dict) -> bool:
        if not root: return False
        if root.value == root.goal: return True

        print(f'processaremos {root.name}')
        Stack, rules_copy = nodes_list(root, rules, facts)
        
        print('\nfim do preprocessamento.\nNova lista de regras: ')
        for rule in rules_copy:
            print(rule)
        
        print('\nLista de nós:')
        for obj in Stack:
            print(f'NÓ {obj.name}={obj.value}:')
            obj.print_children()

        preorder_visited = []


        
        #from here, my root has its proprer children

        while Stack:
            top = Stack.pop()
            if check_children(top, rules_copy, facts):
                if modus_ponens_backward(top, facts):
                    return True
            for child in top.children:
                encadeamento_para_tras(child, rules_copy, facts)
        
        return root.value == root.goal


        # while Stack:
        #     top = Stack.pop()
        #     preorder_visited.append(top)

        #     found = verification(top, rules, facts)

        #     if found:
        #         for previous in preorder_visited:
        #             if previous.is_child(top.name): 
        #                 modus_ponens_backward(previous, facts)

        #     for child in top.children:
        #         Stack.append(child)

        # for node in preorder_visited:
        #     print(f'Node: {node.name}. Children: ')
        #     for child in node.children:
        #         print(f"{child.name} = {child.value}")
        #     print()

        # return root.value == root.goal
    
    
    def nodes_list(question:Node, rules:list, facts:dict):
        lista_de_nos = deque([])
        rules_copy = []
        for rule in rules:
            # print(f'consequente: {consequente}')
            if list(rule['consequente'].keys())[0] == question.name:
                question.form_branch(rule['antecedente'])
                lista_de_nos.append(question)
            else:
                rules_copy.append(rule)
        
        return lista_de_nos, rules_copy
        
        

    return encadeamento_para_tras(root, rules, facts)
    


def forward_chaining(root:Node, rules:list, facts:dict):
    
    def modus_ponens_forward(rule:dict, facts:dict) -> bool:
        print("\nat modus_ponens_forward")
        print(f'facts: {facts}')
        print(f'rule: {rule}')
        
        facts_vars = set(facts.keys())
        ant_vars = set(rule['antecedente'].keys())
        
        cons_var = list(rule['consequente'].keys())[0]
        objetivo = rule['consequente'][cons_var]
    
        flag = True

        print(f'objetivo {cons_var}:{objetivo} | flag: {flag}')

        for key in ant_vars:
            if not key in facts_vars:
                return False

            if facts[key] == 'NAO':
                if objetivo == 'NAO':
                    flag = True
                    break
                elif objetivo == 'SIM':
                    flag = False
                    break
        if flag:
            facts[cons_var] = objetivo
            print(f'inserido: {cons_var}: {facts[cons_var]}')
        return flag
        

    def encadeamento_para_frente(root:Node, rules:list, facts:dict):
        i = len(facts)
        rules_copy = rules
        
        #ate nao conseguir add fatos
        while not i > len(facts):
            for rule in rules_copy:
                if modus_ponens_forward(rule, facts):
                    rules_copy.remove(rule)
            
            if modus_ponens_facts(root, facts):
                return True
            i += 1
        return False
    
    return encadeamento_para_frente(root, rules, facts)
