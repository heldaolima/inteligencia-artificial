from collections import deque

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
        consequente = rule.get('cons')
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
    print("Nós visitados:")
    for node in preorder_visited:
        print(f"{node.name}: {node.value}")

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
    print(rules)

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

    # root = Node('A', False)

    # ans = encadeamento_para_tras(root, rules, facts)
    # if (ans): 
    #     print(f"Podemos concluir ", end='')
    # else: 
    #     print(f"Não podemos concluir ", end='')
    
    # print(root.name)

main()
