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