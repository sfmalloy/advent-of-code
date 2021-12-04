
    .data
    .align 32
ARRAY:
    .zero 8000
    .text
    .global main
#==============================================================================
# print(int num) -> void
print:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rax

    xorq %rax, %rax
    movq %rdi, %rsi
    leaq PRINT_STR, %rdi
    callq printf

    popq %rax
    leave
    ret

#==============================================================================

read_input:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx              # Save callee-saved registers
    pushq %r12
    pushq %r13
    pushq %r14
    pushq %r15

    xorq %rsi, %rsi         # open arg 2 = O_RDONLY
    leaq FILENAME, %rdi     # open arg 1 = filename
    movq $2, %rax           # open syscall number
    syscall                 # call kernel
    movq %rax, %rbx         # Move file descriptor to rbx

    subq $144, %rsp         # Make room for struct stat (input_stat)
    leaq -144(%rbp), %rsi   # fstat arg 2 = address of input_stat
    movq %rbx, %rdi         # fstat arg 1 = file descriptor 
    movq $5, %rax           # fstat syscall number
    syscall                 # Call kernel

    xorq %r9, %r9           # mmap arg 6 = offset of 0
    movq %rbx, %r8          # mmap arg 5 = file descriptor
    movq $2, %r10           # mmap arg 4 = MAP_PRIVATE
    movq $1, %rdx           # mmap arg 3 = PROT_READ
    movq -96(%rbp), %rsi    # mmap arg 2 = input_stat.st_size
    xorq %rdi, %rdi         # mmap arg 1 = NULL
    movq $9, %rax           # mmap syscall number
    syscall                 # call kernel

    movq %rax, %r12         # Copy mmap return value into r12 for freeing later
    movq %r12, %r13         # Copy mmap return value into r13 for use with strtol
    subq $16, %rsp          # Make room for temp char*
    xorq %r14, %r14         # Zero out index

    movq -96(%rbp), %rsi    # munmap arg 2 = mem size in bytes to unmap
    movq %r12, %rdi         # munmap arg 1 = address to unmap
    movq $11, %rax          # munmap syscall number
    syscall

    movq %rbx, %rdi         # close arg 1 = file descriptor
    movq $3, %rax           # close sycall number
    syscall                 # call kernel

    addq $160, %rsp         # Free stack space used by fstat
    popq %r15               # Restore old callee-saved regsiters
    popq %r14
    popq %r13
    popq %r12
    popq %rbx
    leave
    ret

#==============================================================================

main:
    pushq %rbp
    movq %rsp, %rbp

    callq read_input
    movq N, %rdi

    xorl %eax, %eax
    leave
    ret

#==============================================================================
    .data
N:
    .long 2000
FILENAME:
    .asciz "inputs/Day01.in"
PRINT_STR:
    .asciz "%d\n"
DEBUG:
    .asciz "index = %d\n"
