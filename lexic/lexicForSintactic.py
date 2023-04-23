import re

allmytokens = []
global token
ITERATOR = 0

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
    if l == "EOF":
        allmytokens.append(Token("$",r,1))
    else:
        finalPattern = "|".join(allrex) 
        finalValue = None
        for tkn in re.finditer(finalPattern, l):
            col = tkn.start() + 1 # aumentamos uno porque el inidice empieza en 1 no en 0
            if tkn.lastgroup == "comment":
                continue
            elif tkn.lastgroup == "string":
                value = tkn.group()
                if value.lower() == '"true"':
                    finalValue = Token("True", r, col, 'Verdadero')
                elif value.lower() == '"false"':
                    finalValue = Token("False", r, col, 'Falso')
                else:
                    finalValue = Token("tkn_text", r, col, value[1:-1])
            elif tkn.lastgroup == "number":
                finalValue = Token("tkn_number", r, col, tkn.group())
            elif tkn.lastgroup == "id":
                if tkn.group() in keywords:
                    finalValue = Token(tkn.group(), r, col, tkn.group())
                else:
                    finalValue = Token("id", r, col, tkn.group())
            elif tkn.lastgroup == "compOp":
                tknId = "tkn_" + opOrSym[tkn.group()]
                finalValue = Token(tknId, r, col, tkn.group())
            else:
                if tkn.group() in opOrSym.keys():
                    tknId = "tkn_" + opOrSym[tkn.group()]
                    finalValue = Token(tknId, r, col, tkn.group())
                else:
                    print(Token("ERROR",r, col)) 
                    return "ERROR"
            allmytokens.append(finalValue) 


rows = 1
while True:
    try:
        line = input()
        x = lexer(line, rows)
        if x == "Error":
            break
        rows += 1
    except EOFError: #Acaba cuando no hay mas entradas del usuario
        lexer('EOF', rows)
        break

#------------------------------------------------

