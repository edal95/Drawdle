from models.trie import Trie, TrieNode
from wordfreq import word_frequency
import heapq
import logging

def solve(en_trie, key, design):
    """
    solve, i.e. generate words to fill the
    wordle board with the desired design; return
    as lists of words to be displayed on board
    """
    solution = []
    design = [design[n:n+5] for n in range(0,26,5)]
    
    for pattern in design:
        # initialize candidate collections
        coloring, noncoloring = initialize_candidates(key)

        # initial parse for greens
        coloring, noncoloring = clear_greens(pattern, key, coloring, noncoloring)
        if not coloring:
            solution.append(key)
            continue

        # find matches and select best choice
        matches = build(en_trie, coloring, noncoloring, pattern, key)
        solution.append(resolve_matches(solution, matches))

    return solution

def initialize_candidates(key):
    """
    initialize the coloring and noncoloring collections
    """
    coloring = dict()
    for letter in key:
        coloring[letter] = coloring.get(letter,0) + 1
    noncoloring = {chr(ltr) for ltr in range(ord('A'),ord('Z')+1) if chr(ltr) not in coloring}
    return coloring, noncoloring
    

def clear_greens(pattern, key, coloring, noncoloring):
    """
    perform an initial parsing of the pattern to match
    all green positions and update candidate collections
    accordingly
    """
    for i, letter in enumerate(pattern):
        # for green, subtract from coloring
        if letter == 'G':
            coloring[key[i]] -= 1
            # exhaust if needed
            if coloring[key[i]] == 0:
                del coloring[key[i]]
                noncoloring.add(key[i])
    return coloring, noncoloring

def build(en_trie, coloring, noncoloring, pattern, key):
    """
    build a solution by DFS over available paths on trie, following color rules
    """
    potential_solutions = []
    def rec_build(node, substring, color_cand, noncolor_cand, pos):
        # if at end, add valid word to heap
        if len(node.children) == 0:
            frequency = word_frequency(substring, 'en')
            heapq.heappush(potential_solutions, (-frequency, substring))
            if len(potential_solutions) > 10000:
                heapq.heappop(potential_solutions)
            return
        cur_letter = key[pos]
        # if green, apply letter to substring and try to continue
        if pattern[pos] == 'G':
            if cur_letter in node.children:
                rec_build(node.children[cur_letter], substring + cur_letter, color_cand, noncolor_cand, pos+1)
        # if black, apply all possible candidates to substring and continue down all those paths
        elif pattern[pos] == 'B':
            # candidates are the intersection of noncoloring and children
            candidates = noncolor_cand.intersection(set(node.children.keys()))
            if cur_letter in candidates:
                candidates.remove(cur_letter)
            for candidate in candidates:
                rec_build(node.children[candidate], substring + candidate, color_cand, noncolor_cand, pos+1)
        # if yellow, apply all possible candidates to substring, update/possibly exhaust candidates, then continue down all the paths
        else: 
            # candidates are intersection of coloring and children, minus the current letter
            candidates = set(color_cand.keys()).intersection(set(node.children.keys()))
            if cur_letter in candidates:
                candidates.remove(cur_letter)
            for candidate in candidates:
                # adjust and possibly exhaust candidate counts
                color_cand[candidate] -= 1
                if color_cand[candidate] == 0:
                    del color_cand[candidate]
                    noncolor_cand.add(candidate)
                # recursive calls with new substring
                rec_build(node.children[candidate], substring + candidate, color_cand, noncolor_cand, pos+1)
                # fix counts to pre-call state and de-exhaust if necessary
                if candidate in noncolor_cand:
                    noncolor_cand.remove(candidate)
                    color_cand[candidate] = 1
                else:
                    color_cand[candidate] += 1
    rec_build(en_trie.root, '', coloring, noncoloring, 0)
    return potential_solutions
    
def resolve_matches(solution, matches):
    """
    return the most common match not yet used in the solution
    """
    if len(matches) == 0:
        return ''
    match = heapq.heappop(matches)[1]
    while match in solution and len(matches) > 0:
        match = heapq.heappop(matches)[1]
    return match
