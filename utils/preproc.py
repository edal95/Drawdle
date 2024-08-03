from models.trie import Trie, TrieNode
import json
import pickle

def build_trie(dictionary):
    """
    build 5-letter word trie from JSON of all English words
    """
    en_trie = Trie()
    for word in dictionary:
        # filter for 5-letter words
        if len(word) != 5:
            continue
        # insert missing nodes in trie to build word
        cur = en_trie.root
        for letter in word:
            if letter not in cur.children:
                cur.children[letter] = TrieNode(letter)
            cur = cur.children[letter]
    return en_trie

def persist_trie(en_trie):
    """
    persist trie using pickle
    """
    with open('data/en_trie.pkl', 'wb') as f:
        pickle.dump(en_trie, f)

def main():
    """
    build and persist the en_trie
    """
    with open('dictionary.json') as f:
        dictionary = json.load(f)
    en_trie = build_trie(dictionary)
    persist_trie(en_trie)
    

if __name__ == '__main__':
    main()
