import re
import sys

class Token():
    def __init__(self,id:str,row:int,col:int,lex:str = None) -> None:
        self.id = id
        self.row = row
        self.col = col
        self.lex = lex

    def __repr__(self) -> str:
        if self.id == "ERROR":
            return ">>> Error lexico (Linea: {}, Posicion: {})".format(self.row,self.col)

        actualLex = (', ' + self.lex) if self.lex != None else ''
        toPrint = '<{}{}, {}, {}>'.format(self.id,actualLex,self.row,self.col) 
        return toPrint

opOrSym = {
    "=":"equals", 
    ".":"period", 
    ",":"comma", 
    ":":"colon", 
    "[":"left_brac", 
    "]":"right_brac", 
    "(":"left_paren", 
    ")":"right_paren", 
    "+":"plus", 
    "-":"minus", 
    "*":"times", 
    "/":"div", 
    "<>":"diff", 
    "<":"less", 
    "<=":"leq", 
    ">":"greater", 
    ">=":"geq"
}

keywords = [
    "TextWindow", "If", "Then", "EndIf", "Else", "ElseIf", "Goto", "While", "EndWhile",
    "For", "EndFor", "To", "Step", "Sub", "EndSub", "And", "Or", "Array", "Stack", "Program"
]

string = "(?P<string>\"[^\"]*\")"
comment = "(?P<comment>'.*)"
id = "(?P<id>[a-zA-ZÀ-ÿ]\w*)" #Aunque /w ya es el patron se tien que asegurar que no empiece por digitos
number = "(?P<number>\d+(\.\d*)?)"
compOp = "(?P<compOp>(<(>|=)?|>(=)?))" #Los operadores compuestos (2 char)
otherChar = "(?P<otherChar>\S)" # los operadores y los simbolos especiales
allrex = [string, comment, id, number, compOp, otherChar]

def lexer(l,r):
    finalPattern = "|".join(allrex) 
    finalValue = None
    for token in re.finditer(finalPattern, l):
        col = token.start() + 1 # aumentamos uno porque el inidice empieza en 1 no en 0
        if token.lastgroup == "comment":
            continue
        elif token.lastgroup == "string":
            value = token.group()
            if value.lower() == '"true"':
                finalValue = Token("True", r, col)
            elif value.lower() == '"false"':
                finalValue = Token("False", r, col)
            else:
                finalValue = Token("tkn_text", r, col, value[1:-1])
        elif token.lastgroup == "number":
            finalValue = Token("tkn_number", r, col, token.group())
        elif token.lastgroup == "id":
            if token.group() in keywords:
                finalValue = Token(token.group(), r, col)
            else:
                finalValue = Token("id", r, col, token.group())
        elif token.lastgroup == "compOp":
            tknId = "tkn_" + opOrSym[token.group()]
            finalValue = Token(tknId, r, col)
        else:
            if token.group() in opOrSym.keys():
                tknId = "tkn_" + opOrSym[token.group()]
                finalValue = Token(tknId, r, col)
            else:
                print(Token("ERROR",r, col))
                return "Error"
        print(finalValue)

rows = 1
# f = open("input.txt", 'r')
while True:
    try:
        line = input()
        '''
        # PARA PRUEBAS PERSONALES
        line = f.readline()
        if line == '':
            print("Acabo el archivo")
            break
        line = line[0:-1] if line[-1] == '\n' else line
        '''
        x = lexer(line, rows)
        if x == "Error":
            break
        rows += 1
    except EOFError: #Acaba cuando no hay mas entradas del usuario
        break