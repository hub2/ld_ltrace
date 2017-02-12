macros = """
DEFAULT REL
    extern dlsym
    section .text
%macro push_arg_regs 0
    push rdi
    push rsi
    push rdx
    push rcx
    push r8
    push r9
%endmacro
%macro pop_arg_regs 0
    pop r9
    pop r8
    pop rcx
    pop rdx
    pop rsi
    pop rdi
%endmacro

; 1 - addr
; 2 - size
write_addr:
    mov rax, 1
    mov rdi, 1
    syscall
    ret

fail:
    ret
[bits 64]"""

handler = """
    global {0}
{0}: ; podmien labelki
    push_arg_regs

    ; Print out the name of the called function
    lea rsi, [rel name_{0}_n]
    mov rdx, {1}
    call write_addr

    ; Find out address of the real function in the next library in dynamic linking chain
    mov rdi, 0xffffffffffffffff
    lea rsi, [rel name_{0}]
    call dlsym wrt ..plt


    ; Check if dlsym failed, if so, return, we cannot do any better than that
    test rax, rax
    pop_arg_regs
    jz fail

    call rax ; Call the real function
    ret
"""

data = """

name_{0}:
    db "{0}", 0
name_{0}_n:
    db "{0}", 10, 0

"""