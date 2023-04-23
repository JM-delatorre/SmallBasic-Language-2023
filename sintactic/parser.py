# https://github.com/JM-delatorre/SmallBasic-Language-2023
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

def errorSin(mylist):
    for i in range(len(mylist)):
        mylist[i] = conv(mylist[i])
    mylist.sort()
    l = "', '".join(mylist)
    l = "'" + l + "'." 
    if token.id == "$":
        print(f"[{token.row}:{token.col}] Error sintactico: Se encontro el final del archivo; se esperaba: {l}")

    else:
        print(f"[{token.row}:{token.col}] Error sintactico: Se encontro: '{token.lex}'; se esperaba: {l}")

    exit()
def conv(tkn):
    if tkn == "$":
        return "EOF"
    elif tkn == "id":
        return "Identificador"
    elif tkn == "tkn_number":
        return "Numero"
    elif tkn == "tkn_text":
        return "Texto"
    elif tkn == "True":
        return "Verdadero"
    elif tkn == "False":
        return "Falso" 
    elif "tkn_" in tkn:
        tkn = tkn.replace("tkn_", "")
        return list(opOrSym.keys())[list(opOrSym.values()).index(tkn)]
    else:
        return tkn
def emparejar(item):
    global token
    global ITERATOR
    if token.id == item:
        ITERATOR += 1
        token = allmytokens[ITERATOR]
    else:
        errorSin([item])

def INICIO():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentencias()
	else:
		errorSin(['Array', 'Goto', 'Stack', 'While', 'Sub', 'TextWindow', 'id', 'If', 'Program', 'For'])
def sentencias():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentencia()
		sigue()
	else:
		errorSin(['Array', 'Goto', 'Stack', 'While', 'Sub', 'TextWindow', 'id', 'If', 'Program', 'For'])
def sigue():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentencias()
	elif token.id in ['$', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile']:
		return
	else:
		errorSin(['ElseIf', 'EndFor', 'Array', 'EndWhile', 'Goto', 'Stack', 'While', 'Sub', 'TextWindow', 'id', '$', 'Else', 'EndIf', 'EndSub', 'If', 'Program', 'For'])
def sentencia():
	if token.id in ['If']:
		sentencia_condicional_if()
	elif token.id in ['While']:
		sentencia_while()
	elif token.id in ['For']:
		sentencia_for()
	elif token.id in ['id']:
		sentencia_de_asignacion()
	elif token.id in ['TextWindow']:
		sentencia_escritura()
	elif token.id in ['Sub']:
		declarar_subrutina()
	elif token.id in ['Goto']:
		ir_a_etiqueta()
	elif token.id in ['Array', 'Program', 'Stack']:
		funcion_built_in()
	else:
		errorSin(['Array', 'Goto', 'While', 'id', 'Sub', 'TextWindow', 'Stack', 'If', 'Program', 'For'])
def funcion_built_in():
	if token.id in ['Stack']:
		emparejar("Stack")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		variable()
		parametros_built_in()
		emparejar("tkn_right_paren")
	elif token.id in ['Array']:
		emparejar("Array")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		variable()
		parametros_built_in()
		emparejar("tkn_right_paren")
	elif token.id in ['Program']:
		emparejar("Program")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		funcion_built_in1()
	else:
		errorSin(['Program', 'Array', 'Stack'])
def parametros_built_in():
	if token.id in ['tkn_comma']:
		emparejar("tkn_comma")
		opcion_parametro()
		parametros_built_in()
	elif token.id in ['tkn_right_paren']:
		return
	else:
		errorSin(['tkn_right_paren', 'tkn_comma'])
def opcion_parametro():
	if token.id in ['False', 'True', 'id', 'tkn_number', 'tkn_text']:
		variable()
	elif token.id in ['tkn_comma', 'tkn_right_paren']:
		return
	else:
		errorSin(['tkn_right_paren', 'False', 'id', 'tkn_text', 'tkn_comma', 'True', 'tkn_number'])
def sentencia_de_asignacion():
	if token.id in ['id']:
		emparejar("id")
		sentencia_de_asignacion1()
	else:
		errorSin(['id'])
def continuar_array():
	if token.id in ['tkn_left_brac']:
		emparejar("tkn_left_brac")
		variable()
		emparejar("tkn_right_brac")
		emparejar("tkn_equals")
		variable()
	elif token.id in ['tkn_equals']:
		emparejar("tkn_equals")
		variable()
	elif token.id in ['$', 'Array', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		return
	else:
		errorSin(['tkn_left_brac', 'tkn_equals', 'Else', 'Sub', 'TextWindow', 'ElseIf', 'EndWhile', 'Goto', 'EndSub', 'Stack', 'While', 'id', 'EndIf', 'Program', 'Array', '$', 'If', 'EndFor', 'For'])
def otra_sentencia():
	if token.id in ['TextWindow']:
		emparejar("TextWindow")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		emparejar("tkn_right_paren")
	elif token.id in ['False', 'True', 'id', 'tkn_left_paren', 'tkn_minus', 'tkn_number', 'tkn_text']:
		expresion()
	elif token.id in ['Array', 'Program', 'Stack']:
		funcion_built_in()
	else:
		errorSin(['tkn_left_paren', 'Array', 'tkn_minus', 'False', 'Stack', 'id', 'TextWindow', 'tkn_text', 'Program', 'True', 'tkn_number'])
def sentencia_escritura():
	if token.id in ['TextWindow']:
		emparejar("TextWindow")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		sentencia_escritura1()
	else:
		errorSin(['TextWindow'])
def sentencia_condicional_if():
	if token.id in ['If']:
		emparejar("If")
		emparejar("tkn_left_paren")
		expresion_condicion()
		emparejar("tkn_right_paren")
		emparejar("Then")
		sentencias()
		condicional_ElseIf()
		condicional_Else()
		emparejar("EndIf")
	else:
		errorSin(['If'])
def condicional_ElseIf():
	if token.id in ['ElseIf']:
		emparejar("ElseIf")
		emparejar("tkn_left_paren")
		expresion_condicion()
		emparejar("tkn_right_paren")
		emparejar("Then")
		sentencias()
		condicional_ElseIf()
	elif token.id in ['Else', 'EndIf']:
		return
	else:
		errorSin(['ElseIf', 'EndIf', 'Else'])
def condicional_Else():
	if token.id in ['Else']:
		emparejar("Else")
		sentencias()
	elif token.id in ['EndIf']:
		return
	else:
		errorSin(['EndIf', 'Else'])
def etiqueta():
	if token.id in ['id']:
		emparejar("id")
		emparejar("tkn_colon")
	else:
		errorSin(['id'])
def ir_a_etiqueta():
	if token.id in ['Goto']:
		emparejar("Goto")
		emparejar("id")
	else:
		errorSin(['Goto'])
def sentencia_while():
	if token.id in ['While']:
		emparejar("While")
		emparejar("tkn_left_paren")
		expresion_condicion()
		emparejar("tkn_right_paren")
		sentencias()
		emparejar("EndWhile")
	else:
		errorSin(['While'])
def sentencia_for():
	if token.id in ['For']:
		emparejar("For")
		emparejar("id")
		emparejar("tkn_equals")
		emparejar("tkn_number")
		emparejar("To")
		emparejar("tkn_number")
		sentencia_for1()
	else:
		errorSin(['For'])
def declarar_subrutina():
	if token.id in ['Sub']:
		emparejar("Sub")
		emparejar("id")
		contenido_subrutina()
		emparejar("EndSub")
	else:
		errorSin(['Sub'])
def contenido_subrutina():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'TextWindow', 'While', 'id']:
		sentencias_subrutina()
	elif token.id in ['EndSub']:
		return
	else:
		errorSin(['Array', 'Goto', 'Stack', 'While', 'id', 'TextWindow', 'EndSub', 'If', 'Program', 'For'])
def sentencias_subrutina():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'TextWindow', 'While', 'id']:
		sentencia_sub()
		sigue()
	else:
		errorSin(['Array', 'Goto', 'Stack', 'While', 'id', 'TextWindow', 'If', 'Program', 'For'])
def sentencia_sub():
	if token.id in ['If']:
		sentencia_condicional_if()
	elif token.id in ['While']:
		sentencia_while()
	elif token.id in ['For']:
		sentencia_for()
	elif token.id in ['id']:
		sentencia_de_asignacion()
	elif token.id in ['TextWindow']:
		sentencia_escritura()
	elif token.id in ['Goto']:
		ir_a_etiqueta()
	elif token.id in ['Array', 'Program', 'Stack']:
		funcion_built_in()
	else:
		errorSin(['Array', 'Goto', 'While', 'id', 'Stack', 'TextWindow', 'If', 'Program', 'For'])
def expresion():
	if token.id in ['tkn_minus']:
		emparejar("tkn_minus")
		expresion()
	elif token.id in ['False', 'True', 'id', 'tkn_number', 'tkn_text']:
		variable()
		expresion1()
	elif token.id in ['tkn_left_paren']:
		emparejar("tkn_left_paren")
		variable()
		expresion11()
	else:
		errorSin(['tkn_left_paren', 'tkn_minus', 'False', 'id', 'tkn_text', 'True', 'tkn_number'])
def expresion_condicion():
	if token.id in ['False', 'True', 'id', 'tkn_number', 'tkn_text']:
		variable()
		expresion_condicion1()
	elif token.id in ['tkn_left_paren']:
		emparejar("tkn_left_paren")
		variable()
		expresion_condicion11()
	else:
		errorSin(['tkn_left_paren', 'False', 'id', 'tkn_text', 'True', 'tkn_number'])
def texto():
	if token.id in ['False', 'True', 'id', 'tkn_number', 'tkn_text']:
		variable()
		texto_aux()
	else:
		errorSin(['False', 'id', 'tkn_text', 'True', 'tkn_number'])
def texto_aux():
	if token.id in ['tkn_plus']:
		emparejar("tkn_plus")
		variable()
		texto_aux()
	elif token.id in ['tkn_right_paren']:
		return
	else:
		errorSin(['tkn_right_paren', 'tkn_plus'])
def variable():
	if token.id in ['id']:
		emparejar("id")
		variable_aux()
	elif token.id in ['tkn_number']:
		emparejar("tkn_number")
	elif token.id in ['True']:
		emparejar("True")
	elif token.id in ['False']:
		emparejar("False")
	elif token.id in ['tkn_text']:
		emparejar("tkn_text")
	else:
		errorSin(['False', 'id', 'tkn_text', 'True', 'tkn_number'])
def variable_aux():
	if token.id in ['tkn_left_brac']:
		emparejar("tkn_left_brac")
		variable()
		emparejar("tkn_right_brac")
	elif token.id in ['$', 'And', 'Array', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile', 'For', 'Goto', 'If', 'Or', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id', 'tkn_comma', 'tkn_diff', 'tkn_div', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_right_brac', 'tkn_right_paren', 'tkn_times']:
		return
	else:
		errorSin(['tkn_left_brac', 'Else', 'Sub', 'TextWindow', 'tkn_times', 'tkn_right_paren', 'tkn_div', 'ElseIf', 'tkn_right_brac', 'tkn_minus', 'And', 'EndWhile', 'Goto', 'tkn_geq', 'Or', 'EndSub', 'tkn_plus', 'Stack', 'While', 'id', 'tkn_greater', 'EndIf', 'Program', 'tkn_leq', 'Array', '$', 'tkn_diff', 'tkn_less', 'If', 'EndFor', 'For', 'tkn_comma'])
def conector():
	if token.id in ['And']:
		emparejar("And")
	elif token.id in ['Or']:
		emparejar("Or")
	else:
		errorSin(['Or', 'And'])
def operador():
	if token.id in ['tkn_plus']:
		emparejar("tkn_plus")
	elif token.id in ['tkn_minus']:
		emparejar("tkn_minus")
	elif token.id in ['tkn_times']:
		emparejar("tkn_times")
	elif token.id in ['tkn_div']:
		emparejar("tkn_div")
	elif token.id in ['tkn_diff']:
		emparejar("tkn_diff")
	elif token.id in ['tkn_leq']:
		emparejar("tkn_leq")
	elif token.id in ['tkn_geq']:
		emparejar("tkn_geq")
	elif token.id in ['tkn_less']:
		emparejar("tkn_less")
	elif token.id in ['tkn_greater']:
		emparejar("tkn_greater")
	else:
		errorSin(['tkn_leq', 'tkn_plus', 'tkn_minus', 'tkn_geq', 'tkn_greater', 'tkn_diff', 'tkn_times', 'tkn_less', 'tkn_div'])
def operador_condicion():
	if token.id in ['tkn_leq']:
		emparejar("tkn_leq")
	elif token.id in ['tkn_geq']:
		emparejar("tkn_geq")
	elif token.id in ['tkn_less']:
		emparejar("tkn_less")
	elif token.id in ['tkn_greater']:
		emparejar("tkn_greater")
	else:
		errorSin(['tkn_less', 'tkn_leq', 'tkn_geq', 'tkn_greater'])
def funcion_built_in1():
	if token.id in ['id']:
		emparejar("id")
		emparejar("tkn_right_paren")
	elif token.id in ['tkn_number']:
		emparejar("tkn_number")
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_number', 'id'])
def sentencia_de_asignacion1():
	if token.id in ['tkn_equals']:
		emparejar("tkn_equals")
		otra_sentencia()
	elif token.id in ['tkn_colon']:
		emparejar("tkn_colon")
	elif token.id in ['tkn_left_brac']:
		emparejar("tkn_left_brac")
		variable()
		emparejar("tkn_right_brac")
		continuar_array()
	elif token.id in ['tkn_left_paren']:
		emparejar("tkn_left_paren")
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_equals', 'tkn_left_paren', 'tkn_left_brac', 'tkn_colon'])
def sentencia_escritura1():
	if token.id in ['False', 'True', 'id', 'tkn_number', 'tkn_text']:
		texto()
		emparejar("tkn_right_paren")
	elif token.id in ['id']:
		emparejar("id")
		emparejar("tkn_right_paren")
	elif token.id in ['tkn_right_paren']:
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_right_paren', 'False', 'id', 'tkn_text', 'True', 'tkn_number'])
def sentencia_for1():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentencias()
		emparejar("EndFor")
	elif token.id in ['Step']:
		emparejar("Step")
		emparejar("tkn_number")
		sentencias()
		emparejar("EndFor")
	else:
		errorSin(['Array', 'Goto', 'Stack', 'While', 'Sub', 'TextWindow', 'id', 'Step', 'If', 'Program', 'For'])
def expresion1():
	if token.id in ['tkn_diff', 'tkn_div', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_times']:
		operador()
		expresion()
	elif token.id in ['And', 'Or']:
		conector()
		expresion()
	elif token.id in ['$', 'Array', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id', 'tkn_right_paren']:
		return
	else:
		errorSin(['Else', 'Sub', 'TextWindow', 'tkn_times', 'tkn_right_paren', 'tkn_div', 'ElseIf', 'tkn_minus', 'And', 'EndWhile', 'Goto', 'tkn_geq', 'Or', 'EndSub', 'tkn_plus', 'Stack', 'While', 'tkn_greater', 'id', 'EndIf', 'Program', 'tkn_leq', 'Array', '$', 'tkn_diff', 'tkn_less', 'If', 'EndFor', 'For'])
def expresion11():
	if token.id in ['tkn_diff', 'tkn_div', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_times']:
		operador()
		expresion()
		emparejar("tkn_right_paren")
	elif token.id in ['And', 'Or']:
		conector()
		expresion()
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_leq', 'tkn_plus', 'tkn_minus', 'And', 'tkn_geq', 'tkn_greater', 'Or', 'tkn_diff', 'tkn_less', 'tkn_times', 'tkn_div'])
def expresion_condicion1():
	if token.id in ['tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less']:
		operador_condicion()
		expresion_condicion()
	elif token.id in ['And', 'Or']:
		conector()
		expresion_condicion()
	elif token.id in ['tkn_right_paren']:
		return
	else:
		errorSin(['tkn_leq', 'And', 'tkn_geq', 'tkn_greater', 'Or', 'tkn_less', 'tkn_right_paren'])
def expresion_condicion11():
	if token.id in ['tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less']:
		operador_condicion()
		expresion_condicion()
		emparejar("tkn_right_paren")
	elif token.id in ['And', 'Or']:
		conector()
		expresion_condicion()
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_leq', 'And', 'tkn_geq', 'tkn_greater', 'Or', 'tkn_less'])

token = allmytokens[ITERATOR]
INICIO()
if token.id != "$": 
	errorSin(["$"]) 
else: 
	print("El analisis sintactico ha finalizado exitosamente.", end=' ') 
