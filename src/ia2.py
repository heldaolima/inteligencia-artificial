from collections import deque

class Node(object):
    def __init__(self, name:str, value:bool) -> None:
        self.name = name 
        self.value = value
        self.children = []


    def print_children(self):
        for child in self.children:
            print(f"{child.name}: {child.value}")


    def has_children(self):
        return len(self.children) > 0


    def add_child(self, obj):
        self.children.append(obj)

    
    def is_child(self, name:str):
        for child in self.children:
            if child.name == name:
                return True
        return False


# util functions from here
def is_in_facts(var:str, facts:dict):
    return var in list(facts.keys())


def add_in_facts(var: str, facts:dict):
    print("adding in facts")
    facts[var] = True


def get_new_facts(root:Node, facts:dict):
    for child in root.children:
        if child.value:
            add_in_facts(facts, child.name)


def look_rules(root:Node, rules):
    for rule in rules:
        consequente = rule.get('cons')
        # print(list(consequente.keys()))
        if root.name in list(consequente.keys()):
            for antecedente in rule.get('ant'):
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

def evaluate_root(root:Node, facts):
    print(f"Evaluate root: {root.name} | {root.value}")
    # root.print_children()
    if root.value:
        if not is_in_facts(root.name, facts):
            print(f"adicionando {root.name} in facts")
            add_in_facts(root.name, facts)
        return True

    # root is true if all its children are
    if root.has_children():
        print("Tem filhos:")
        
        flag = True
        for child in root.children:
            print(f"{child.name}: {child.value}")
            
            if not child.value:
                flag = False
                break
        
        if flag and not is_in_facts(root.name, facts):
            print(f"adicionando {root.name} in facts")
            add_in_facts(root.name, facts)
        root.value = flag
        return flag
    else:
        return False

def verification(root:Node, rules:dict, facts:dict):
    root.value = look_facts(root, facts)
    
    if root.value:
        # print("I was found in facts!")
        return True
    
    if evaluate_root(root, facts):
        # print("My children are bore me!")
        return True

    look_rules(root, rules)


def encadeamento_para_tras(root:Node, rules:dict, facts:dict):
    if not root: return
    
    Stack = deque([root])
    Preorder = []

    while Stack:
        top = Stack.pop()
        Preorder.append(top)

        ans = verification(top, rules, facts)

        if ans:
            # print(f"Top in if: {top.name}")
            for previous in Preorder:
                # print(f"Previous {previous.name}")
                if previous.is_child(top.name):
                    # print("Entrei no evaluate")
                    evaluate_root(previous, facts)
            #dê um jeito de ajustar o pai: evaluate father
            print(facts)

        for child in top.children:
            Stack.append(child)

    return root.value

def main():
    rules = [
        {
            "ant" : {
                "F": True,
                "D": True
            },
            "cons" : {
                "A": True,
            }
        },
        {
            "ant" : {
                "E": True
            },
            "cons" : {
                "B": True,
                "C": True
            }
        },
        {
            "ant" : {
                "G": True
            },
            "cons" : {
                "D": True
            }
        }
    ]

    question = {
        "A": True,
    }

    facts = {
        "G": True,
        "F": True
    }

    objective = {
        'A': False
    }

    root = Node('A', False)
    ans = encadeamento_para_tras(root, rules, facts)
    if (ans): print(f"Podemos concluir ", end='')
    else: print(f"Não podemos concluir ", end='')
    print(root.name)
    root.print_children()

    # tree structure is needed
    # eu preciso manter o controle pais-filhos: tanto registrar direitinho os filhos de um nó quanto os seus valores
    # raiz: Objetivo setado pra falso
    # constrói os filhos e faz modus_ponens
    # retorna quando ou a raiz der verdadeira ou eu tiver exaurido as opções
        

main()