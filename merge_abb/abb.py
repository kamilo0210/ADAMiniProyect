class Node:
    def __init__(self, key, data):
        self.key = key      # Tupla (opinión, experticia)
        self.data = data    # Objeto Encuestado
        self.left = None
        self.right = None

class ABB:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        """Inserta un nodo ordenado por key descendiende."""
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            return Node(key, data)
        # Comparación descendente
        if key > node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)
        return node

    def traverse_desc(self):
        """Devuelve lista de data en orden descendente."""
        result = []
        self._reverse_inorder(self.root, result)
        return result

    def _reverse_inorder(self, node, result):
        if not node:
            return
        self._reverse_inorder(node.left, result)
        result.append(node.data)
        self._reverse_inorder(node.right, result)
