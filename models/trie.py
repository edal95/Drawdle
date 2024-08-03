class TrieNode:
    def __init__(self, letter='*'):
        self.letter = letter
        self.children = dict()

class Trie:
    def __init__(self):
        self.root = TrieNode()
