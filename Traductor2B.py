import sys
sys.path.append('../..')

from sly import Lexer, Parser
#usar $ tanto para & como para *
tabla = {}
contenedor = {} #Diccionario con todas las tablas.
labels = 0
labelsprintf=0
nivel=1
varprintf=[]
valueprintf=[]
labelsif=[]
endlabelswhile=[]
labelswhile=[]
tablaVectores={}
decla=False
asig=False
eax=False
prinfvar=0
printfstring=""
longitud=[]
vectores={}
vector=False
counterparameter = 0
declavar={}
declavalue=[]
f=open("Ensamblador.S","w")

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
    def aumentarcontador(self):
        self.contador-=4

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
        f.write("subl $"+str(4*tam)+", %esp\n")

class NodoAsign():
    def __init__(self, variable, valor,tam):
        if tam<=-1:
            if valor == None:
                f.write("movl %eax, " + str(tabla[variable][0]) + "(%ebp)\n")
            else:
                if type(valor) is str:
                    f.write("movl "+str(tabla[variable][0])+"(%ebp) ,"+str(tabla[variable][0]) + "(%ebp)\n")
                else:
                    if eax:
                        f.write("movl %eax ," + str(tabla[variable][0]) + "(%ebp)\n")
                    else:
                        f.write("movl $" + str(valor) + ", " + str(tabla[variable][0]) + "(%ebp)\n")
        else:
            if tam>0:
                variable=variable+str(tam)
            if valor == None:
                f.write("movl %eax, " + str(tabla[variable][0]) + "(%ebp)\n")
            else:
                if type(valor) is str:
                    f.write("movl "+str(tabla[variable][0])+"(%ebp) ,"+str(tabla[variable][0]) + "(%ebp)\n")
                else:
                    if eax:
                        f.write("movl %eax ," + str(tabla[variable][0]) + "(%ebp)\n")
                    else:
                        f.write("movl $" + str(valor) + ", " + str(tabla[variable][0]) + "(%ebp)\n")


class NodoSuma():
    def __init__(self):
        f.write("addl %ecx, %eax\n")
        #f.write("movl %eax, " + str1)

class NodoResta():
    def __init__(self):
        f.write("subl %ecx, %eax\n")

class NodoProducto():
    def __init__(self):
        f.write("imull %ecx, %eax\n")

class NodoDivision():
    def __init__(self):
        f.write("cdq\n")
        f.write("divl %ecx\n")

class NodoEqual():
    def __init__(self):
        global labels
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp %edx, %ecx\n")
        f.write("jne final"+str(labels)+"\n")
        f.write("movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()


class NodoNequal():
    def __init__(self):
        global labels
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp %edx, %ecx\n")
        f.write("je final"+str(labels)+"\n")
        f.write("movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoGreater():
    def __init__(self):
        global labels
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp %edx, %ecx\n")
        f.write("jle final"+str(labels)+"\n")
        f.write("movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()


class NodoSmaller():
    def __init__(self):
        global labels
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp %edx, %ecx\n")
        f.write("jg final"+str(labels)+"\n")
        f.write(" movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoSmallerEqual():
    def __init__(self):
        global labels
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp %edx, %ecx\n")
        f.write("jg final"+str(labels)+"\n")
        f.write(" movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoGreaterEqual():
    def __init__(self):
        global labels
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp %edx, %ecx\n")
        f.write("jl final"+str(labels)+"\n")
        f.write(" movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoNeg():##Problema con esto
    def __init__(self):
        global eax
        if eax:
            f.write("negl %eax\n")
        else:
            f.write("negl %ecx\n")


class NodoNot():#aqui
    def __init__(self):
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp $0, %edx\n")
        f.write("jne final"+str(labels)+"\n")
        f.write("movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoAnd():
    def __init__(self):
        f.write("movl %eax,%edx\n")
        f.write("movl $0,%eax\n")
        f.write("cmp $0, %edx\n")
        f.write("je final"+str(labels)+"\n")
        f.write("movl %ecx,%edx\n")
        f.write("cmp $0, %edx\n")
        f.write("je final"+str(labes)+"\n")
        f.write("movl $1, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoOr():
    def __init__(self):
        f.write("movl %eax,%edx\n")
        f.write("movl $1,%eax\n")
        f.write("cmp $0, %edx\n")
        f.write("jne final"+str(labels)+"\n")
        f.write("movl %ecx,%edx\n")
        f.write("cmp $0, %edx\n")
        f.write("jne final"+str(labels)+"\n")
        f.write("movl $0, %eax\n")
        f.write("final"+str(labels)+":\n")
        incrementLabel()

class NodoWhile():
    def __init__(self):
        global endlabelswhile,labels
        f.write("cmp $0,%eax\n")
        f.write("jne final"+str(labels)+"\n")
        endlabelswhile.append(labels)
        incrementLabel()



class NodoIf():
    def __init__(self):
        global labels,labelsif
        f.write("cmp $0,%eax\n")
        f.write("je final"+str(labels)+"\n")
        labelsif.append(labels)
        incrementLabel()


class NodoLogic():
    def __init__(self,  valor1, op, valor2):
        self. valor1 = valor1
        self.op = op
        self.valor2 = valor2

    def escribir(self):
        #Averiguar en que posicion esta la variable que buscas.
        f.write( "cmp " + manejador.cadena(self.valor2) + "," + manejador.cadena(self.valor1)+"\n")

    def salto(self):
        global labels
        if self.op == '!=':
            f.write("je L" + str(labels + 1)+"\n")
        if self.op == '==':
            f.write("jne L" + str(labels + 1)+"\n")
        if self.op == '<':
            f.write("jl L" + str(labels + 1)+"\n")
        if self.op == '>':
            f.write("jg L" + str(labels + 1)+"\n")
        if self.op == '<=':
            f.write("jle L" + str(labels + 1)+"\n")
        if self.op == '>=':
            f.write("jge L" + str(labels + 1)+"\n")

class beginFunction():
    def __init__(self, nombre):
        #resetparameter()
        f.write('.text\n')
        f.write('.globl ' + nombre+"\n")
        f.write('.type ' + nombre + ", @function\n")
        f.write(nombre + ":\n")

        f.write('pushl %ebp\n')
        manejador.aumentarcontador()
        f.write('movl %esp, %ebp\n')

class endFunction():
    def __init__(self):
        f.write('movl %ebp, %esp\n')
        f.write('popl %ebp\n')
        f.write('ret\n')

class CalcLexer(Lexer):
    tokens = {ID, TIPO, NUM, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, EQUAL, NEQUAL ,GREATER,
              IF, ELSE, WHILE, LKEY, RKEY, COMA, END, LESS, BIGGEROREQUAL, LESSOREQUAL, MAIN, RETURN,RCORCHERTE,LCORCHETE,DIRECC,PRINTF,CADENA,SCANF}
    ignore = ' \t'

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    CADENA =r'"[a-zA-Z0-9% ]*"' # COMPROBAR ESTO
    ID['int'] = TIPO
    ID['void'] = TIPO
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    #ID['for']=FOR
    ID['main'] = MAIN
    ID['return'] = RETURN
    ID['printf'] = PRINTF
    ID['scanf']=SCANF

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
    DIRECC=r'&'


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
        #f.write(p[-1]) #Hell yeah, accedemos al principio.
        beginFunction(p[-1])

    @_('TIPO ID resto')
    def parametro(self, p): #PEEERFECTO!!!!!
        #f.write('incrementado parametro ' + p.ID)
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
            f.write('subl $' + str(counterparameter) + ", %esp\n")
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

    @_('imprimir END entrada')
    def entrada(self,p):
        pass

    @_('escanear END entrada')
    def entrada(self,p):
        pass

    @_('PRINTF LPAREN  CADENA empty9 idextra empty8 RPAREN')
    def imprimir(self,p):
        global varprintf,asig
        imprimir=p.CADENA
        imprimir=imprimir.split("%d")
        printfstring=""
        for i in range(0,len(imprimir)):
            printfstring=printfstring+imprimir[i]
            if varprintf:
                printfstring=printfstring+str((tabla[varprintf.pop()][1]))
        #print(printfstring)
        del varprintf[:]
        asig=False

    @_('SCANF LPAREN  CADENA empty9 idextra empty10 RPAREN')
    def escanear(self,p):
        pass

    @_(' COMA basico idextra')
    def idextra(self,p):
        global varprintf
        varprintf.append(p.basico)

    @_(' COMA DIRECC basico idextra')
    def idextra(self,p):
        global varprintf
        varprintf.append(p.basico)

    @_(' ')
    def idextra(self,p):
        pass

    @_('')
    def empty8(self,p):
        global labelsprintf,varprintf,tabla
        for i in range(0,len(varprintf)):
            f.write("pushl "+str(tabla[varprintf[i]][0])+"(%ebp)\n")
        f.write("pushl $s"+str(labelsprintf)+"\n")
        f.write("call printf\n")
        labelsprintf=labelsprintf+1

    @_('')
    def empty10(self,p):
        global labelsprintf,varprintf,tabla
        for i in range(0,len(varprintf)):
            f.write("leal "+str(tabla[varprintf[i]][0])+"(ebp), %eax\n")
            f.write("pushl %eax\n")
        f.write("pushl $s"+str(labelsprintf)+"\n")
        f.write("call scanf\n")
        labelsprintf=labelsprintf+1

    @_('')
    def empty9(self,p):
        global asig
        asig=True

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
                    f.write("movl $"+str(var)+", %eax\n")
                    f.write("movl %eax, "+ str(tabla[value][0]) + "(%ebp)\n")
                else:
                    if type(value) is str:
                        try:
                            manejador.insertVar(value,declavar[var],tam)#ID, valor
                            NodoVariable(tam)
                            f.write("movl $"+str(declavar[var])+", %eax\n")
                            f.write("movl %eax, "+ str(tabla[value][0]) + "(%ebp)\n")
                        except:
                            manejador.insertVar(value,tabla[var][1],tam)#ID, valor
                            NodoVariable(tam)
                            if(tam>0):
                                f.write("movl  "+str(tabla[var][0])+"(%ebp), "+ str(tabla[value][0]) + "(%ebp)\n")

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
        global decla,nivel
        if nivel!=1:
            raise NameError("Declaracion anidada")
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
        f.write('call ' + p.ID+"\n")
        f.write('addl ' + str(counterparameter) + ", %esp\n")
        resetparameter()

    @_(' ')
    def argumentos(self, p):
        pass

    @_('ID restoargumentos')
    def argumentos(self, p):
        f.write("pushl " + manejador.cadena(p.ID)+"\n")#p.ID)
        incrementparameter()

    @_('COMA argumentos')
    def restoargumentos(self, p):
        pass

    @_(' ')
    def restoargumentos(self, p):
        pass

    @_('RETURN logic END')
    def instruction(self, p):
        #f.write('movl ' + manejador.cadena(p.logic) + ", %eax")
        #f.write('ret')
        #endFunction() Hace falta en la tabla un marcador inicio-fin funcion
        pass

    @_('WHILE LPAREN empty1 empty2 entrada RKEY')
    def instruction(self, p):
        global labels,endlabelswhile,nivel
        f.write('jmp final' + str(labelswhile.pop())+"\n")
        f.write("final"+str(endlabelswhile.pop())+":\n")
        incrementLabel()
        global eax
        eax=False
        nivel-=1

    @_(" ")
    def empty1(self, p):
        global labels,labelswhile,endlabelswhile,nivel
        nivel+=1
        f.write("final"+str(labels)+":\n")
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
        nivel-=1

    @_('logic RPAREN')
    def empty3(self,p):
        global eax,nivel
        nivel+=1
        eax=False
        NodoIf()

    @_(' ')
    def elseif(self,p):
        global labels,labelsif
        f.write("final"+str(labelsif.pop())+":\n")
        incrementLabel()

    @_('empty4 entrada RKEY')
    def elseif(self,p):
        global labels,labelsif
        f.write("final"+str(labelsif.pop())+":\n")

    @_("ELSE LKEY")
    def empty4(self,p):
        global labels,labelsif
        f.write("jmp final"+str(labels))
        f.write("final"+str(labelsif.pop())+":\n")
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
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %ecx\n")
                else:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %eax\n")
                    eax=True
                return tabla[var][1]
            else:
                if eax:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %ecx\n")
                else:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %eax\n")
                    eax=True
                asig=True
                return var
        else:
            return var

    @_('DIRECC ID dimasig')
    def basico(self,p):
        global eax,decla,asig
        var=p.ID
        if p.dimasig>0:
            var=var+str(p.dimasig)
        if not decla:
            if not asig:
                if eax:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %ecx\n")
                else:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %eax\n")
                    eax=True
                return tabla[var][1]
            else:
                if eax:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %ecx\n")
                else:
                    f.write("movl "+str(tabla[var][0])+"(%ebp), %eax\n")

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
                f.write("movl $"+str(p.NUM)+", %ecx\n")
            else:
                f.write("movl $"+str(p.NUM)+", %eax\n")
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
        f.close()
        with open("Ensamblador.S", 'r') as reader:
            for line in reader:
                print(line,end='')

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
