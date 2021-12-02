    .text
    .global main
#==============================================================================
# print(void) -> void
print:
    pushq %rbp
    movq %rsp, %rbp
    pushl %eax

    xorl %eax, %eax
    movl %edi, %esi
    movl $PRINT_STR, %edi
    call printf

    popl %eax

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
    cmpl (%rdi), %ecx       # if *(ARRAY+4) > *ARRAY then jump to .L01
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
# part2(void) -> int
part2:
    pushq %rbp
    movq %rsp, %rbp

    xorl %eax, %eax         # zero out counter
    leaq ARRAY, %rdi        # array pointer
    movl $2, %esi           # end index
    movl (%rdi), %edx       # previous sum
    addl 4(%rdi), %edx
    addl 8(%rdi), %edx
    addq $4, %rdi           # move array pointer to next window
part2_loop:
    cmpl N, %esi
    je part2_end

    movl (%rdi), %ecx
    addl 4(%rdi), %ecx
    addl 8(%rdi), %ecx
    cmp %edx, %ecx          # if sum > prev_sum then jump to .L03
    jg .L03
    jmp .L04
.L03:
    inc %eax                # increment counter
.L04:
    movl %ecx, %edx         # move sum into prev_sum
    inc %esi                # increment index
    addq $4, %rdi           # move array pointer
    jmp part2_loop          # jump to start of loop
part2_end:
    leave
    ret

#==============================================================================
input:
    pushq %rbp
    movq %rsp, %rbp

    movl $2, %eax           # Open system call number
    movl $INPUT_FILE, %ebx  # Input filepath
    xorl %ecx, %ecx         # Set flag to read only
    int $0x80

    pushl %eax              # Push file descriptor to the stack
    

    leave
    ret

#==============================================================================

main:
    pushq %rbp
    movq %rsp, %rbp

    call part1
    movl %eax, %edi
    call print

    call part2
    movl %eax, %edi
    call print

    xorl %eax, %eax
    leave
    ret

#==============================================================================

    .data
PRINT_STR:
    .asciz "%lld\n"
INPUT_FILE:
    .asciz "inputs/Day01.in\0"
N:
    .long 2000
ARRAY:
    .long 8000
