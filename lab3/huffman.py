import math 
import sys
import json
from BinaryTree import Node

def recursive_dfs(tree, code):
    nodes = {}
    if(tree != None):

        if (tree.left is None):
            nodes[ord(tree.val[0])] = code

        else:
            nodes.update(recursive_dfs(tree.left, code + "0"))
            nodes.update(recursive_dfs(tree.right, code + "1"))
            
    return nodes

def main():
    file = open(sys.argv[1], "rb")
    byte_dict = {}
    total = 0

    #Count frequencies
    try:
        byte = file.read(1)
        while byte != "":

            total += 1
            
            if byte_dict.get(byte) is None:
                byte_dict[byte] = 1
            else:
                byte_dict[byte] += 1;
            byte = file.read(1)

    finally:
        file.close()

    byte_list = sorted(byte_dict.items(), key=lambda x: x[1])

    trees = []

    for char, count in byte_list:
        node = Node((char, count))
        trees.append(node)

    #perform Huffman code algorithm by joining Binary Trees together
    while(len(trees) > 1):

    	start_len = len(trees) - 2

        first = trees[0]
        second = trees[1]
        count = second.val[1] + first.val[1]
        val = ("None", count)
        node = Node(val)   

        if second.val[1] > first.val[1]:
            node = node.set_left(first)
            node = node.set_right(second)
        else:
            node = node.set_left(second)
            node = node.set_right(first)

        trees = trees[2:]

        for tree in trees:
            if (tree.val[1] > count):
                ind = trees.index(tree)
                trees.insert(ind, node)
                break

        if (len(trees) == start_len):
        	trees.append(node)

    print len(trees)
    trees[0].to_string()
    codes = recursive_dfs(trees[0], "")

    with open('code.txt', 'wb') as outfile:
        json.dump(codes, outfile)

if __name__ == '__main__':
    main()
