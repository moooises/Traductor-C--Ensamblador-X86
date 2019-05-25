import sys
sys.path.append('../..')

from sly import Lexer, Parser
#usar $ tanto para & como para *
tabla = {} #Dictionary
labels = 0
class Tabla():
    contador = 0
    global tabla
    def insertVar(self, var, value):
        if var in tabla:
            raise NameError('Variable ' + "\"" + var + "\"" + ' declarada anteriormente')
        else:
            self.contador -= 4
            tabla[var] = [self.contador, value,]

    def insertValue(self, var, value):
        if var in tabla:
            tabla[var][1] = value #Modificamos el campo valor de la variable.
        else:
            raise NameError('Variable ' + "\"" + var + "\"" + 'no declarada')

    def compVar(self, var):
        if var in tabla:
            return 't'
        else:
            return 'f'

    def cadena(self, var):
        if var in tabla:
            res = str(tabla[var][0]) + "(%ebp)"
        else:
            res = "$" + str(var)
        return res

manejador = Tabla()
def incrementLabel():
    global labels
    labels = labels + 1
    print('L' + str(labels) + ':')
def decrementLabel(): #Lo uso en el while.
    global labels
    labels = labels - 1


class NodoVariable():
    def __init__(self):
        print("subl $4, %esp")

class NodoAsign():
    def __init__(self, variable, valor):
        if valor == None:
            print("movl %eax, " + str(tabla[variable][0]) + "(%ebp)")
        else:
            print("movl $" + str(valor) + ", " + str(tabla[variable][0]) + "(%ebp)")

class NodoSuma():
    def __init__(self, valor1, valor2):
        #Vamos a la tabla para la comprobacion de tipos.
        str1 = manejador.cadena(valor1)#[0]
        str2 = manejador.cadena(valor2)#[0]

        print("movl " + str1 + ", %eax")
        print("addl " + str2 + ", %eax")
        #print("movl %eax, " + str1)

class NodoProducto():
    def __init__(self, valor1, valor2):
        str1 = manejador.cadena(valor1)
        str2 = manejador.cadena(valor2)
        print("movl " + str1 + ", %eax")
        print("addl " + str2 + ", %eax")
        print("movl %eax, " + str1)

class NodoEqual():
    def __init__(self, valor1, valor2):
        print("operador ==")

class NodoNequal():
    def __init__(self, valor1, valor2):
        print("operador !=")

class NodoGreater():
    def __init__(self, valor1, valor2):
        print("operador >")

class NodoLogic():
    def __init__(self,  valor1, op, valor2):
        self. valor1 = valor1
        self.op = op
        self.valor2 = valor2

    def escribir(self):
        #Averiguar en que posicion esta la variable que buscas.
        print( "cmp " + manejador.cadena(self.valor2) + "," + manejador.cadena(self.valor1))

    def salto(self):
        global labels
        if self.op == '!=':
            print("je L" + str(labels + 1))
        if self.op == '==':
            print("jne L" + str(labels + 1))

class CalcLexer(Lexer):
    tokens = {ID, TIPO, NUM, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, EQUAL, NEQUAL ,GREATER,
              IF, ELSE, WHILE, LKEY, RKEY, COMA, END, LESS}
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['int'] = TIPO
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    NUM = r'\d+'

    #Aritmetic
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    GREATER = r'>'
    LESS = r'<'
    EQUAL = r'=='
    NEQUAL = r'!='
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    LKEY = r'{'
    RKEY = r'}'
    COMA = r','
    END = r';'


    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens
    #manejador = Tabla()

    #precedence = (
    #    ('left', PLUS, MINUS),
    #    ('left', TIMES, DIVIDE),
    #    ('right', UMINUS)
    #    )

    def __init__(self):
        self.names = { }

    @_('f_linea instruction')
    def entrada(self,p):
        pass

    @_('statement')
    def instruction(self, p):
        pass

    @_('WHILE LPAREN empty1 empty2 statement RKEY')
    def instruction(selfself, p):
        global labels
        print('jmp L' + str(labels))
        incrementLabel()

    @_(" ")
    def empty1(self, p):
        incrementLabel() #Imprimir la etiqueta actual

    @_("logic RPAREN LKEY")
    def empty2(self, p):
        p.logic.salto() #Instruccion de salto.

    """ #Fin del bucle while antiguo
    @_('endwhile')#('WHILE LPAREN logic RPAREN LKEY statement RKEY')
    def instruction(self, p):
        print('Pasando por instruction')
        pass

    @_('middle statement RKEY')
    def endwhile(self, p):
        print('pasando por endwhile')
        pass

    @_('middle_logic RPAREN LKEY')
    def middle(self, p):
        print('pasando por middle')
        pass

    @_('begin_while LPAREN logic')
    def middle_logic(self, p):
        print('pasando por middle_logic')
        nodo = p.logic
        print(nodo.valor1, nodo.op, nodo.valor2)
        pass

    @_('WHILE LPAREN')
    def begin_while(self, p):
        #print('pasando por begin_while')
        incrementLabel()
        pass
    """
    #Comienzo del bucle while

    @_('endif  endelse')
    def instruction(self,p):
        print("Pasando por endif  endelse")

    @_('middle_if statement RKEY')
    def endif(self,p):
        print("Pasando por middleif statement RKEY")

    @_('middle_if_logic LKEY')
    def middle_if(self,p):
        print("Pasando por middle_if_logic LKEY")

    @_('begin_if logic RPAREN')
    def middle_if_logic(self,p):
        print("Pasando por begin_if logic RPAREN")

    @_('IF LPAREN')
    def begin_if(self,p):
        print("Pasando por IF LPAREN")

    @_('middle_else RKEY')
    def endelse(self,p):
        print("Pasa por middleelse RKEY")

    @_('')
    def endelse(self,p):
        print("No hay else")

    @_('begin_else statement')
    def middle_else(self,p):
        print("Pasa por begin_else statement")

    @_('ELSE LKEY')
    def begin_else(self,p):
        print("Paso por ELSE LKEY")

    @_('TIPO linea END f_linea')
    def f_linea(self, p):
        #print('Instruccion correcta')
        pass

    @_('')
    def f_linea(self, p):
        pass

    @_('assig rest')
    def linea(self, p):
        pass
        #manejador.insertVar(p.ID) #Aquí almacenamos la variable.

    @_('ID rest')
    def linea(self, p):
        manejador.insertVar(p.ID, 0)
        NodoVariable()

    @_('ID ASSIGN logic')
    def assig(self,p):
        manejador.insertVar(p.ID, p.logic)
        NodoVariable()
        NodoAsign(p.ID, p.logic)
        #print(tabla[p.ID])

    @_(' ')
    def assig(self, p):
        pass

    @_('COMA linea')
    def rest(self, p):
        pass

    @_(' ')
    def rest(self,p):
        pass

    @_('ID ASSIGN logic END statement')
    def statement(self, p): #Falta buscar el valor en el sistema
        manejador.insertValue(p.ID, p.logic)
        NodoAsign(p.ID, p.logic)
        #print('pasando por statement')
        #tabla[p.ID][1] = p.logic
        #print(tabla[p.ID])

    @_('logic')
    def statement(self,p):
        return p.logic
    @_(' ')
    def statement(self,p):
        pass

    @_('logic EQUAL logicpr')
    def logic(self, p):
        return NodoLogic(p.logic, p.EQUAL, p.logicpr)

    @_('logic NEQUAL logicpr')
    def logic(self, p):
        a = NodoLogic(p.logic, p.NEQUAL, p.logicpr)
        a.escribir()
        return a
        #print('pasando por !=')

    @_('logicpr')
    def logic(self,p):
        return p.logicpr

    @_('logicpr GREATER expr')
    def logicpr(self, p):
        NodoGreater(p.logicpr, p.expr)

    @_('logicpr LESS expr')
    def logicpr(self, p):
        NodoLess(p.logicpr, p.expr)

    @_('expr')
    def logicpr(self, p):
        return p.expr

    @_('expr PLUS fact')
    def expr(self, p):
        NodoSuma(p.expr,p.fact)

    @_('expr MINUS fact')
    def expr(self, p):
        a = NodoResta(p.expr, p.fact)
        return a.result #p.expr0 - p.expr1

    @_('fact')
    def expr(self, p):
        return p.fact

    @_('fact TIMES basico')
    def fact(self, p):
        a = NodoProducto(p.fact, p.basico)
        #return a.result #p.expr0 * p.expr1

    @_('fact DIVIDE basico')
    def fact(self, p):
        a = fact(p.fact, p.basico)
        return a.result #p.expr0 / p.expr1

    @_('basico')
    def fact(self, p):
        return p.basico

    @_('MINUS basico')
    def basico(self, p):
        return -p.basico

    @_('ID') #Uso de la variable
    def basico(self, p): #Si el id no esta en la tabla, debe mostrar error.
        return p.ID

    @_('NUM')
    def basico(self, p):
        #print("NUM = ", p.NUM)
        return int(p.NUM)

    @_('LPAREN expr RPAREN')
    def basico(self, p):
        return p.expr

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))

#entrada -> int a = 3, b = 4; while( a != 3) { a = a + 1; }
#entrada -> int a = 3, b =4; a = a +b;

#Problemas: La insercion de variables en la pila se hace al reves.
