from sly import Lexer, Parser

profundidad=0
variablesPila={}# Id----Profundidad en la pila
#variables globales tiene profundidad cero
variablesValor={}
etiquetas=-1


class NodoOR:
    def __init__(self,x,y):
        print("pop %eax")
        print("cmpl $0, %eax")
        print("jne finalOR")#meter contandor
        print("pop %eax")




class BottomUpLexer(Lexer):
    tokens = {IF, WHILE, ELSE, ID, NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, ASSIGN, AND, OR, NOT, BIGGER, SMALLER, EQUAL,NOTEQUAL ,BIGGEROREQUAL,SMALLEROREQUAL,CADENA,PRINTF,INT,FLOAT,CHAR}
    literals = {';', '"', ',','(',')','{','}'}

    ignore = ' \t'

    NUMBER = r'\d+'

    #CADENA = r'[a-z]'
    ID = r'[a-zA-Z][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['int'] = INT
    ID['float'] = FLOAT
    ID['char'] = CHAR
    #ID['printf'] = PRINTF
    EQUAL = r'=='
    NOTEQUAL= r'!='
    BIGGEROREQUAL= r'>='
    SMALLEROREQUAL=r'<='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    AND = r'&&'
    OR = r'\|\|'
    NOT = r'!'
    BIGGER = r'>'
    SMALLER = r'<'
    ASSIGN = r'='
    #CADENA =r'[a-zA-Z0-9%]*' # COMPROBAR ESTO


    @_(r'\d+') # si no pones esto te trata los numeros como string
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno+= t.value.count('\n')

    def error(self, t):
        print('error')
        self.index += 1

class BottomUpParser(Parser):
    tokens=BottomUpLexer.tokens

    def __init__(self):
        self.names={}

    @_('tipo asig ";" entrada')
    def entrada(self,p):
        pass

    @_(' ')
    def entrada(self,p):
        pass

    @_('INT')
    def tipo(self,p):
        print("subl $4, %esp")

    @_('CHAR')
    def tipo(self,p):
        print("subl $4, %esp")

    @_('FLOAT')
    def tipo(self,p):
        print("subl $4, %esp")

    @_('ID igual')
    def asig(self,p):
        global profundidad
        profundidad=profundidad-4
        #hay que comprobar que no se repite
        variablesPila[p.ID] = profundidad#comprobar
        variablesValor[p.ID]= p.igual

    @_('ASSIGN logicOR assignExtra')
    def igual(self,p):
        return p.logicOR

    @_(' ')
    def igual(Self,p):
        pass

    @_('"," asig')
    def assignExtra(self,p):
        pass

    @_(' ')
    def assignExtra(self,p):
        pass

    @_('logicOR OR bool')
    def logicOR(self,p):
        global etiquetas
        #NodoOR(p.op,p.logic)
        etiquetas=etiquetas+1
        print("popl %edx")
        print("movl $1,%eax")
        print("cmp $0, %edx")
        print("jne final"+str(etiquetas))
        print("popl %edx")
        print("cmp $0, %edx")
        print("jne final"+str(etiquetas))
        print("     movl $0, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.logicOR or p.bool

    @_('bool')
    def logicOR(self,p):
        return p.bool

    @_('logicAND')
    def bool(self,p):
        return p.logicAND

    @_('logicAND AND op')
    def logicAND(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %edx")
        print("movl $0,%eax")
        print("cmp $0, %edx")
        print("je final"+str(etiquetas))
        print("popl %edx")
        print("cmp $0, %edx")
        print("je final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.logicAND and p.op

    @_('op')
    def logicAND(self,p):
        return p.op

    @_('NOT logicOR')
    def op(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %edx")
        print("movl $0,%eax")
        print("cmp $0, %edx")
        print("jne final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return not p.logicOR

    @_('rel')
    def op(self,p):
        return p.rel

    @_('rel SMALLER arit')#<
    def rel(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %eax")
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("popl %ecx")
        print("cmp %edx, %ecx")
        print("jg final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.rel < p.arit

    @_('rel BIGGER arit')#>
    def rel(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %eax")
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("popl %ecx")
        print("cmp %edx, %ecx")
        print("jle final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.rel > p.arit

    @_('rel SMALLEROREQUAL arit')#<=
    def rel(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %eax")
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("popl %ecx")
        print("cmp %edx, %ecx")
        print("jg final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.rel <= p.arit

    @_('rel BIGGEROREQUAL arit')#>=
    def rel(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %eax")
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("popl %ecx")
        print("cmp %edx, %ecx")
        print("jl final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.rel >= p.arit

    @_('rel EQUAL arit')
    def rel(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %eax")
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("popl %ecx")
        print("cmp %edx, %ecx")
        print("jne final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.rel==p.arit

    @_('rel NOTEQUAL arit')
    def rel(self,p):
        global etiquetas
        etiquetas=etiquetas+1
        print("popl %eax")
        print("movl %eax,%edx")
        print("movl $0,%eax")
        print("popl %ecx")
        print("cmp %edx, %ecx")
        print("je final"+str(etiquetas))
        print("     movl $1, %eax")
        print("final"+str(etiquetas)+":")
        print("pushl %eax")
        return p.rel != p.arit

    @_('arit')
    def rel(self,p):
        return p.arit

    @_('arit PLUS sum')
    def arit(self,p):
        print("popl %eax")
        print("popl %ecx")
        print("addl %ecx, %eax")
        print("pushl %eax")
        return p.arit+p.sum

    @_('arit MINUS sum')
    def arit(self,p):
        print("popl %eax")
        print("popl %ecx")
        print("subl %ecx, %eax")
        print("pushl %eax")
        return p.arit-p.sum

    @_('sum')
    def arit(self,p):
        return p.sum

    @_('sum TIMES fact')
    def sum(self,p):
        print("popl %eax")
        print("popl %ecx")
        print("addl %ecx, %eax")
        print("pushl %eax")
        return p.sum * p.fact

    @_('sum DIVIDE fact')
    def sum(self,p):
        print("popl %eax")
        print("popl %ecx")
        print("cdq")
        print("divl %ecx")
        print("pushl %eax")
        return p.sum // p.fact

    @_('fact')
    def sum(self,p):
        return p.fact

    @_('MINUS fact')
    def fact(self,p):
        print("popl %eax")
        print("negl %eax")
        print("pushl %eax")
        return -p.fact

    @_('NUMBER')
    def fact(self,p):
        print("movl $"+str(p.NUMBER)+", %eax")
        print("pushl %eax")
        return p.NUMBER

    @_('ID')
    def fact(self,p):
        print("movl %ebp("+str(variablesPila[p.ID])+"), %eax")
        print("pushl %eax")
        return variablesValor[p.ID]

if __name__ == '__main__':
    lexer = BottomUpLexer()
    parser = BottomUpParser()

    while True:
        text = input("introduce una operacion: ")

        if text:
            parser.parse(lexer.tokenize(text))
