# TODO ADD github 
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
                    finalValue = Token("True", r, col)
                elif value.lower() == '"false"':
                    finalValue = Token("False", r, col)
                else:
                    finalValue = Token("tkn_text", r, col, value[1:-1])
            elif tkn.lastgroup == "number":
                finalValue = Token("tkn_number", r, col, tkn.group())
            elif tkn.lastgroup == "id":
                if tkn.group() in keywords:
                    finalValue = Token(tkn.group(), r, col)
                else:
                    finalValue = Token("id", r, col, tkn.group())
            elif tkn.lastgroup == "compOp":
                tknId = "tkn_" + opOrSym[tkn.group()]
                finalValue = Token(tknId, r, col)
            else:
                if tkn.group() in opOrSym.keys():
                    tknId = "tkn_" + opOrSym[tkn.group()]
                    finalValue = Token(tknId, r, col)
                else:
                    print(Token("ERROR",r, col)) 
                    return "ERROR"
            allmytokens.append(finalValue) 


rows = 1
while True:
    try:
        line = input()
        # # PARA PRUEBAS PERSONALES
        # line = f.readline()
        # if line == '':
        #     print("Acabo el archivo")
        #     lexer('EOF', rows)
        #     break
        # line = line[0:-1] if line[-1] == '\n' else line
        x = lexer(line, rows)
        if x == "Error":
            break
        rows += 1
    except EOFError: #Acaba cuando no hay mas entradas del usuario
        lexer('EOF', rows)
        break

#------------------------------------------------

def errorSin(mylist):
    l = ",".join(mylist)
    print(f"[{token.row}:{token.col}] Error sintactico: Se encontro: {token.id}; se esperaba: {l}")

def emparejar(item):
    global token
    if token.id == item:
        ITERATOR += 1
        token = allmytokens[ITERATOR]
    else:
        errorSin([item])

def INICIO():
	if token.id in {'bus', 'cat', 'big', 'ant', 'cow'}:
		A()
	else:
		errorSin(['bus', 'big', 'cat', 'ant', 'cow'])
def A():
	if token.id in {'bus', 'big', 'cat', 'cow'}:
		B()
		C()
	elif token.id in {'ant'}:
		emparejar("ant")
		A()
		emparejar("all")
	else:
		errorSin(['bus', 'big', 'cat', 'ant', 'cow'])
def B():
	if token.id in {'big'}:
		emparejar("big")
		C()
	elif token.id in {'bus'}:
		emparejar("bus")
		A()
		emparejar("boss")
	elif token.id in {'cow', 'cat'}:
		emparejar("&")
	else:
		errorSin(['bus', 'big', 'cat', 'cow'])
def C():
	if token.id in {'cat'}:
		emparejar("cat")
	elif token.id in {'cow'}:
		emparejar("cow")
	else:
		errorSin(['cow', 'cat'])

print(allmytokens)