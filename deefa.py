import graphviz

ReservedWords = {
    "PROGRAM": 1,
    "IF": 2,
    "END": 3,
    "IMPLICIT": 4,
    "NONE": 5,
    "DO": 6,
    "ELSE": 7,
    "INTEGER": 8,
    "REAL": 9,
    "PARAMETER": 10,
    "COMPLEX": 11,
    "THEN": 12,
    "CHARACTER": 13,
    "READ": 14,
    "PRINT": 15,
    "LOGICAL": 16,
    ".TRUE.": 17,
    ".FALSE.": 18,
    "\n": 19,
    "ENDIF": 20,
    "ENDDO": 21
    # " ": Token_type.SPACE,
}
Operators = {".": 22,
             "=": 23,
             "+": 24,
             "-": 25,
             "*": 26,
             "/": 27,
             "<": 28,
             ">": 29,
             "(": 30,
             ")": 31,
             "[": 32,
             "]": 33,
             ",": 34,
             "'": 35,
             "\"": 36,
             ":": 37,
             "==": 38,
             ">=": 39,
             "<=": 40,
             "::": 41
             }


def generate_dfa(lex, bool):
    identifier_dfa = graphviz.Digraph(comment='DFA for Identifier')

    identifier_dfa.node('start')
    # identifier_dfa.node('accept', shape='doublecircle')
    if bool:
        identifier_dfa.node('DEAD')
    input_word = lex
    current_node = 'start'
    a = 1
    for node_count, char in enumerate(input_word):
        next_node = f'node{node_count}'
        identifier_dfa.node(next_node, label="S" + str(a))
        identifier_dfa.edge(current_node, next_node, label=f"[{char}]")
        if bool:
            start=ord(char[0])-1
            start=chr(start)
            end=ord(char[0])+1
            end=chr(end)
            identifier_dfa.edge(current_node, 'DEAD', label=f"^[{char}]")
        current_node = next_node
        a = a + 1
    identifier_dfa.node(current_node, shape='doublecircle')
    # identifier_dfa.edge(current_node, 'accept', label='')

    identifier_dfa.attr(rankdir='LR')

    identifier_dfa.render('identifier', format='png', view=True, directory="DFA")


import tkinter as tk
from tkinter import ttk


def create_gui(word_list):
    root = tk.Tk()
    root.title("Word List")

    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    for word in word_list:
        frame = tk.Frame(scrollable_frame)
        frame.pack(pady=5)

        label = tk.Label(frame, text=word, font=("Arial", 12, "bold"))
        label.pack(side=tk.LEFT, padx=10)

        button = tk.Button(frame, text="Click", command=lambda w=word: generate_dfa(w.upper(),
                                                                                    w.upper() in ReservedWords or w.upper() in Operators),
                           font=("Arial", 10, "bold"))
        button.pack(side=tk.LEFT, padx=10)

    root.mainloop()
