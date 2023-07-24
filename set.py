from typing import Any, Optional, Iterable
from random import random


class Node:
    def __init__(self, val, key: Any):
        self.val = val                                   # 値
        self.key: Any = key                              # 木管理のためのキー
        self.child: list[Optional[Node]] = [None, None]  # [左の子, 右の子]
        self.priority: float = random()                  # 優先度
        self.size: int = 1                               # 部分木のサイズ
        self.sum: int = key                              # 部分木の値の和

    def update(self):  # ノードの更新
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
        self.root: Optional[Node] = None  # 根のノードを保持しておく

    def __str__(self) -> str:  # 出力時の整形
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

    def __repr__(self) -> str:  # 出力時の整形
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

    # 木の回転  b=0 で左回転, b=1 で右回転
    # 再帰関数として実装する都合上、別で public なメンバ関数 rotate を用意しています
    def _rotate(root: Optional[Node], b):
        s = root.child[1-b]
        root.child[1-b] = s.child[b]
        s.child[b] = root
        root.update()
        s.update()
        return s

    # 値の挿入  値として int など以外のものを入れるにあたって、str(val) の hash をみかけ上の key としています. 最悪な実装ですが, うまい方法が思いつきませんでした
    # 再帰関数として実装する都合上、別で public なメンバ関数 insert を用意しています
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

    # 値が key であるノードの削除
    # 再帰関数として実装する都合上、別で public なメンバ関数 erase を用意しています
    def _erase(root: Optional[Node], val):
        key = hash(str(val))
        if root == None:
            return None

        if val != root.val:
            b = int(key < root.key)
            root.child[1-b] = Treap._erase(root.child[1-b], val)
        else:
            if (root.child[0] == None or root.child[1] == None):
                root = root.child[0] if root.child[0] != None else root.child[1]
            else:
                b = int(root.child[0].priority < root.child[1].priority)
                root = Treap._rotate(root, 1-b)
                root.child[1-b] = Treap._erase(root.child[1-b], val)
        return root

    # 値が val であるノードの検索 あれば True, なければ False
    # 再帰関数として実装する都合上、別で public なメンバ関数 find を用意しています
    def _find(root: Optional[Node], val):
        key = hash(str(val))
        if root == None:
            return False
        if val == root.val:
            return True
        else:
            return Treap._find(root.child[root.key < key], val)

    # 値の挿入
    def insert(self, key):
        self.root = Treap._insert(self.root, key)
        return self

    # 値の削除
    def erase(self, key):
        self.root = Treap._erase(self.root, key)
        return self

    # 値の検索
    def find(self, key):
        return Treap._find(self.root, key)

    # すべての値の列挙
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
    # Iterable なオブジェクト (list など) から Set を構成する
    def __init__(self, l: Iterable[Any] = []):
        super().__init__()

        for val in l:
            self.insert(val)

    def copy(self):  # deepcopy
        return Set(self.items())

    def order(self):  # 位数
        return len(self.items())

    def __add__(self, other):  # 直和集合
        res = Set()
        for item in self.items():
            res.insert((item, 0))
        for item in other.items():
            res.insert((item, 1))
        return res

    def __or__(self, other):  # 和集合
        res = self.copy()
        for item in other.items():
            res.insert(item)
        return res

    def __sub__(self, other):  # 差集合
        res = self.copy()
        for item in other.items():
            res.erase(item)
        return res

    def __mul__(self, other):  # 直積集合 (2項間)
        res = Set()
        for p in self.items():
            for q in other.items():
                res.insert((p, q))
        return res

    def __and__(self, other):  # 積集合
        res = self.copy()
        res = res - (self - other)
        return res

    def __rpow__(self, left):  # べき集合
        if left != 2:
            raise ValueError(f"Power set should be written as: 2 ** Set")
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

    def __contains__(self, val):  # 値 val が集合に属するか
        return self.find(val)

    def __le__(self, other):  # 左辺の集合は右辺の集合の部分集合か
        left = self.items()
        flag = True
        for item in left:
            if not item in other:
                flag = False
        return flag

    def __ge__(self, other):  # 右辺の集合は左辺の集合の部分集合か
        right = other.items()
        flag = True
        for item in right:
            if not item in self:
                flag = False
        return flag

    def __eq__(self, other):  # 左辺の集合と右辺の集合は等しいか
        return (self <= other) and (self >= other)

    def __ne__(self, other):  # 左辺の集合と右辺の集合は等しくないか
        return not (self == other)

    def __lt__(self, other):  # 左辺の集合は右辺の集合の真部分集合か
        return (self <= other) and (self != other)

    def __gt__(self, other):  # 右辺の集合は左辺の集合の真部分集合か
        return (self >= other) and (self != other)

    def product(*args):  # 直積集合 (多項間)
        pools = [tuple(pool.items()) for pool in args]
        res = [[]]
        for pool in pools:
            res = [x + [y] for x in res for y in pool]
        return Set(res)

    def direct_sum(*args):  # 直和集合 (多項間)
        res = Set()
        for idx, val in enumerate(args):
            for item in val.items():
                res.insert((item, idx))
        return res

s = Set([0, 1, 2])
print(s)
print(s + s)
print(s - s)
print(s * s)
print(s & s)
print(s | s)
print(2 ** s)
print(1 in s)
print(4 in s)
print(s <= Set([0, 1, 2, 3]))
print(s <= Set([0, 1]))
print(s >= Set([0, 1]))
print(s >= Set([0, 1, 2, 3]))
print(s == Set([0, 1, 2]))
print(Set.product(s, s, s))
print(s.erase(2))
