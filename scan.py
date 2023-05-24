import deefa
import tkinter as tk
from tkinter import filedialog as fd
from enum import Enum
import re
import pandas


class Token_type(Enum):  # listing all tokens type

    Implicit = 1
    End = 2
    DO = 3
    Else = 4
    COMMA = 5
    If = 6
    INTEGER = 7
    Dot = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    Identifier = 18
    Constant = 19
    Error = 20
    PROGRAM = 21
    NONE = 22
    REAL = 23
    COMPLEX = 24
    LOGICAL = 25
    CHARACTER = 26  # add brackets for length
    PARAMETER = 27
    SINGLECOLON = 28
    THEN = 29
    LEFTPARANTHESES = 30  # (
    LEN = 31
    RIGHTPARANTHESES = 32  # )
    DOUBLEQUOTATION = 33
    LESSTHANOREQUALOP = 34
    GREATERTHANOREQUAL = 35
    EQUALCOMP = 36
    SINGLEQUOTATION = 38
    READ = 39
    PRINT = 40
    TRUE = 41
    FALSE = 42
    COMMENTOP = 43
    NEWLINE = 44
    BLOCKNAME = 45
    LEFTBRACKET = 46  # [
    RIGHTBRACKET = 47  # ]
    # SPACE = 48  # ]
    COMMENTED = 49
    DOUBLECOLON = 50
    ENDIF = 51
    ENDDO = 52
    STRING = 53


# class token to hold string and token type
class token:
    def _init_(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {
    "PROGRAM": Token_type.PROGRAM,
    "IF": Token_type.If,
    "END": Token_type.End,
    "IMPLICIT": Token_type.Implicit,
    "NONE": Token_type.NONE,
    "DO": Token_type.DO,
    "ELSE": Token_type.Else,
    "INTEGER": Token_type.INTEGER,
    "REAL": Token_type.REAL,
    "PARAMETER": Token_type.PARAMETER,
    "COMPLEX": Token_type.COMPLEX,
    "THEN": Token_type.THEN,
    "CHARACTER": Token_type.CHARACTER,
    "READ": Token_type.READ,
    "PRINT": Token_type.PRINT,
    "LOGICAL": Token_type.LOGICAL,
    # "TRUE": Token_type.TRUE,
    # "FALSE": Token_type.FALSE,
    "\n": Token_type.NEWLINE,
    "ENDIF": Token_type.ENDIF,
    "ENDDO": Token_type.ENDDO
    # " ": Token_type.SPACE,
}
Operators = {".": Token_type.Dot,
             "=": Token_type.EqualOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             "<": Token_type.LessThanOp,
             ">": Token_type.GreaterThanOp,
             "(": Token_type.LEFTPARANTHESES,
             ")": Token_type.RIGHTPARANTHESES,
             "[": Token_type.LEFTBRACKET,
             "]": Token_type.RIGHTBRACKET,
             ",": Token_type.COMMA,
             "'": Token_type.SINGLEQUOTATION,
             "\"": Token_type.DOUBLEQUOTATION,
             ":": Token_type.SINGLECOLON,
             "==": Token_type.EQUALCOMP,
             ">=": Token_type.GREATERTHANOREQUAL,
             "<=": Token_type.LESSTHANOREQUALOP,
             "::": Token_type.DOUBLECOLON
             }
Tokens = []  # to add tokens to list
scannerErrors = []


def find_token(text):
    # tokens = re.findall(r'\w+|[\=\+\-\*\/\<\>\(\)\{\}\'\"\n\:\[\]\,\!\." "]', text)
    tokens = re.findall(r'\w+|\W', text)
    print(tokens)
    i = 0
    """while i<len(tokens):
        if(tokens[i]=="="and tokens[i+1]=="="):
            Tokens.append(token(i, Token_type.EQUALCOMP))
            i+=1
        i+=1"""
    while i < len(tokens):
        if tokens[i] == " ":
            i = i + 1
            continue
        elif tokens[i] == "!":
            t = token()
            t.lex = str(tokens[i])
            t.token_type = Token_type.COMMENTOP
            Tokens.append(t)
            j = i + 1
            comments = ""
            while j < len(tokens):
                if tokens[j] != "\n":
                    comments += tokens[j]
                    j += 1
                else:
                    break
            i = j - 1
            if (comments != ""):
                s = token()
                s.lex = comments
                s.token_type = Token_type.COMMENTED
                Tokens.append(s)

        elif str(tokens[i]).upper() in ReservedWords:
            if str(tokens[i]).upper() == "END" and i + 2 < len(tokens):
                if str(tokens[i + 2]).upper() == "IF":
                    t = token()
                    t.lex = "ENDIF"
                    t.token_type = Token_type.ENDIF
                    Tokens.append(t)
                    i = i + 2
                elif str(tokens[i + 2]).upper() == "DO":
                    t = token()
                    t.lex = "ENDDO"
                    t.token_type = Token_type.ENDDO
                    Tokens.append(t)
                    i = i + 2
                else:
                    t = token()
                    t.lex = str(tokens[i]).upper()
                    t.token_type = Token_type.End
                    Tokens.append(t)
            else:
                t = token()
                t.lex = str(tokens[i]).upper()
                t.token_type = ReservedWords[str(tokens[i]).upper()]
                Tokens.append(t)
        elif re.match(r"^[a-zA-Z][a-zA-z0-9]*$", tokens[i]):
            t = token()
            t.lex = str(tokens[i]).upper()
            t.token_type = Token_type.Identifier
            Tokens.append(t)
        elif tokens[i] in Operators:
            if tokens[i] == "." and i + 1 < len(tokens):
                if str(tokens[i + 1]).upper() == "TRUE":
                    if i + 2 < len(tokens):
                        if tokens[i + 2] == ".":
                            t = token()
                            t.lex = str(tokens[i] + tokens[i + 1] + tokens[i + 2])
                            t.token_type = Token_type.TRUE
                            Tokens.append(t)
                            i = i + 2
                        else:
                            t = token()
                            t.lex = str(tokens[i] + tokens[i + 1])
                            t.token_type = Token_type.Error
                            scannerErrors.append(t)
                            Tokens.append(t)
                            i = i + 1
                    else:
                        t = token()
                        t.lex = str(tokens[i] + tokens[i + 1])
                        t.token_type = Token_type.Error
                        scannerErrors.append(t)
                        Tokens.append(t)
                        i = i + 1
                elif str(tokens[i + 1]).upper() == "FALSE":
                    if i + 2 < len(tokens):
                        if tokens[i + 2] == ".":
                            t = token()
                            t.lex = str(tokens[i] + tokens[i + 1] + tokens[i + 2])
                            t.token_type = Token_type.FALSE
                            Tokens.append(t)
                            i = i + 2
                        else:
                            t = token()
                            t.lex = str(tokens[i] + tokens[i + 1])
                            t.token_type = Token_type.Error
                            scannerErrors.append(t)
                            Tokens.append(t)
                            i = i + 1
                    else:
                        t = token()
                        t.lex = str(tokens[i] + tokens[i + 1])
                        t.token_type = Token_type.Error
                        scannerErrors.append(t)
                        Tokens.append(t)
                        i = i + 1
                else:
                    t = token()
                    t.lex = str(tokens[i])
                    t.token_type = Token_type.Dot
                    Tokens.append(t)
            elif tokens[i] == "'" and i + 1 < len(tokens):
                j = i + 1
                string = ""
                while j < len(tokens):
                    if tokens[j] == "'":
                        break
                    elif tokens[j] == "\n":
                        break
                    else:
                        string += tokens[j]
                        j += 1
                if j < len(tokens):
                    if tokens[j] == "'":
                        t = token()
                        t.lex = tokens[i]
                        t.token_type = Token_type.SINGLEQUOTATION
                        Tokens.append(t)
                        if string != "":
                            s = token()
                            s.lex = str(string)
                            s.token_type = Token_type.STRING
                            Tokens.append(s)
                        d = token()
                        d.lex = str(tokens[j])
                        d.token_type = Token_type.SINGLEQUOTATION
                        Tokens.append(d)
                    if tokens[j] == "\n":
                        t = token()
                        t.lex = str(tokens[i] + string)
                        t.token_type = Token_type.Error
                        scannerErrors.append(t)
                        Tokens.append(t)
                        s = token()
                        s.lex = str(tokens[j])
                        s.token_type = Token_type.NEWLINE
                else:
                    t = token()
                    t.lex = str(tokens[i] + string)
                    t.token_type = Token_type.Error
                    scannerErrors.append(t)
                    Tokens.append(t)
                i = j
            elif tokens[i] == "'":
                t = token()
                t.lex = str(tokens[i])
                t.token_type = Token_type.Error
                scannerErrors.append(t)
                Tokens.append(t)

            elif tokens[i] == "\"" and i + 1 < len(tokens):
                j = i + 1
                string = ""
                while j < len(tokens):
                    if tokens[j] == "\"":
                        break
                    elif tokens[j] == "\n":
                        break
                    else:
                        string += tokens[j]
                        j += 1
                if j < len(tokens):
                    if tokens[j] == "\"":
                        t = token()
                        t.lex = tokens[i]
                        t.token_type = Token_type.DOUBLEQUOTATION
                        Tokens.append(t)
                        if string != "":
                            s = token()
                            s.lex = str(string)
                            s.token_type = Token_type.STRING
                            Tokens.append(s)
                        d = token()
                        d.lex = str(tokens[j])
                        d.token_type = Token_type.DOUBLEQUOTATION
                        Tokens.append(d)
                    if tokens[j] == "\n":
                        t = token()
                        t.lex = str(tokens[i] + string)
                        t.token_type = Token_type.Error
                        scannerErrors.append(t)
                        Tokens.append(t)
                        s = token()
                        s.lex = str(tokens[j])
                        s.token_type = Token_type.NEWLINE
                else:
                    t = token()
                    t.lex = str(tokens[i] + string)
                    t.token_type = Token_type.Error
                    scannerErrors.append(t)
                    Tokens.append(t)
                i = j
            elif tokens[i] == "\"":
                t = token()
                t.lex = str(tokens[i])
                t.token_type = Token_type.Error
                scannerErrors.append(t)
                Tokens.append(t)
            elif tokens[i] == "=" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = "=="
                    t.token_type = Operators["=="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = "="
                    t.token_type = Operators["="]
                    Tokens.append(t)

            elif tokens[i] == "<" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = "<="
                    t.token_type = Operators["<="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = "<"
                    t.token_type = Operators["<"]
                    Tokens.append(t)
            elif tokens[i] == ">" and i + 1 < len(tokens):
                if tokens[i + 1] == "=":
                    t = token()
                    t.lex = ">="
                    t.token_type = Operators[">="]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = ">"
                    t.token_type = Operators[">"]
                    Tokens.append(t)
            elif tokens[i] == ":" and i + 1 < len(tokens):
                if tokens[i + 1] == ":":
                    t = token()
                    t.lex = "::"
                    t.token_type = Operators["::"]
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = ":"
                    t.token_type = Operators[":"]
                    Tokens.append(t)
            else:
                t = token()
                t.lex = str(tokens[i]).upper()
                t.token_type = Operators[tokens[i]]
                Tokens.append(t)
        elif re.match(r"\d+", tokens[i]) and not re.search(r"[a-zA-Z]+", tokens[i]):
            # ([0-9]+)+(\.[0-9]*)?  -?\d+(.\d+)?
            if i + 1 < len(tokens):
                if tokens[i + 1] == "." and i + 2 < len(tokens):
                    if re.match(r"\d+", tokens[i + 2]) and not re.search(r"[a-zA-Z]+", tokens[i + 2]):
                        t = token()
                        t.lex = str(tokens[i] + tokens[i + 1] + tokens[i + 2]).upper()
                        t.token_type = Token_type.Constant
                        Tokens.append(t)
                        i = i + 2
                    else:
                        t = token()
                        t.lex = str(tokens[i] + tokens[i + 1] + tokens[i + 2]).upper()
                        t.token_type = Token_type.Error
                        scannerErrors.append(t)
                        Tokens.append(t)
                        i = i + 2
                elif tokens[i + 1] == ".":
                    t = token()
                    t.lex = str(tokens[i] + tokens[i + 1]).upper()
                    t.token_type = Token_type.Error
                    scannerErrors.append(t)
                    Tokens.append(t)
                    i = i + 1
                else:
                    t = token()
                    t.lex = str(tokens[i]).upper()
                    t.token_type = Token_type.Constant
                    Tokens.append(t)
            else:
                t = token()
                t.lex = str(tokens[i]).upper()
                t.token_type = Token_type.Constant
                Tokens.append(t)
        else:
            t = token()
            t.lex = str(tokens[i]).upper()
            t.token_type = Token_type.Error
            scannerErrors.append(t)
            Tokens.append(t)
        i += 1
    return Tokens


def getErrors():
    return scannerErrors
import tkinter as tk
from tkinter import filedialog
import pandas as pd

root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner and Parser Phases')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            entry1.delete(0, tk.END)
            entry1.insert(tk.END, file_contents)


browse_button = tk.Button(text='Browse', command=browse_file, bg='orange', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=browse_button)


def Scan():
    x1 = entry1.get()
    x = find_token(x1)
    df = pd.DataFrame.from_records([t.to_dict() for t in x])
    print(df.to_string())
    label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)

    label4 = tk.Label(root, text="Token_type" + x1, font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(150, 260, window=button1)


def Parse():
    x1 = entry1.get()
    # TODO: Implement the parsing logic for the given input
    #       Update the GUI accordingly



button2 = tk.Button(text='Parse', command=Parse, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(250, 260, window=button2)

root.mainloop()

lexemes=[]
for t in Tokens:
    if t.token_type!=Token_type.COMMENTED and t.token_type!=Token_type.STRING and t.token_type!=Token_type.NEWLINE:
        lexemes.append(t.lex)
deefa.create_gui(lexemes)