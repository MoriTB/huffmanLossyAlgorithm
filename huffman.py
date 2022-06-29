from collections import Counter


class NodeTree(object):
    def __init__(self, frequency, symbol=None, left=None, right=None):
        self.left = left
        self.right = right
        self.frequency = frequency
        self.symbol = symbol

    def children(self):
        return self.left, self.right

    def __str__(self):
        return self.left, self.right


def huffman_code_tree(node, binString=''):
    '''
    Function to find Huffman Code
    '''
    print("where are we?")
    if type(node) is int:
        print("we in last state?? are we?")
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d


def make_tree(nodes):
    '''
    Function to make tree
    :param nodes: Nodes
    :return: Root of the tree
    '''
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        #print("here is the key1 and c1 >>>>>", key1, c1)
        (key2, c2) = nodes[-2]
        #print("here is the key2 and c2 >>>>>", key2, c2)
        nodes = nodes[:-2]
        #print(nodes)
        node = NodeTree(c1 + c2, left=key1, right=key2)
        #print("node is >>>>>", node.symbol,node.frequency,node.left,node.right)
        nodes.append((node, c1 + c2))
        #print("nodes after appened >>>>> ", nodes)
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        #print(nodes)
    print("we out")
    print(nodes)
    return nodes[0][0]




if __name__ == '__main__':
    codes = [10, 34, 10, 8, 10, 10, 127, 43, 6, 34, 10, 5, 34, 8, 8]
    freq = dict(Counter(codes))
    nodes = []
    for symbol, frequency in freq.items():
        nodes.append(NodeTree(frequency, symbol))
    nodes = sorted(freq.items(), key=lambda x: x[1],
                   reverse=True)  # reverse sorting (from high freq  ----- > low freq )
    root = make_tree(nodes)
#    print(root)
    encoding = huffman_code_tree(root)
    print(encoding)
    for i in encoding:
        print(f'{i} : {encoding[i]}')
