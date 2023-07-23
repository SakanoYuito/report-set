from typing import Any, Optional, Iterable
from random import random


class Node:
    def __init__(self, val, key: Any):
        self.val = val
        self.key: Any = key                  # 値
        self.child: list[Optional[Node]] = [None, None]  # [左の子, 右の子]
        self.priority: float = random()      # 優先度
        self.size: int = 1                   # 部分木のサイズ
        self.sum: int = key                  # 部分木の値の和

    def update(self):
        siz_child = [0, 0]
        sum_child = [0, 0]

        for i in (0, 1):
            if self.child[i] != None:
                siz_child[i] = self.child[i].size
                sum_child[i] = self.child[i].sum

        self.size = sum(siz_child) + 1
        self.sum = sum(sum_child) + self.key

        return self


class Treap:
    def size(t: Optional[Node]):
        if t == None:
            return 0
        else:
            return t.size

    def sum(t: Optional[Node]):
        if t == None:
            return 0
        else:
            return t.sum

    def __init__(self):
        self.root: Optional[Node] = None

    def __str__(self) -> str:
        if self.root == None:
            return '{}'
        items = []
        stack = [self.root]
        while len(stack) > 0:
            p = stack.pop()
            items.append(p.val)
            for c in p.child:
                if c != None:
                    stack.append(c)
        res = '{' + ", ".join(map(str, items)) + '}'
        return res

    def _rotate(root: Optional[Node], b):
        s = root.child[1-b]
        root.child[1-b] = s.child[b]
        s.child[b] = root
        root.update()
        s.update()
        return s

    def _insert(root: Optional[Node], val):
        key = hash(str(val))
        if root == None:
            return Node(val, key)

        if key == root.key:
            return root
        b = int(key < root.key)
        root.child[1-b] = Treap._insert(root.child[1-b], val)
        if root.priority > root.child[1-b].priority:
            root = Treap._rotate(root, b)

        return root

    def _erase(root: Optional[Node], key):
        if root == None:
            return None

        if key != root.key:
            b = int(key < root.key)
            root.child[1-b] = Treap._erase(root.child[1-b], key)
        else:
            if (root.child[0] == None or root.child[1] == None):
                root = root.child[0] if root.child[0] != None else root.child[1]
            else:
                b = int(root.child[0].priority < root.child[1].priority)
                root = Treap._rotate(root, 1-b)
                root.child[1-b] = Treap._erase(root.child[1-b], key)
        return root

    def _find(root: Optional[Node], val):
        key = hash(str(val))
        if root == None:
            return False
        if val == root.val:
            return True
        else:
            return Treap._find(root.child[root.key < key], val)

    def insert(self, key):
        self.root = Treap._insert(self.root, key)
        return self

    def erase(self, key):
        self.root = Treap._erase(self.root, key)
        return self

    def find(self, key):
        return Treap._find(self.root, key)

    def items(self):
        if self.root == None:
            return []
        items = []
        stack = [self.root]
        while len(stack) > 0:
            p = stack.pop()
            items.append(p.val)
            for c in p.child:
                if c != None:
                    stack.append(c)
        return items


class Set(Treap):
    def __init__(self, l: Iterable[Any] = []):
        super().__init__()

        for val in l:
            self.insert(val)

    def copy(self):
        return Set(self.items())

    def __add__(self, other):
        res = Set()
        for item in self.items():
            res.insert((item, 0))
        for item in other.items():
            res.insert((item, 1))
        return res

    def __or__(self, other):
        res = self.copy()
        for item in other.items():
            res.insert(item)
        return res

    def __sub__(self, other):
        res = self.copy()
        for item in other.items():
            res.erase(item)
        return res

    def __mul__(self, other):
        res = Set()
        for p in self.items():
            for q in other.items():
                res.insert((p, q))
        return res

    def __and__(self, other):
        res = self.copy()
        res = res - (self - other)
        return res

    def __rpow__(self, left):
        if left != 2:
            raise ValueError("err")
        if self.root == None:
            return Set()

        res = Set()
        items = self.items()
        n = len(items)

        for bit in range(2**n):
            s = Set()
            for i in range(n):
                if ((bit >> i) & 1):
                    s.insert(items[i])
            res.insert(s)

        return res

    def __contains__(self, other):
        return self.find(other)

    def __le__(self, other):
        left = self.items()
        flag = True
        for item in left:
            if not item in other:
                flag = False
        return flag

    def __ge__(self, other):
        right = other.items()
        flag = True
        for item in right:
            if not item in self:
                flag = False
        return flag

    def __eq__(self, other):
        return (self <= other) and (self >= other)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self <= other) and (self != other)

    def __gt__(self, other):
        return (self >= other) and (self != other)

    def product(*args):
        pools = [tuple(pool.items()) for pool in args]
        res = [[]]
        for pool in pools:
            res = [x + [y] for x in res for y in pool]
        return res

    def order(self):
        return len(self.items())
