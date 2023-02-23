""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, with edits by Jackson Goerner'
__docformat__ = 'reStructuredText'


from bst import BinarySearchTree
from typing import TypeVar, Generic, List
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)
        self.count = 0

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            best and worst case: O(log(N)), N is the number of nodes in the tree
        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1

        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
            current.size += 1
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            current.size += 1
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')

        if self.is_leaf(current):
            pass
        elif current.left is None:
            current.height = 1 + self.get_height(current.right) #current.right.height
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

        current = self.rebalance(current)
        return current

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
            worst case: O(D * D), D is the depth of the tree
            best case: O(D), when successor is None
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
            current.size -= 1
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
            current.size -= 1
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)      # O(D)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        if self.is_leaf(current):
            pass
        elif current.left is None:
            current.height = 1 + self.get_height(current.right)
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        
        
        current = self.rebalance(current)
        return current

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """

        child = current.right
        
        current.right = child.left     
        child.left = current

        
        if self.is_leaf(current):
            current.height = 1
            current.size = 1
        elif current.left is None:
            current.height = 1 + self.get_height(current.right)
            current.size = 1 + current.right.size
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
            current.size = 1 + current.left.size
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
            current.size = current.left.size + current.right.size + 1

        if self.is_leaf(child):
            child.height = 1
            child.size = 1
        elif child.left is None:
            child.height = 1 + self.get_height(child.right)
            child.size = 1 + child.right.size
        elif child.right is None:
            child.height = 1 + self.get_height(child.left)
            child.size = 1 + child.left.size
        else:
            child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))
            child.size = child.left.size + child.right.size + 1


        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        child = current.left
        
        current.left = child.right     # do current.left is equal to centre
        child.right = current
        
        #Only do this if current.left and current.right is not None
        if self.is_leaf(current):
            current.height = 1
            current.size = 1
        elif current.left is None:
            current.height = 1 + self.get_height(current.right)
            current.size = 1 + current.right.size
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
            current.size = 1 + current.left.size
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
            current.size = current.left.size + current.right.size + 1

        if self.is_leaf(child):
            child.height = 1
            child.size = 1
        elif child.left is None:
            child.height = 1 + self.get_height(child.right)
            child.size = 1 + child.right.size
        elif child.right is None:
            child.height = 1 + self.get_height(child.left)
            child.size = 1 + child.left.size
        else:
            child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))
            child.size = child.left.size + child.right.size + 1

        return child


    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def range_between(self, i: int, j: int) -> List:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive.
        
        :worst case complexity O(j - i + log(N))
        best case: O(log(N))
        """
        return self.range_between_aux(self.root, i, j, [], j-i)
    
    def range_between_aux(self, current: AVLTreeNode, i, j, elements: list[K], difference):
        '''
        Recursive function for finding the nodes from range_between function. 
        This uses the idea of giving each node a size variable which is the size of all childern nodes + 1(the node itself).
        :complexity O(j - i + log(N))
        best case: O(log(N))
        '''
        self.count = 0
        if current is None:
            return elements
        
        if current.left is None:
            a = 0
        else:
            a = current.left.size

        if i == a + 1:
            if self.count <= difference:
                if current.right is not None:
                    self.inorder_aux(current.right, elements, difference)
                    return elements
                else:
                    return elements

        
        if i < a + 1:
            self.range_between_aux(current.left, i, j, elements, difference)
            if self.count <= difference:
                elements.append(current.item)
                self.count += 1
            if self.count <= difference:
                if current.right is not None:
                    self.inorder_aux(current.right, elements, difference)
                    return elements
                else:
                    return elements

        if i > a + 1:
            self.range_between_aux(current.right, i - a - 1, j, elements, difference)
            return elements

        return elements


    def inorder_aux(self, current, elements, difference) -> None:
        """
        Actual in-order traversal of the tree
        :complexity: O(N) where N is number of nodes in the tree
        """
        if current is not None and self.count <= difference:  # if not a base case
            self.inorder_aux(current.left, elements, difference)
            if self.count <= difference:
                elements.append(current.item)
                self.count += 1
            self.inorder_aux(current.right, elements, difference)
        


class AVLTreeCave(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)
        self.count = 0

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            best and worst case: O(log(N)), N is the number of nodes in the tree
        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1

        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
            current.size += 1
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            current.size += 1
        else:  # key == current.key
            temp_lst =[]        # if they have same mining rate, adds it to a list
            if type(current.item) != list:
                temp_lst.append(current.item)
            else:
                for i in current.item:
                    temp_lst.append(i)
            temp_lst.append(item)
            current.item = temp_lst

        if self.is_leaf(current):
            pass
        elif current.left is None:
            current.height = 1 + self.get_height(current.right) #current.right.height
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

        current = self.rebalance(current)
        return current

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
            worst case: O(D * D), D is the depth of the tree
            best case: O(D), when successor is None
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
            current.size -= 1
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
            current.size -= 1
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        if self.is_leaf(current):
            pass
        elif current.left is None:
            current.height = 1 + self.get_height(current.right)
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        
        
        current = self.rebalance(current)
        return current

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """

        child = current.right
        
        current.right = child.left     # do current.left is equal to centre
        child.left = current
        
        if self.is_leaf(current):
            current.height = 1
            current.size = 1
        elif current.left is None:
            current.height = 1 + self.get_height(current.right)
            current.size = 1 + current.right.size
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
            current.size = 1 + current.left.size
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
            current.size = current.left.size + current.right.size + 1

        if self.is_leaf(child):
            child.height = 1
            child.size = 1
        elif child.left is None:
            child.height = 1 + self.get_height(child.right)
            child.size = 1 + child.right.size
        elif child.right is None:
            child.height = 1 + self.get_height(child.left)
            child.size = 1 + child.left.size
        else:
            child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))
            child.size = child.left.size + child.right.size + 1


        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        child = current.left
        
        current.left = child.right     # do current.left is equal to centre
        child.right = current
        
        #Only do this if current.left and current.right is not None
        if self.is_leaf(current):
            current.height = 1
            current.size = 1
        elif current.left is None:
            current.height = 1 + self.get_height(current.right)
            current.size = 1 + current.right.size
        elif current.right is None:
            current.height = 1 + self.get_height(current.left)
            current.size = 1 + current.left.size
        else:
            current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
            current.size = current.left.size + current.right.size + 1

        if self.is_leaf(child):
            child.height = 1
            child.size = 1
        elif child.left is None:
            child.height = 1 + self.get_height(child.right)
            child.size = 1 + child.right.size
        elif child.right is None:
            child.height = 1 + self.get_height(child.left)
            child.size = 1 + child.left.size
        else:
            child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))
            child.size = child.left.size + child.right.size + 1

        return child


    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def range_between(self, i: int, j: int) -> List:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive.
        
        :complexity O(j - i + log(N))
        """
        return self.range_between_aux(self.root, i, j, [], j-i)
    
    def range_between_aux(self, current: AVLTreeNode, i, j, elements: list[K], difference):
        self.count = 0
        if current is None:
            return elements
        
        if current.left is None:
            a = 0
        else:
            a = current.left.size

        if i == a + 1:
            if self.count <= difference:
                if current.right is not None:
                    self.inorder_aux(current.right, elements, difference)
                    return elements
                else:
                    return elements

        
        if i < a + 1:
            self.range_between_aux(current.left, i, j, elements, difference)
            if self.count <= difference:
                elements.append(current.item)
                self.count += 1
            if self.count <= difference:
                if current.right is not None:
                    self.inorder_aux(current.right, elements, difference)
                    return elements
                else:
                    return elements

        if i > a + 1:
            self.range_between_aux(current.right, i - a - 1, j, elements, difference)
            return elements

        return elements


    def inorder_aux(self, current, elements, difference) -> None:
        """
        Actual in-order traversal of the tree
        :complexity: O(N) where N is number of nodes in the tree
        """
        if current is not None and self.count <= difference:  # if not a base case
            self.inorder_aux(current.left, elements, difference)
            if self.count <= difference:
                elements.append(current.item)
                self.count += 1
            self.inorder_aux(current.right, elements, difference)