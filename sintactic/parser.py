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
		sentences()
	else:
		errorSin(['Sub', 'If', 'For', 'id', 'Array', 'Goto', 'Program', 'TextWindow', 'While', 'Stack'])
def sentences():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentence()
		temp_sentences()
	else:
		errorSin(['Sub', 'If', 'For', 'id', 'Array', 'Goto', 'Program', 'TextWindow', 'While', 'Stack'])
def temp_sentences():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentences()
	elif token.id in ['$', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile']:
		return
	else:
		errorSin(['Sub', 'ElseIf', 'If', 'EndIf', 'For', '$', 'EndFor', 'id', 'EndWhile', 'Array', 'Goto', 'Program', 'TextWindow', 'Else', 'While', 'EndSub', 'Stack'])
def sentence():
	if token.id in ['If']:
		if_conditional_sentence()
	elif token.id in ['While']:
		while_sentence()
	elif token.id in ['For']:
		for_sentence()
	elif token.id in ['id']:
		assign_sentence()
	elif token.id in ['TextWindow']:
		write_sentence()
	elif token.id in ['Sub']:
		sub_declare()
	elif token.id in ['Goto']:
		go_label()
	elif token.id in ['Array', 'Program', 'Stack']:
		builtin_declare()
	else:
		errorSin(['Sub', 'If', 'For', 'id', 'TextWindow', 'Goto', 'Array', 'Program', 'While', 'Stack'])
def builtin_declare():
	if token.id in ['Program']:
		emparejar("Program")
		builtin_block()
	elif token.id in ['Stack']:
		emparejar("Stack")
		builtin_block()
	elif token.id in ['Array']:
		emparejar("Array")
		builtin_block()
	else:
		errorSin(['Array', 'Program', 'Stack'])
def builtin_block():
	if token.id in ['tkn_period']:
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		arguments()
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_period'])
def arguments():
	if token.id in ['Array', 'False', 'Program', 'Stack', 'True', 'id', 'tkn_comma', 'tkn_number', 'tkn_right_paren', 'tkn_text']:
		param_option()
		builtin_param()
	elif token.id in ['tkn_right_paren']:
		return
	else:
		errorSin(['tkn_text', 'False', 'True', 'tkn_comma', 'id', 'tkn_number', 'Array', 'tkn_right_paren', 'Program', 'Stack'])
def builtin_param():
	if token.id in ['tkn_comma']:
		emparejar("tkn_comma")
		param_option()
		builtin_param()
	elif token.id in ['tkn_right_paren']:
		return
	else:
		errorSin(['tkn_comma', 'tkn_right_paren'])
def param_option():
	if token.id in ['Array', 'False', 'Program', 'Stack', 'True', 'id', 'tkn_number', 'tkn_text']:
		myvar()
	elif token.id in ['tkn_comma', 'tkn_right_paren']:
		return
	else:
		errorSin(['tkn_text', 'False', 'True', 'tkn_comma', 'id', 'tkn_number', 'Array', 'tkn_right_paren', 'Program', 'Stack'])
def assign_sentence():
	if token.id in ['id']:
		emparejar("id")
		assign_sentence1()
	else:
		errorSin(['id'])
def array_continue():
	if token.id in ['tkn_left_brac']:
		emparejar("tkn_left_brac")
		myvar()
		emparejar("tkn_right_brac")
		emparejar("tkn_equals")
		myvar()
	elif token.id in ['tkn_equals']:
		emparejar("tkn_equals")
		expr()
	elif token.id in ['$', 'Array', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		return
	else:
		errorSin(['ElseIf', 'id', 'tkn_equals', 'Stack', 'Sub', 'EndIf', 'EndWhile', '$', 'EndFor', 'For', 'Array', 'If', 'tkn_left_brac', 'TextWindow', 'Goto', 'Program', 'Else', 'While', 'EndSub'])
def temp_sentence():
	if token.id in ['TextWindow']:
		emparejar("TextWindow")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		emparejar("tkn_right_paren")
	elif token.id in ['Array', 'False', 'Program', 'Stack', 'TextWindow', 'True', 'id', 'tkn_left_paren', 'tkn_minus', 'tkn_number', 'tkn_text']:
		expr()
	elif token.id in ['Array', 'Program', 'Stack']:
		builtin_declare()
	else:
		errorSin(['tkn_text', 'tkn_minus', 'False', 'True', 'id', 'tkn_left_paren', 'TextWindow', 'Array', 'Program', 'tkn_number', 'Stack'])
def write_sentence():
	if token.id in ['TextWindow']:
		emparejar("TextWindow")
		emparejar("tkn_period")
		emparejar("id")
		emparejar("tkn_left_paren")
		write_sentence1()
	else:
		errorSin(['TextWindow'])
def if_conditional_sentence():
	if token.id in ['If']:
		emparejar("If")
		emparejar("tkn_left_paren")
		expr_conditional()
		emparejar("tkn_right_paren")
		emparejar("Then")
		sentences()
		elseif_conditional()
		else_conditional()
		emparejar("EndIf")
	else:
		errorSin(['If'])
def elseif_conditional():
	if token.id in ['ElseIf']:
		emparejar("ElseIf")
		emparejar("tkn_left_paren")
		expr_conditional()
		emparejar("tkn_right_paren")
		emparejar("Then")
		sentences()
		elseif_conditional()
	elif token.id in ['Else', 'EndIf']:
		return
	else:
		errorSin(['EndIf', 'Else', 'ElseIf'])
def else_conditional():
	if token.id in ['Else']:
		emparejar("Else")
		sentences()
	elif token.id in ['EndIf']:
		return
	else:
		errorSin(['EndIf', 'Else'])
def label():
	if token.id in ['id']:
		emparejar("id")
		emparejar("tkn_colon")
	else:
		errorSin(['id'])
def go_label():
	if token.id in ['Goto']:
		emparejar("Goto")
		emparejar("id")
	else:
		errorSin(['Goto'])
def while_sentence():
	if token.id in ['While']:
		emparejar("While")
		emparejar("tkn_left_paren")
		expr_conditional()
		emparejar("tkn_right_paren")
		sentences()
		emparejar("EndWhile")
	else:
		errorSin(['While'])
def for_sentence():
	if token.id in ['For']:
		emparejar("For")
		myvar()
		emparejar("tkn_equals")
		expr()
		emparejar("To")
		expr_conditional()
		for_sentence1()
	else:
		errorSin(['For'])
def sub_declare():
	if token.id in ['Sub']:
		emparejar("Sub")
		emparejar("id")
		sub_block()
		emparejar("EndSub")
	else:
		errorSin(['Sub'])
def sub_block():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'TextWindow', 'While', 'id']:
		sub_sentences()
	elif token.id in ['EndSub']:
		return
	else:
		errorSin(['If', 'For', 'id', 'Array', 'Goto', 'Program', 'TextWindow', 'While', 'EndSub', 'Stack'])
def sub_sentences():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'TextWindow', 'While', 'id']:
		sub_sentence()
		temp_sentences()
	else:
		errorSin(['If', 'For', 'id', 'Array', 'Goto', 'Program', 'TextWindow', 'While', 'Stack'])
def sub_sentence():
	if token.id in ['If']:
		if_conditional_sentence()
	elif token.id in ['While']:
		while_sentence()
	elif token.id in ['For']:
		for_sentence()
	elif token.id in ['id']:
		assign_sentence()
	elif token.id in ['TextWindow']:
		write_sentence()
	elif token.id in ['Goto']:
		go_label()
	elif token.id in ['Array', 'Program', 'Stack']:
		builtin_declare()
	else:
		errorSin(['If', 'For', 'id', 'TextWindow', 'Goto', 'Array', 'Program', 'While', 'Stack'])
def expr():
	if token.id in ['tkn_left_paren']:
		emparejar("tkn_left_paren")
		expr()
		emparejar("tkn_right_paren")
		expr1()
	elif token.id in ['TextWindow']:
		write_sentence()
	elif token.id in ['tkn_minus']:
		emparejar("tkn_minus")
		expr()
	elif token.id in ['Array', 'False', 'Program', 'Stack', 'True', 'id', 'tkn_number', 'tkn_text']:
		myvar()
		expr1()
	else:
		errorSin(['tkn_text', 'tkn_minus', 'False', 'True', 'id', 'tkn_left_paren', 'TextWindow', 'Array', 'Program', 'tkn_number', 'Stack'])
def expr1():
	if token.id in ['tkn_diff', 'tkn_div', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_times']:
		op()
		expr()
	elif token.id in ['And', 'Or']:
		conector()
		expr()
	elif token.id in ['$', 'Array', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'To', 'While', 'id', 'tkn_right_paren']:
		return
	else:
		errorSin(['tkn_less', 'tkn_plus', 'ElseIf', 'id', 'Or', 'tkn_div', 'While', 'tkn_greater', 'Stack', 'Sub', 'EndIf', 'EndWhile', '$', 'EndFor', 'For', 'Array', 'And', 'If', 'tkn_right_paren', 'TextWindow', 'Goto', 'Program', 'Else', 'tkn_diff', 'tkn_geq', 'To', 'tkn_minus', 'tkn_times', 'tkn_leq', 'EndSub'])
def expr_conditional():
	if token.id in ['Array', 'Program', 'Stack']:
		builtin_declare()
		expr_conditional()
	elif token.id in ['tkn_diff', 'tkn_div', 'tkn_equals', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_times']:
		op_conditional()
		myvar()
	elif token.id in ['tkn_minus']:
		emparejar("tkn_minus")
		expr_conditional()
	elif token.id in ['TextWindow']:
		write_sentence()
	elif token.id in ['Array', 'False', 'Program', 'Stack', 'True', 'id', 'tkn_number', 'tkn_text']:
		myvar()
		expr_conditional1()
	elif token.id in ['tkn_left_paren']:
		emparejar("tkn_left_paren")
		myvar()
		expr_conditional11()
	else:
		errorSin(['tkn_less', 'tkn_plus', 'True', 'id', 'tkn_number', 'tkn_equals', 'tkn_div', 'tkn_greater', 'Stack', 'tkn_text', 'False', 'Array', 'tkn_left_paren', 'TextWindow', 'Program', 'tkn_diff', 'tkn_geq', 'tkn_minus', 'tkn_times', 'tkn_leq'])
def expr_conditional1():
	if token.id in ['tkn_diff', 'tkn_div', 'tkn_equals', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_times']:
		op_conditional()
		expr_conditional()
	elif token.id in ['And', 'Or']:
		conector()
		expr_conditional()
	elif token.id in ['And', 'Array', 'For', 'Goto', 'If', 'Or', 'Program', 'Stack', 'Step', 'Sub', 'TextWindow', 'While', 'id', 'tkn_diff', 'tkn_div', 'tkn_equals', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_right_paren', 'tkn_times']:
		return
	else:
		errorSin(['tkn_less', 'tkn_plus', 'id', 'tkn_equals', 'Or', 'tkn_div', 'While', 'tkn_greater', 'Stack', 'Sub', 'For', 'Array', 'Step', 'And', 'If', 'tkn_right_paren', 'TextWindow', 'Goto', 'Program', 'tkn_diff', 'tkn_geq', 'tkn_minus', 'tkn_times', 'tkn_leq'])
def text():
	if token.id in ['Array', 'False', 'Program', 'Stack', 'True', 'id', 'tkn_number', 'tkn_text']:
		myvar()
		temp_text()
	else:
		errorSin(['tkn_text', 'False', 'True', 'id', 'tkn_number', 'Array', 'Program', 'Stack'])
def temp_text():
	if token.id in ['tkn_plus']:
		emparejar("tkn_plus")
		myvar()
		temp_text()
	elif token.id in ['tkn_right_paren']:
		return
	else:
		errorSin(['tkn_plus', 'tkn_right_paren'])
def myvar():
	if token.id in ['id']:
		emparejar("id")
		temp_var()
	elif token.id in ['Array', 'Program', 'Stack']:
		builtin_declare()
	elif token.id in ['tkn_number']:
		emparejar("tkn_number")
	elif token.id in ['True']:
		emparejar("True")
	elif token.id in ['False']:
		emparejar("False")
	elif token.id in ['tkn_text']:
		emparejar("tkn_text")
	else:
		errorSin(['tkn_text', 'True', 'False', 'tkn_number', 'id', 'Array', 'Program', 'Stack'])
def temp_var():
	if token.id in ['tkn_left_brac']:
		emparejar("tkn_left_brac")
		myvar()
		emparejar("tkn_right_brac")
	elif token.id in ['$', 'And', 'Array', 'Else', 'ElseIf', 'EndFor', 'EndIf', 'EndSub', 'EndWhile', 'For', 'Goto', 'If', 'Or', 'Program', 'Stack', 'Step', 'Sub', 'TextWindow', 'To', 'While', 'id', 'tkn_comma', 'tkn_diff', 'tkn_div', 'tkn_equals', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_right_brac', 'tkn_right_paren', 'tkn_times']:
		return
	else:
		errorSin(['tkn_leq', 'tkn_less', 'tkn_plus', 'ElseIf', 'id', 'tkn_equals', 'Or', 'tkn_div', 'tkn_greater', 'Stack', 'Sub', 'EndIf', 'EndWhile', '$', 'EndFor', 'For', 'Array', 'tkn_right_brac', 'Step', 'And', 'If', 'tkn_comma', 'tkn_left_brac', 'tkn_right_paren', 'TextWindow', 'Goto', 'Program', 'Else', 'tkn_diff', 'tkn_geq', 'To', 'tkn_minus', 'tkn_times', 'While', 'EndSub'])
def conector():
	if token.id in ['And']:
		emparejar("And")
	elif token.id in ['Or']:
		emparejar("Or")
	else:
		errorSin(['And', 'Or'])
def op():
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
		errorSin(['tkn_leq', 'tkn_less', 'tkn_plus', 'tkn_minus', 'tkn_times', 'tkn_div', 'tkn_diff', 'tkn_greater', 'tkn_geq'])
def op_conditional():
	if token.id in ['tkn_leq']:
		emparejar("tkn_leq")
	elif token.id in ['tkn_geq']:
		emparejar("tkn_geq")
	elif token.id in ['tkn_less']:
		emparejar("tkn_less")
	elif token.id in ['tkn_greater']:
		emparejar("tkn_greater")
	elif token.id in ['tkn_equals']:
		emparejar("tkn_equals")
	elif token.id in ['tkn_plus']:
		emparejar("tkn_plus")
	elif token.id in ['tkn_times']:
		emparejar("tkn_times")
	elif token.id in ['tkn_minus']:
		emparejar("tkn_minus")
	elif token.id in ['tkn_div']:
		emparejar("tkn_div")
	elif token.id in ['tkn_diff']:
		emparejar("tkn_diff")
	else:
		errorSin(['tkn_div', 'tkn_less', 'tkn_plus', 'tkn_minus', 'tkn_times', 'tkn_equals', 'tkn_leq', 'tkn_diff', 'tkn_greater', 'tkn_geq'])
def assign_sentence1():
	if token.id in ['tkn_equals']:
		emparejar("tkn_equals")
		temp_sentence()
	elif token.id in ['tkn_colon']:
		emparejar("tkn_colon")
	elif token.id in ['tkn_left_brac']:
		emparejar("tkn_left_brac")
		myvar()
		emparejar("tkn_right_brac")
		array_continue()
	elif token.id in ['tkn_left_paren']:
		emparejar("tkn_left_paren")
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_left_brac', 'tkn_equals', 'tkn_colon', 'tkn_left_paren'])
def write_sentence1():
	if token.id in ['Array', 'False', 'Program', 'Stack', 'True', 'id', 'tkn_number', 'tkn_text']:
		text()
		emparejar("tkn_right_paren")
	elif token.id in ['id']:
		emparejar("id")
		emparejar("tkn_right_paren")
	elif token.id in ['Array', 'False', 'Program', 'Stack', 'TextWindow', 'True', 'id', 'tkn_left_paren', 'tkn_minus', 'tkn_number', 'tkn_text']:
		expr()
		emparejar("tkn_right_paren")
	elif token.id in ['tkn_right_paren']:
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_text', 'tkn_minus', 'False', 'True', 'id', 'tkn_number', 'Array', 'TextWindow', 'Program', 'tkn_left_paren', 'tkn_right_paren', 'Stack'])
def for_sentence1():
	if token.id in ['Array', 'For', 'Goto', 'If', 'Program', 'Stack', 'Sub', 'TextWindow', 'While', 'id']:
		sentences()
		emparejar("EndFor")
	elif token.id in ['Step']:
		emparejar("Step")
		expr()
		sentences()
		emparejar("EndFor")
	else:
		errorSin(['Sub', 'If', 'For', 'id', 'Array', 'Goto', 'Program', 'TextWindow', 'While', 'Step', 'Stack'])
def expr_conditional11():
	if token.id in ['tkn_diff', 'tkn_div', 'tkn_equals', 'tkn_geq', 'tkn_greater', 'tkn_leq', 'tkn_less', 'tkn_minus', 'tkn_plus', 'tkn_times']:
		op_conditional()
		expr_conditional()
		expr_conditional1()
		emparejar("tkn_right_paren")
		expr_conditional1()
	elif token.id in ['And', 'Or']:
		conector()
		expr_conditional()
		emparejar("tkn_right_paren")
	else:
		errorSin(['tkn_leq', 'And', 'tkn_less', 'tkn_plus', 'tkn_minus', 'tkn_times', 'tkn_equals', 'Or', 'tkn_div', 'tkn_diff', 'tkn_greater', 'tkn_geq'])

token = allmytokens[ITERATOR]
INICIO()
if token.id != "$": 
	errorSin(["$"]) 
else: 
	print("El analisis sintactico ha finalizado exitosamente.", end=' ') 
