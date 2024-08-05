from flask import Flask, render_template, request, jsonify
from logic.solver import solve
from models.trie import Trie, TrieNode
import pickle
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

try:
    trie_path = os.path.join('data','en_trie.pkl')
    with open(trie_path, 'rb') as f:
        en_trie = pickle.load(f)
    logging.info("Successfully loaded en_trie.")
except Exception as e:
    logging.error(f"Error loading en_trie: {e}")
    en_trie = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solveboard', methods=['POST'])
def get_and_solve_board():
    data = request.json
    # get design
    mapping = {"black":"B","goldenrod":"Y","limegreen":"G"}
    colors = data.get('colors', [])
    design = [mapping[c] for c in colors]
    # get key and return blank solution if invalid
    key = data.get('key', '')
    if len(key) != 5:
        return jsonify({'match':['     ']*6})
    # if trie failed to load
    if en_trie is None:
        return jsonify({'error': 'Data not loaded'}), 500
    # solve, format, and return solution
    solution = solve(en_trie, key, design)
    for i in range(len(solution)):
        if solution[i] == '':
            solution[i] = '     '
    return jsonify({'match': solution})


if __name__ == '__main__':
    app.run(debug=True)
