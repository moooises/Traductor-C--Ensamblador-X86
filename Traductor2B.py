import sys
sys.path.append('../..')

from sly import Lexer, Parser
#usar $ tanto para & como para *
tabla = {}
contenedor = {} #Diccionario con todas las tablas.
labels = 0
labelsif=[]
endlabelswhile=[]
labelswhile=[]
tablaVectores={}
decla=False
asig=False
eax=False
longitud=[]
vectores={}
vector=False
counterparameter = 0
declavar={}
declavalue=[]

def incrementparameter():
    global counterparameter
    counterparameter += 4

def resetparameter():
    global counterparameter
    counterparameter = 0

class Tabla():
    contador = 0
    #selector = 0
    #def selectTable(self, id):
    #    if id in selector:
    #        self.selector = tabla[id]

    def insertVar(self, var, value,tam):
        if var in tabla:
            raise NameError('Variable ' + "\"" + str(var) + "\"" + ' declarada anteriormente')
        else:
            if int(tam)<=1:
                self.contador-= 4
                tabla[var] = [self.contador, value]
            else:
                for i in range(0,int(tam)):
                    self.contador-= 4
                    if i==0:
                        tabla[var] = [self.contador, 0]
                    else:
                        tabla[var+str(i)]=[self.contador, 0]

    def insertValue(self, var, value,tam):
        if var in tabla:
            if tam<=-1:
                tabla[var][1] = value #Modificamos el campo valor de la variable.
            else:
                if tam==0:
                    tabla[var][1] = value
                else:
                    tabla[var+str(tam)][1] = value

                #for i in range(0,vectores[var]):
                #    if i==0:
                #        if tabla[var][2]==tam:
                #            tabla[var][1] = value
                #    else:
                #        if tabla[var+str(i)][2]==tam:

        else:
            raise NameError('Variable ' + "\"" + str(var) + "\"" + 'no declarada')
        #print(tabla)

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
    #print('L' + str(labels) + ':')
def decrementLabel(): #Lo uso en el while.
    global labels
    labels = labels - 1


class NodoVariable():
    def __init__(self,tam):
        tam=int(tam)
        if tam==-1:
            tam=1
        print("subl $"+str(4*tam)+", %esp")

class NodoAsign():
    def __init__(self, variable, valor,tam):
        if tam<=-1:
            if valor == None:
                print("movl %eax, " + str(tabla[variable][0]) + "(%ebp)")
            else:
                if type(valor) is str:
                    print("movl "+str(tabla[variable][0])+"(%ebp) ,"+str(tabla[variable][0]) + "(%ebp)")
                else:
                    if eax:
                        print("movl %eax ," + str(tabla[variable][0]) + "(%ebp)")
                    else:
                        print("movl $" + str(valor) + ", " + str(tabla[variable][0]) + "(%ebp)")
        else:
            if tam>0:
                variable=variable+str(tam)
            if valor == None:
                print("movl %eax, " + str(tabla[variable][0]) + "(%ebp)")
            else:
                if type(valor) is str:
                    print("movl "+str(tabla[variable][0])+"(%ebp) ,"+str(tabla[variable][0]) + "(%ebp)")
                else:
                    if eax:
                        print("movl %eax ," + str(tabla[variable][0]) + "(%ebp)")
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
        print('ret')

class CalcLexer(Lexer):
    tokens = {ID, TIPO, NUM, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, EQUAL, NEQUAL ,GREATER,
              IF, ELSE, WHILE, LKEY, RKEY, COMA, END, LESS, BIGGEROREQUAL, LESSOREQUAL, MAIN, RETURN,RCORCHERTE,LCORCHETE}
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['int'] = TIPO
    ID['void'] = TIPO
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['main'] = MAIN
    ID['return'] = RETURN
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
    RCORCHERTE=r'\]'
    LCORCHETE=r'\['


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
        pass
    @_('TIPO ID begin LPAREN parametro reserva RPAREN LKEY entrada RKEY main_f') #Funcion estándar
    def main_f(self, p):
        endFunction()
        pass
    @_(' ')
    def main_f(self, p):
        pass

    @_(' ')
    def begin(self, p):
        global tabla
        #manejador.tabla = {}
        tabla = {}
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

    @_('asignacion END  entrada')
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

    @_('TIPO empty5 declaracion')
    def declaraciontipo(self,p):
        global decla,declavalue,declavar,tabla,longitud,tablaVectores,vectores
        decla=False
        #for i in range(0,len(declavar)):
        longitud.reverse()
        for i in range(0,len(declavar)):
            value=declavalue.pop()
            var=declavar[value]
            tam=longitud.pop()
            if tam>=1:
                vectores[value]=tam

            if var==None:
                manejador.insertVar(value,0,tam)#ID, valor
                NodoVariable(tam)
            else:
                if type(var) is int:
                    manejador.insertVar(value,var,tam)#ID, valor
                    NodoVariable(tam)
                    print("movl $"+str(var)+", %eax")
                    print("movl %eax, "+ str(tabla[value][0]) + "(%ebp)")
                else:
                    if type(value) is str:
                        try:
                            manejador.insertVar(value,declavar[var],tam)#ID, valor
                            NodoVariable(tam)
                            print("movl $"+str(declavar[var])+", %eax")
                            print("movl %eax, "+ str(tabla[value][0]) + "(%ebp)")
                        except:
                            manejador.insertVar(value,tabla[var][1],tam)#ID, valor
                            NodoVariable(tam)
                            if(tam>0):
                                print("movl  "+str(tabla[var][0])+"(%ebp), "+ str(tabla[value][0]) + "(%ebp)")

                    else:
                        manejador.insertVar(var,0,tam)#ID, valor
                        NodoVariable(tam)

        vector=False
        declavar.clear()
        del declavalue[:]
        del longitud[:]

    @_('ID dim valordec empty6 restodeclaracion')
    def declaracion(self,p):
        global longitud
        if int(p.dim)>1 and p.valordec!=None:
            raise NameError('Inicializacion de vector erronea')
        longitud.append(p.dim)


    @_('')
    def empty5(self,p):
        global decla
        decla=True


    @_('ID dimasig valorasig empty7 restoasignacion')#falta empty6
    def asignacion(self, p): #Falta buscar el valor en el sistema
        pass

    @_(' ')
    def empty7(self,p):
        global eax,asig,decla,vectores
        tam=-1
        if int(p[-2])>-1:
            v=vectores[p[-3]]
            if v!=None:
                if int(p[-2])>v or int(p[-2])<0:
                    raise NameError('Sobrepasada la longitud del vector '+p[-3])
                else:
                    tam=int(p[-2])
            else:
                raise NameError('Variable '+p[-3]+' no es un vector')


        asig=True
        manejador.insertValue(p[-3], p[-1],tam)
        NodoAsign(p[-3], p[-1],tam)
        asig=False
        eax=False

    @_('ASSIGN logic dimasig')
    def valordec(self,p):
        if p.dimasig>-1:
            if p.dimasig==0:
                return tabla[p[-5]][1]
            else:
                return tabla[p[-5]+str(p.dimasig)][1]
        else:
            return p.logic


    @_('')
    def valordec(self,p):
        pass

    @_('ASSIGN logic dimasig')
    def valorasig(self,p):
        if p.dimasig>1:
            if p.dimasig==0:
                return tabla[p[-5]][1]
            else:
                return tabla[p[-5]+str(p.dimasig)][1]
        else:
            return p.logic


    @_('')
    def valorasig(self,p):
        pass

    @_('LCORCHETE NUM RCORCHERTE dim')
    def dim(self,p):
            return int(p.NUM)*p.dim
    @_('')
    def dim(self,p):
        return 1

    @_('LCORCHETE NUM RCORCHERTE dimasig')
    def dimasig(self,p):
        if int(p.NUM)==1 and p.dimasig==-1:
             return 1
        else:
            return int(p.NUM)*p.dimasig
    @_('')
    def dimasig(self,p):
        return -1

    @_(' ')
    def empty6(self,p):
        global declavalue,declavar
        declavar[p[-3]]=p[-1]
        declavalue.append(p[-3])


    @_('COMA asignacion ')
    def restoasignacion(self,p):
        pass

    @_('')
    def restoasignacion(self,p):
        global asig
        asig=False

    @_('COMA declaracion ')
    def restodeclaracion(self,p):
        pass

    @_('')
    def restodeclaracion(self,p):
        pass

    @_('ID LPAREN argumentos RPAREN END')
    def instruction(self, p):
        global counterparameter
        print('call ' + p.ID)
        print('addl ' + str(counterparameter) + ", %esp")
        resetparameter()

    @_(' ')
    def argumentos(self, p):
        pass

    @_('ID restoargumentos')
    def argumentos(self, p):
        print("pushl " + manejador.cadena(p.ID))#p.ID)
        incrementparameter()

    @_('COMA argumentos')
    def restoargumentos(self, p):
        pass

    @_(' ')
    def restoargumentos(self, p):
        pass

    @_('RETURN logic END')
    def instruction(self, p):
        #print('movl ' + manejador.cadena(p.logic) + ", %eax")
        #print('ret')
        #endFunction() Hace falta en la tabla un marcador inicio-fin funcion
        pass

    @_('WHILE LPAREN empty1 empty2 entrada RKEY')
    def instruction(self, p):
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

    @_('logic EQUAL logicpr')
    def logic(self, p):
        NodoEqual()
        if type(p.logic) is str:
            return tabla[p.logic][1]==p.logicpr
        else:
            return p.logic == p.logicpr
        #return NodoLogic(p.logic, p.EQUAL, p.logicpr)

    @_('logic NEQUAL logicpr')
    def logic(self, p):
        NodoNequal()
        if type(p.logic) is str:
            return tabla[p.logic][1]!=p.logicpr
        else:
            return p.logic != p.logicpr

    @_('logicpr')
    def logic(self, p):
        return p.logicpr #Perfe, debería subir el nodo.

    @_('logicpr LESSOREQUAL expr')
    def logicpr(self, p):
        NodoSmallerEqual()
        if type(p.logicpr) is str:
            return tabla[p.logicpr][1]<=p.pexpr
        else:
            return p.logicpr <= p.expr

    @_('logicpr BIGGEROREQUAL expr')
    def logicpr(self, p):
        NodoGreaterEqual()
        if type(p.logicpr) is str:
            return tabla[p.logicpr][1]>=p.pexpr
        else:
            return p.logicpr >= p.expr

    @_('logicpr GREATER expr')
    def logicpr(self, p):
        NodoGreater()
        if type(p.logicpr) is str:
            return tabla[p.logicpr][1]>p.pexpr
        else:
            return p.logicpr > p.expr

    @_('logicpr LESS expr')
    def logicpr(self, p):
        NodoSmaller()
        if type(p.logicpr) is str:
            return tabla[p.logicpr][1]<p.pexpr
        else:
            return p.logicpr < p.expr

    @_('expr')
    def logicpr(self, p):
        return p.expr

    @_('expr PLUS fact')
    def expr(self, p):
        global tabla,eax
        NodoSuma()
        if type(p.expr) is str:
            return tabla[p.expr][1]+p.fact
        else:
            return p.expr+p.fact

    @_('expr MINUS fact')
    def expr(self, p):
        NodoResta()
        if type(p.expr) is str:
            return tabla[p.expr][1]-p.fact
        else:
            return p.expr-p.fact #p.expr0 - p.expr1

    @_('fact')
    def expr(self, p):
        return p.fact

    @_('fact TIMES basico')
    def fact(self, p):
        NodoProducto()
        if type(p.fact) is str:
            return tabla[p.fact][1]*p.basico
        else:
            return p.fact*p.basico

    @_('fact DIVIDE basico')
    def fact(self, p):
        NodoDivision()
        if type(p.fact) is str:
            return tabla[p.fact][1]/p.basico
        else:
            return p.fact/p.basico

    @_('basico')
    def fact(self, p):
        return p.basico

    @_('MINUS basico')
    def basico(self, p):
        NodoNeg()
        return -p.basico

    @_('ID dimasig') #Uso de la variable
    def basico(self, p): #Si el id no esta en la tabla, debe mostrar error.
        global eax,decla,asig
        var=p.ID
        if p.dimasig>0:
            var=var+str(p.dimasig)
        if not decla:
            if not asig:
                if eax:
                    print("movl "+str(tabla[var][0])+"(%ebp), %ecx")
                else:
                    print("movl "+str(tabla[var][0])+"(%ebp), %eax")
                    eax=True
                return tabla[var][1]
            else:
                if eax:
                    print("movl "+str(tabla[var][0])+"(%ebp), %ecx")
                else:
                    print("movl "+str(tabla[var][0])+"(%ebp), %eax")
                    eax=True
                asig=True
                return var
        else:
            return var

    @_('NUM')
    def basico(self, p):
        global eax,decla
        if not decla:
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

    if len(sys.argv) == 2:
        dir = './' + sys.argv[1]
        reader = open(dir, 'r')
        text = reader.read()
        parser.parse(lexer.tokenize(text))
    else:
        print("Este programa necesita un parámetro");

    """
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
    """
#entrada -> int a = 3, b = 4; while( a != 3) { a = a + 1; }
#entrada -> int a = 3, b =4; a = a +b;
#entrada -> int a = 3;  a < 3;
#entrada -> int a = 3, b = 4; while( a >= 3) { a = a + 1; }

#entrada -> int main(){int a;}
#int funcion(){} int main(){}
# int funcion(int a, int b){ int a;} int main(){int a;}

#Problemas: La insercion de variables en la pila se hace al reves.
