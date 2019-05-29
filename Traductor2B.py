import sys
sys.path.append('../..')

from sly import Lexer, Parser
#usar $ tanto para & como para *
tabla = {} #Dictionary
labels = 0
labelsif=[]
endlabelswhile=[]
labelswhile=[]
eax=False
counterparameter = 0

def incrementparameter():
    global counterparameter
    counterparameter += 4

def resetparameter():
    global counterparameter
    counterparameter = 0

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
        global endlabelswhile,labels
        print("cmp $0,%eax")
        print("jne final"+str(labels))
        endlabelswhile.append(labels)
        incrementLabel()



class NodoIf():
    def __init__(self):
        global labels,labelsif
        print("cmp $0,%eax")
        print("je final"+str(labels))
        labelsif.append(labels)
        incrementLabel()


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

class beginFunction():
    def __init__(self, nombre):
        #resetparameter()
        print('.text')
        print('.globl ' + nombre)
        print('.type ' + nombre + ", @function")
        print(nombre + ":")

        print('pushl %ebp')
        print('movl %esp, %ebp')

class endFunction():
    def __init__(self):
        print('movl %ebp, %esp')
        print('popl %ebp')
        #print('movl $0, %eax')
        print('ret')


class CalcLexer(Lexer):
    tokens = {ID, TIPO, NUM, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, EQUAL, NEQUAL ,GREATER,
              IF, ELSE, WHILE, LKEY, RKEY, COMA, END, LESS, BIGGEROREQUAL, LESSOREQUAL, MAIN}
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['int'] = TIPO
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['main'] = MAIN
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

    #@_('function main_f')
    #def code(self, p):
    #    pass

    #@_('TIPO ID LPAREN RPAREN LKEY entrada RKEY')
    #def function(self, p):
    #    pass

    #@_(' ')
    #def function(self,p):
    #    pass

    @_('TIPO MAIN begin LPAREN RPAREN LKEY entrada RKEY main_f')
    def main_f(self, p):
        endFunction()

    @_('TIPO ID begin LPAREN parametro reserva RPAREN LKEY entrada RKEY main_f') #Funcion estándar
    def main_f(self, p):
        endFunction()

    @_(' ')
    def main_f(self, p):
        pass

    @_(' ')
    def begin(self, p):
        #print(p[-1]) #Hell yeah, accedemos al principio.
        beginFunction(p[-1])

    @_('TIPO ID resto')
    def parametro(self, p): #PEEERFECTO!!!!!
        #print('incrementado parametro ' + p.ID)
        incrementparameter()

    @_(' ')
    def parametro(self, p):
        pass

    @_('COMA parametro')
    def resto(self, p):
        pass

    @_(' ')
    def resto(self, p):
        pass

    @_(' ')
    def reserva(self, p):
        global counterparameter
        if counterparameter != 0:
            print('subl $' + str(counterparameter) + ", %esp")
            resetparameter()

    @_('asignacion END entrada')
    def entrada(self,p):
        pass

    @_('declaraciontipo END entrada')
    def entrada(self,p):
        pass

    @_('instruction entrada')
    def entrada(self,p):
        pass

    @_('')
    def entrada(self,p):
        pass

    @_('TIPO declaracion')
    def declaraciontipo(self,p):
        pass

    @_('ID valor empty5 restodeclaracion ')
    def declaracion(self,p):
        pass

    @_('')
    def empty5(self,p):
        global eax
        manejador.insertVar(p[-2], p[-1])#ID, valor
        NodoVariable()
        if eax:
            print("movl %eax, "+ str(tabla[p[-2]][0]) + "(%ebp)")
            eax=False
        else:
            print("movl %ecx, "+ str(tabla[p[-2]][0]) + "(%ebp)")

    @_('ID valor restoasignacion')#falta empty6
    def asignacion(self, p): #Falta buscar el valor en el sistema
        global eax
        eax=False
        manejador.insertValue(p.ID, p.valor)
        NodoAsign(p.ID, p.valor)


        #print('pasando por statement')
        #tabla[p.ID][1] = p.logic
        #print(tabla[p.ID])

    @_('ASSIGN logic')
    def valor(self,p):
        return p.logic

    @_('')
    def valor(self,p):
        pass

    @_('COMA asignacion')
    def restoasignacion(self,p):
        pass

    @_('')
    def restoasignacion(self,p):
        pass

    @_('COMA declaracion')
    def restodeclaracion(self,p):
        pass

    @_('')
    def restodeclaracion(self,p):
        pass

    @_('WHILE LPAREN empty1 empty2 entrada RKEY')
    def instruction(selfself, p):
        global labels,endlabelswhile
        print('jmp final' + str(labelswhile.pop()))
        print("final"+str(endlabelswhile.pop())+":")
        incrementLabel()
        global eax
        eax=False

    @_(" ")
    def empty1(self, p):
        global labels,labelswhile,endlabelswhile
        print("final"+str(labels)+":")
        labelswhile.append(labels)
        incrementLabel() #Imprimir la etiqueta actual

    @_("logic RPAREN LKEY")
    def empty2(self, p):
        global eax
        eax=False
        NodoWhile()
    #Comienzo del bucle while
    #@_('WHILE LPAREN empty1 empty2 statement RKEY')

    @_('IF LPAREN empty3 LKEY entrada RKEY elseif')
    def instruction(self,p):
        global eax
        eax=False

    @_('logic RPAREN')
    def empty3(self,p):
        global eax
        eax=False
        NodoIf()

    @_(' ')
    def elseif(self,p):
        global labels,labelsif
        print("final"+str(labelsif.pop())+":")
        incrementLabel()

    @_('empty4 entrada RKEY')
    def elseif(self,p):
        global labels,labelsif
        print("final"+str(labelsif.pop())+":")

    @_("ELSE LKEY")
    def empty4(self,p):
        global labels,labelsif
        print("jmp final"+str(labels))
        print("final"+str(labelsif.pop())+":")
        labelsif.append(labels)
        incrementLabel()

    """
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
    """

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

#entrada -> int main(){int a;}
#int funcion(){} int main(){}

#Problemas: La insercion de variables en la pila se hace al reves.
