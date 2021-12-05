    .text
    .global solve
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

# part1(void) -> int
part1:
    pushq %rbp
    movq %rsp, %rbp

    xorl %eax, %eax         # zero out counter
    leaq ARRAY, %rdi        # array pointer
    movl $1, %esi           # index
part1_loop:
    cmpl N, %esi            # compare to index
    je part1_end

    movl 4(%rdi), %ecx      
    cmpl (%rdi), %ecx       # if *(ARRAY+1) > *ARRAY then jump to .L01
    jg .L01
    jmp .L02
.L01:
    inc %eax                # increment counter
.L02:
    inc %esi                # increment index
    addq $4, %rdi           # move array pointer
    jmp part1_loop          # jump to start of loop
part1_end:
    leave
    ret
#==============================================================================

# part1(void) -> int
part2:
    pushq %rbp
    movq %rsp, %rbp

    xorl %eax, %eax         # zero out counter
    leaq ARRAY, %rdi        # array pointer
    movl $3, %esi           # index
part2_loop:
    cmpl N, %esi            # compare to index
    je part1_end

    movl 12(%rdi), %ecx      
    cmpl (%rdi), %ecx       # if *(ARRAY+3) > *ARRAY then jump to .L01
    jg .L03
    jmp .L04
.L03:
    inc %eax                # increment counter
.L04:
    inc %esi                # increment index
    addq $4, %rdi           # move array pointer
    jmp part2_loop          # jump to start of loop
part2_end:
    leave
    ret

#==============================================================================

read_input:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx                  # Save callee-saved registers
    pushq %r12
    pushq %r13
    pushq %r14
    pushq %r15

    xorq %rsi, %rsi             # open arg 2 = O_RDONLY
    leaq FILENAME, %rdi         # open arg 1 = filename
    movq $2, %rax               # open syscall number
    syscall                     # call kernel
    movq %rax, %rbx             # Move file descriptor to rbx

    subq $144, %rsp             # Make room for struct stat (input_stat)
    leaq -144(%rbp), %rsi       # fstat arg 2 = address of input_stat
    movq %rbx, %rdi             # fstat arg 1 = file descriptor 
    movq $5, %rax               # fstat syscall number
    syscall                     # Call kernel

    xorq %r9, %r9               # mmap arg 6 = offset of 0
    movq %rbx, %r8              # mmap arg 5 = file descriptor
    movq $2, %r10               # mmap arg 4 = MAP_PRIVATE
    movq $1, %rdx               # mmap arg 3 = PROT_READ
    movq -96(%rbp), %rsi        # mmap arg 2 = input_stat.st_size
    xorq %rdi, %rdi             # mmap arg 1 = NULL
    movq $9, %rax               # mmap syscall number
    syscall                     # call kernel

    movq %rax, %r12             # Copy mmap return value into r12 for freeing later
    movq %r12, %r13             # Copy mmap return value into r13 for use with strtol
    subq $16, %rsp              # Make room for temp char*
    xorq %r14, %r14             # Zero out index

.readloop:
    cmp N, %r14                 # Compare index with size
    je .end_readloop

    leaq -160(%rbp), %r15       # Store address of where next location is going
    
    movq $10, %rdx              # strtol arg 3 = Base 10
    movq %r15, %rsi             # strtol arg 2 = Next location
    movq %r13, %rdi             # strtol arg 1 = Address of file memory
    callq strtol

    movq (%r15), %r13           # Move current file address to next address

    movq %rax, ARRAY(,%r14,4)   # Store result in array
    inc %r14                    # Increase index
    jmp .readloop               # Jump to start of loop

.end_readloop:
    movq -96(%rbp), %rsi        # munmap arg 2 = mem size in bytes to unmap
    movq %r12, %rdi             # munmap arg 1 = address to unmap
    movq $11, %rax              # munmap syscall number
    syscall

    movq %rbx, %rdi             # close arg 1 = file descriptor
    movq $3, %rax               # close sycall number
    syscall                     # call kernel

    addq $160, %rsp             # Free stack space used by fstat
    popq %r15                   # Restore old callee-saved regsiters
    popq %r14
    popq %r13
    popq %r12
    popq %rbx
    leave
    ret

#==============================================================================

solve:
    pushq %rbp
    movq %rsp, %rbp

    callq read_input
    callq part1
    callq part2

    leave
    ret

#==============================================================================
    .data
    .align 16
N:
    .long 2000
    .align 16
FILENAME:
    .asciz "Day01.in"
    .align 16
PRINT_STR:
    .asciz "%d\n"
    .align 16
DEBUG:
    .asciz "index = %d\n"
    .align 32
ARRAY:
    .zero 8000
