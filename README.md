This is a fork from [pymsasid](https://code.google.com/p/pymsasid/). pymsasid is a x86 disassembler completely written in python. It supports disassembling in two syntax - Intel and AT&T. This fork adds one more syntax - C like syntax(eg `add rax, 0x1` would be represented as `rax += 0x1`.

## C Syntax
Disassemblers disassemble machine code into human readable assembly code. Although assembly mnemonics are human readable they are not as easy as reading an C code. Adding C like disassembly might help to read through assembly code quickly without the help of architecture assembly manual. However the purpose of assembly mnemonics cant be ignored, so this syntax just adds the C like disassembly as supplement to AT&T syntax.

##Example

    push    ebp                             # ebp => stack
    mov     rbp, rsp                        # rbp = rsp
    push    ebx                             # ebx => stack
    sub     rsp, 0x8                        # rsp -= 0x8
    cmp     byte [rip+0x200be8], 0x0        # eflags._f = 0x0 - *((uint8_t)(rip+0x200be8))
    jnz     0x4dL                           # if (!eflags.zf) goto 0x4dL
    mov     rbx, 0x600e40                   # rbx = 0x600e40
    mov     rax, [rip+0x200be2]             # rax = *((rip+0x200be2))
    sub     rbx, 0x600e38                   # rbx -= 0x600e38
    sar     rbx, 0x3                        # rbx ->>= 0x3;
    sub     rbx, 0x1                        # rbx -= 0x1
    cmp     rax, rbx                        # eflags._f = rbx - rax
    jae     0x26L                           # if (!eflags.cf) goto 0x26L
    add     rax, 0x1                        # rax += 0x1
    mov     [rip+0x200bbd], rax             # *((rip+0x200bbd)) = rax
    call    qword [rax8+0x600e38]           # call *((uint64_t)(rax8+0x600e38))
    mov     rax, [rip+0x200baf]             # rax = *((rip+0x200baf))
    cmp     rax, rbx                        # eflags._f = rbx - rax
    jb      -0x1cL                          # if (eflags.cf) goto -0x1cL
    mov     byte [rip+0x200b9b], 0x1        # *((uint8_t)(rip+0x200b9b)) = 0x1
    add     rsp, 0x8                        # rsp += 0x8
    pop     ebx                             # ebx <= stack
    pop     ebp                             # ebp <= stack
    ret                                     # return

## How To Use
Checkout the example.py
