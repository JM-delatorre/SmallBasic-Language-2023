# TODO ADD github 
# TODO ADD LEXIC 

def errorSin(mylist):
    l = ",".join(mylist)
    print(f"[{token.row}:{token.col}] Error sintactico: Se encontro: {token.id}; se esperaba: {l}")

def emparejar(item):
    if token.id == item:
        ITERATOR += 1
        token = allmytokens[ITERATOR]
    else:
        errorSin([item])

def INICIO():
	if token.id in {'bus', 'big', 'cat', 'cow', 'ant'}:
		A()
	else:
		errorSin(['big', 'cat', 'bus', 'cow', 'ant'])
	print('esta es mi funcion INICIO')

def A():
	if token.id in {'big', 'cat', 'bus', 'cow'}:
		B()
		C()
	elif token.id in {'ant'}:
		emparejar("ant")
		A()
		emparejar("all")
	else:
		errorSin(['big', 'cat', 'bus', 'cow', 'ant'])
	print('esta es mi funcion A')

def B():
	if token.id in {'big'}:
		emparejar("big")
		C()
	elif token.id in {'bus'}:
		emparejar("bus")
		A()
		emparejar("boss")
	elif token.id in {'cat', 'cow'}:
		emparejar("&")
	else:
		errorSin(['big', 'cat', 'bus', 'cow'])
	print('esta es mi funcion B')

def C():
	if token.id in {'cat'}:
		emparejar("cat")
	elif token.id in {'cow'}:
		emparejar("cow")
	else:
		errorSin(['cat', 'cow'])
	print('esta es mi funcion C')

