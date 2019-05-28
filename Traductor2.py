import sys
sys.path.append('../..')

from sly import Lexer, Parser
#usar $ tanto para & como para *
tabla = {} #Dictionary
labels = 0
labelswhile=0
eax=False
class Tabla():
    contador = 0
    global tabla
    def insertVar(self, var, value):
        if var in tabla:
            raise NameError('Variable ' + "\"" + str(var) + "\"" + ' declarada anteriormente')
        else:
            self.contador -= 4
            tabla[var] = [self.contador, value,]

    def insertValue(self, var, value):
        if var in tabla:
            tabla[var][1] = value #Modificamos el campo valor de la variable.
        else:
            raise NameError('Variable ' + "\"" + str(var) + "\"" + 'no declarada')

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
"""

def incrementLabel():
    global labels
    labels = labels + 1
    print('L' + str(labels) + ':')
def decrementLabel(): #Lo uso en el while.
    global labels
    labels = labels - 1
"""
def incrementLabel():
    global labels
    labels = labels + 1
    #print('L' + str(labels) + ':')
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
    def __init__(self):
        print("addl %ecx, %eax")
        #print("movl %eax, " + str1)

class NodoResta():
    def __init__(self):
        print("subl %ecx, %eax")

class NodoProducto():
    def __init__(self):
        print("imull %ecx, %eax")

class NodoDivision():
    def __init__(self):
        print("cdq")
        print("divl %ecx")

class NodoEqual():
    def __init__(self):
        global labels
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp %edx, %ecx")
        print("jne final"+str(labels))
        print("movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()


class NodoNequal():
    def __init__(self):
        global labels
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp %edx, %ecx")
        print("je final"+str(labels))
        print("movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoGreater():
    def __init__(self):
        global labels
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp %edx, %ecx")
        print("jle final"+str(labels))
        print("movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()


class NodoSmaller():
    def __init__(self):
        global labels
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp %edx, %ecx")
        print("jg final"+str(labels))
        print(" movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoSmallerEqual():
    def __init__(self):
        global labels
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp %edx, %ecx")
        print("jg final"+str(labels))
        print(" movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoGreaterEqual():
    def __init__(self):
        global labels
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp %edx, %ecx")
        print("jl final"+str(labels))
        print(" movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoNeg():##Problema con esto
    def __init__(self):
        global eax
        if eax:
            print("negl %eax")
        else:
            print("negl %ecx")


class NodoNot():#aqui
    def __init__(self):
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp $0, %edx")
        print("jne final"+str(labels))
        print("movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoAnd():
    def __init__(self):
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("cmp $0, %edx")
        print("je final"+str(labels))
        print("movl %ecx,%edx")
        print("cmp $0, %edx")
        print("je final"+str(labes))
        print("movl $1, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoOr():
    def __init__(self):
        print("movl %eax,%edx")
        print("movl $1,%eax")
        print("cmp $0, %edx")
        print("jne final"+str(labels))
        print("movl %ecx,%edx")
        print("cmp $0, %edx")
        print("jne final"+str(labels))
        print("movl $0, %eax")
        print("final"+str(labels)+":")
        incrementLabel()

class NodoWhile():
    def __init__(self):
        print("cmp $0,%eax")
        print("je final"+str(labels))

class NodoIf():
    def __init__(self):
        print("cmp $0,%eax")
        print("je final"+str(labels))

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
        if self.op == '<':
            print("jl L" + str(labels + 1))
        if self.op == '>':
            print("jg L" + str(labels + 1))
        if self.op == '<=':
            print("jle L" + str(labels + 1))
        if self.op == '>=':
            print("jge L" + str(labels + 1))

class CalcLexer(Lexer):
    tokens = {ID, TIPO, NUM, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, EQUAL, NEQUAL ,GREATER,
              IF, ELSE, WHILE, LKEY, RKEY, COMA, END, LESS, BIGGEROREQUAL, LESSOREQUAL}
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
    BIGGEROREQUAL = r'>='
    LESSOREQUAL = r'<='
    EQUAL = r'=='
    NEQUAL = r'!='
    GREATER = r'>'
    LESS = r'<'
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

    @_('statement') #Aquí he quitado el END que genera ambigüedad.
    def instruction(self, p):
        print("holaaaaaaaaa")

    @_(' ')
    def instruction(self, p):
        print("En epsilon")

    @_('WHILE LPAREN empty1 empty2 instruction RKEY') #He sustituido statement por instruction.
    def instruction(selfself, p):
        global labels
        print("En el while")
        print('jmp final' + str(labelswhile))
        print("final"+str(labels)+":")
        incrementLabel()

    @_(" ")
    def empty1(self, p):
        global labels,labelswhile
        print("final"+str(labels)+":")
        labelswhile=labels
        incrementLabel() #Imprimir la etiqueta actual

    @_("logic RPAREN LKEY")
    def empty2(self, p):
        global eax
        NodoWhile()
        eax=False
    #Comienzo del bucle while
    #@_('WHILE LPAREN empty1 empty2 statement RKEY')

    @_('IF LPAREN empty3 LKEY instruction elseif')
    def instruction(self,p):
        print("En el if")

    @_('logic RPAREN')
    def empty3(self,p):
        global eax
        NodoIf()
        eax=False


    @_('RKEY')
    def elseif(self,p):
        print("final"+str(labels))
        incrementLabel()

    @_('empty4 instruction RKEY')
    def elseif(self,p):
        print("final"+str(labels)+":")

    @_("ELSE LKEY")
    def empty4(self,p):
        print("jmp final"+str(labels+1))
        print("final"+str(labels)+":")
        incrementLabel()

    @_('TIPO linea END f_linea')
    def f_linea(self, p):
        #print('Instruccion correcta')
        pass

    @_('')
    def f_linea(self, p):
        pass

    @_('assig rest')
    def linea(self, p):
        print("ultimo respiro")
        pass
        #manejador.insertVar(p.ID) #Aquí almacenamos la variable.

    @_('ID rest')
    def linea(self, p):
        manejador.insertVar(p.ID, 0)
        NodoVariable()

    @_('ID ASSIGN logic')
    def assig(self,p):
        global eax
        manejador.insertVar(p.ID, p.logic)
        NodoVariable()
        print("movl %eax, "+ str(tabla[p.ID][0]) + "(%ebp)")
        eax=False
        #NodoAsign(p.ID, p.logic)
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
        print("pasando statement")
        manejador.insertValue(p.ID, p.logic)
        NodoAsign(p.ID, p.logic)
        #print('pasando por statement')
        #tabla[p.ID][1] = p.logic
        #print(tabla[p.ID])

    @_('logic')
    def statement(self,p):
        print("corre")
        return p.logic
    @_(' ')
    def statement(self,p):
        pass

    @_('logic EQUAL logicpr')
    def logic(self, p):
        NodoEqual()
        return p.logic != p.logicpr
        #return NodoLogic(p.logic, p.EQUAL, p.logicpr)

    @_('logic NEQUAL logicpr')
    def logic(self, p):
        NodoNequal()
        return p.logic != p.logicpr

    @_('logicpr')
    def logic(self, p):
        return p.logicpr #Perfe, debería subir el nodo.

    @_('logicpr LESSOREQUAL expr')
    def logicpr(self, p):
        NodoSmallerEqual()
        return p.logicpr <= p.expr

    @_('logicpr BIGGEROREQUAL expr')
    def logicpr(self, p):
        NodoGreaterEqual()
        return p.logicpr >= p.expr

    @_('logicpr GREATER expr')
    def logicpr(self, p):
        NodoGreater()
        return p.logicpr > p.expr

    @_('logicpr LESS expr')
    def logicpr(self, p):
        NodoSmaller()
        return p.logicpr < p.expr

    @_('expr')
    def logicpr(self, p):
        return p.expr

    @_('expr PLUS fact')
    def expr(self, p):
        NodoSuma()
        return p.expr+p.fact

    @_('expr MINUS fact')
    def expr(self, p):
        NodoResta()
        return p.expr-p.fact #p.expr0 - p.expr1

    @_('fact')
    def expr(self, p):
        return p.fact

    @_('fact TIMES basico')
    def fact(self, p):
        NodoProducto()
        return p.fact*p.basico

    @_('fact DIVIDE basico')
    def fact(self, p):
        NodoDivision()
        return p.fact/p.basico

    @_('basico')
    def fact(self, p):
        return p.basico

    @_('MINUS basico')
    def basico(self, p):
        NodoNeg()
        return -p.basico

    @_('ID') #Uso de la variable
    def basico(self, p): #Si el id no esta en la tabla, debe mostrar error.
        global eax
        if eax:
            print("movl "+str(tabla[p.ID][0])+"(%ebp), %ecx")
        else:
            print("movl "+str(tabla[p.ID][0])+"(%ebp), %eax")
            eax=True
        return tabla[p.ID][1]

    @_('NUM')
    def basico(self, p):
        global eax
        if eax:
            print("movl $"+str(p.NUM)+", %ecx")
        else:
            print("movl $"+str(p.NUM)+", %eax")
            eax=True
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
#entrada -> int a = 3;  a < 3;
#entrada -> int a = 3, b = 4; while( a >= 3) { a = a + 1; }
#entrada -> int a=1;if(a==1){while(1==1){a=a+1;}}
#entrada -> int a = 3, b = 4; while( a >= 3) { while(a == 2) {a = a + 1; }}
#Problemas: La insercion de variables en la pila se hace al reves.
