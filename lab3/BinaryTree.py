class Node:

    def __init__(self, val):
        self.right = None
        self.left = None
        self.val = val
        
    def set_left(self, left):

        self.left = left

        return self

    def set_right(self, right):

        self.right = right

        return self

    def to_string(self):

        if self.left is None:
            left_s = ""
        else:
            left_s = self.left.to_string()

        if self.right is None:
            right_s = ""
        else:
            right_s = self.right.to_string()

        return  "Node (" + left_s + str(self.val)  + right_s + ")"


'''
    def main():  
        t = Tree()
        t.root = Node(4)
        t.root.right = Node(5)
        print t.root.count #this works
        print t.root.right.count #this works too
        t = Tree()
        t.insert(t.root,4)  
        t.insert(t.root,5)
        print t.root.count #this fails
        print t.root.right.count #this fails too

if __name__ == '__main__':
     main()
'''