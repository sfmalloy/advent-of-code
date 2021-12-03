    .data
ARRAY:
    .align 4
    .zero 8000
PRINT_STR:
    .asciz "%lld\n"
FILENAME:
    .asciz "inputs/Day01.in\0"
N:
    .long 2000

    .text
    .global main
#==============================================================================
# print(void) -> void
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
# part1(void) -> int
part1:
    pushq %rbp
    movq %rsp, %rbp

    movq $40, %rax

.part1_end:
    leave
    ret

#==============================================================================
# part2(void) -> int
part2:
    pushq %rbp
    movq %rsp, %rbp

    xorl %eax, %eax         # zero out counter
    leaq ARRAY, %rdi        # array pointer
    movl $2, %esi           # end index
.part2_loop:
    cmpl N, %esi
    je .part2_end

    movl 12(%rdi), %ecx
    cmp (%rdi), %ecx        # if *(ARRAY+12) > *ARRAY then jump to .L03
    jg .L03
    jmp .L04
.L03:
    inc %eax                # increment counter
.L04:
    inc %esi                # increment index
    addq $4, %rdi           # move array pointer
    jmp .part2_loop          # jump to start of loop
.part2_end:
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
    leaq ARRAY, %r15        # Save address of ARRAY

.input_loop:
    leaq -160(%rbp), %rdi   # Address of memory pointer (char**)
    movq %rdi, -152(%rbp)   # Save address on stack

    movq $10, %rdx          # strtol arg 3 = base 10
    movq -152(%rbp), %rsi   # strtol arg 2 = Address of char* for advancing mem ptr
    movq %r13, %rdi         # strtol arg 1 = mem ptr
    call strtol

    movq %rax, (%r15)       # Move strtol result into array
    addq $4, %r15           # Advance array pointer
    movq -160(%rbp), %r13   # Advance to next line

    inc %r14                # Increment index
    cmpq N, %r14            # compare N to index
    jl .input_loop
.input_loop_end:
    movq %r14, %rsi
    movq $PRINT_STR, %rdi
    callq printf

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

    movq $40, %rdi
    callq print

    xorl %eax, %eax
    leave
    ret

#==============================================================================

