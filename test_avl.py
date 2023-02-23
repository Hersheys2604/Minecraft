from avl import AVLTree
from node import TreeNode, AVLTreeNode
import math
import random
import unittest

__author__ = "Saksham Nagpal"


class TestAVL(unittest.TestCase):
    """ Testing additional AVL functionality. """

    def setUp(self):
        self.successor = {}
        self.height = {} 

    def check_invariant(self, current: AVLTreeNode) -> bool:
        if current is not None and current.left is not None:
            # checking the invariant
            self.assertGreater(current.key, current.left.key, 'Invariant does not hold for node {0} as current.key = {1} while current.left.key = {2}'.format(current, current.key, current.left.key))
            # calling for left child
            self.check_invariant(current.left)

        if current is not None and current.right is not None:
            self.assertLess(current.key, current.right.key, 'Invariant does not hold for node {0} as current.key = {1} while current.right.key = {2}'.format(current, current.key, current.right.key))
            # calling for right child
            self.check_invariant(current.right)

        return True

    def testInvariant(self):
        numbers = list(range(1, 100))
        for attempt in range(10):
            with self.subTest(attempt):
                random.shuffle(numbers)

                tree = AVLTree()
                self.setUp()  # clearning the cache
                length = random.randint(10, 100)
                for num in numbers[:length]:
                    tree[num] = num
                # print(f"balance:   {self.get_height(tree.root.right) - self.get_height(tree.root.left)}")
                self.assertTrue(self.check_invariant(tree.root), 'The invariant does not hold!')

    def testDelete(self):
        numbers = list(range(1, 100))
        for attempt in range(10):
            with self.subTest(attempt):
                random.shuffle(numbers)

                tree = AVLTree()
                self.setUp()  # clearning the cache
                length = random.randint(10, 100)
                sorted_array = []
                for num in numbers[:length]:
                    tree[num] = num
                    sorted_array.append(num)

                to_delete = numbers[:(length // 2)]
                random.shuffle(to_delete)
                for n in to_delete:
                    del tree[n]
                # print(f"balance:   {self.get_height(tree.root.right) - self.get_height(tree.root.left)}")
                self.assertTrue(self.check_invariant(tree.root), 'The invariant does not hold after node deletion!')

    def testInOrder(self):
        numbers = list(range(1, 100))
        for attempt in range(10):
            with self.subTest(attempt):
                random.shuffle(numbers)

                tree = AVLTree()
                self.setUp()  # clearning the cache
                length = random.randint(10, 100)
                sorted_array = []
                for num in numbers[:length]:
                    tree[num] = num
                    sorted_array.append(num)
                # print(f"balance:   {self.get_height(tree.root.right) - self.get_height(tree.root.left)}")
                sorted_array.sort()  # creating a properly sorted array
                array = [key for key in tree]  # using out treesort

                self.assertEqual(array, sorted_array, 'In-Order traversal produces a wrong order: {0}'.format(array))

    def get_height(self, current: AVLTreeNode) -> int:
        if current is None:
            return 0

        # caching the height
        if current not in self.height:
            self.height[current] = 1 + max(self.get_height(current.left), self.get_height(current.right))

        return self.height[current]

    def check_balance(self, current: AVLTreeNode) -> bool:
        if current is not None:
            bfactor = self.get_height(current.right) - self.get_height(current.left)
            self.assertTrue(bfactor in (-1, 0, 1), 'Balance factor is wrong for key node ({0}, {1})'.format(current.key, current.item))

        return True

    def testHeight(self):
        numbers = list(range(1, 500))
        for attempt in range(10):
            random.shuffle(numbers)

            tree = AVLTree()
            self.height = {}  # clearing the cache
            length = random.randint(10, 500)
            for num in numbers[:length]:
                tree[num] = num

            # correct bounds for an AVL tree height:
            lb = math.log2(length + 1) - 1
            ub = 1.440420 * math.log2(length + 2) - 0.3277
            # print(f"lb:    {lb}")
            # print(f"ub:    {ub}")
            # print(self.get_height(tree.root))
            # print(tree.str(tree.root))
            self.assertTrue(lb <= self.get_height(tree.root) < ub, 'Wrong height for an AVL tree with {0} nodes! Make sure the tree is balanced.'.format(length))

    def testBalance(self):
        numbers = list(range(1, 100))
        for attempt in range(10):
            random.shuffle(numbers)

            tree = AVLTree()
            self.height = {}  # clearing the cache
            length = random.randint(10, 100)
            for num in numbers[:length]:
                tree[num] = num
            # print(f"root node: {tree.root}")
            # print(f"balance:   {self.get_height(tree.root.right) - self.get_height(tree.root.left)}")
            self.assertTrue(self.check_balance(tree.root), 'The tree is unbalanced!')

    def test_range_between(self):
        random.seed(16)
        numbers = list(range(1, 100))
        tree = AVLTree()
        length = random.randint(10, 100)
        for num in numbers[:length]:
            tree[num] = num

        self.assertEqual(tree.range_between(1, 5), [2, 3, 4, 5, 6], "Range between failed")


if __name__ == '__main__':
    # seeding the pseudo-random generator
    random.seed(16)

    # running all the tests
    unittest.main()
