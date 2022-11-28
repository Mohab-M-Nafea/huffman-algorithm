
class Node:
    def __init__(self, c, f, right=None, left=None):
        self.right = right
        self.left = left
        self.freq = f
        self.ch = c


def node(text):
    nodes = [Node(ch, text.count(ch)) for ch in list(set(text))]

    return nodes


def tree(nodes):
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda index: index.freq)

        left = nodes.pop(0)
        right = nodes.pop(0)

        total = left.freq + right.freq
        nodes.append(Node(None, total, right, left))

    return nodes[0]


def encode(root, code, huffman_code):
    if root is None:
        return

    if root.left is None and root.right is None:
        huffman_code[root.ch] = code if len(code) > 0 else "0"

    encode(root.left, code + "0", huffman_code)
    encode(root.right, code + "1", huffman_code)
