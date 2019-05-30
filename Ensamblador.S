.text
.globl main
.type main, @function
main:
pushl %ebp
movl %esp, %ebp
subl $4, %esp
movl $8, %eax
movl %eax, -8(%ebp)
movl -8(%ebp), %eax
leal -8(ebp), %eax
pushl %eax
pushl $s0
call scanf
movl %ebp, %esp
popl %ebp
ret
