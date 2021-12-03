	.file	"Day01.c"
	.text
	.globl	ARRAY
	.bss
	.align 32
	.type	ARRAY, @object
	.size	ARRAY, 8000
ARRAY:
	.zero	8000
	.globl	N
	.section	.rodata
	.align 8
	.type	N, @object
	.size	N, 8
N:
	.quad	2000
.LC0:
	.string	"Usage: ./Day01 <num_runs>"
.LC2:
	.string	"start time error"
.LC5:
	.string	"Time: %Lf us\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$184, %rsp
	.cfi_offset 3, -24
	movl	%edi, -164(%rbp)
	movq	%rsi, -176(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	cmpl	$1, -164(%rbp)
	jg	.L2
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$-1, %eax
	jmp	.L14
.L2:
	fldz
	fstpt	-96(%rbp)
	movl	$0, -156(%rbp)
	jmp	.L4
.L13:
	leaq	-128(%rbp), %rax
	movq	%rax, %rsi
	movl	$0, %edi
	call	clock_gettime@PLT
	cmpl	$-1, %eax
	jne	.L5
	leaq	.LC2(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$-1, %eax
	jmp	.L14
.L5:
	movl	$0, %eax
	call	read_input
	movl	$0, -152(%rbp)
	movl	$0, -148(%rbp)
	movq	$1, -144(%rbp)
	jmp	.L6
.L8:
	movq	-144(%rbp), %rax
	leaq	0(,%rax,4), %rdx
	leaq	ARRAY(%rip), %rax
	movl	(%rdx,%rax), %edx
	movq	-144(%rbp), %rax
	subq	$1, %rax
	leaq	0(,%rax,4), %rcx
	leaq	ARRAY(%rip), %rax
	movl	(%rcx,%rax), %eax
	cmpl	%eax, %edx
	jle	.L7
	addl	$1, -152(%rbp)
.L7:
	addq	$1, -144(%rbp)
.L6:
	movl	$2000, %eax
	cmpq	%rax, -144(%rbp)
	jb	.L8
	movq	$3, -136(%rbp)
	jmp	.L9
.L11:
	movq	-136(%rbp), %rax
	leaq	0(,%rax,4), %rdx
	leaq	ARRAY(%rip), %rax
	movl	(%rdx,%rax), %edx
	movq	-136(%rbp), %rax
	subq	$3, %rax
	leaq	0(,%rax,4), %rcx
	leaq	ARRAY(%rip), %rax
	movl	(%rcx,%rax), %eax
	cmpl	%eax, %edx
	jle	.L10
	addl	$1, -148(%rbp)
.L10:
	addq	$1, -136(%rbp)
.L9:
	movl	$2000, %eax
	cmpq	%rax, -136(%rbp)
	jb	.L11
	leaq	-112(%rbp), %rax
	movq	%rax, %rsi
	movl	$0, %edi
	call	clock_gettime@PLT
	cmpl	$-1, %eax
	jne	.L12
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$-1, %eax
	jmp	.L14
.L12:
	movq	-104(%rbp), %rax
	movq	-120(%rbp), %rdx
	subq	%rdx, %rax
	movq	%rax, -184(%rbp)
	fildq	-184(%rbp)
	fldt	.LC3(%rip)
	fdivrp	%st, %st(1)
	fstpt	-80(%rbp)
	movq	-112(%rbp), %rax
	movq	%rax, -184(%rbp)
	fildq	-184(%rbp)
	movq	-128(%rbp), %rax
	movq	%rax, -184(%rbp)
	fildq	-184(%rbp)
	fsubrp	%st, %st(1)
	fstpt	-64(%rbp)
	fldt	-80(%rbp)
	fldt	-64(%rbp)
	faddp	%st, %st(1)
	fstpt	-48(%rbp)
	fldt	-48(%rbp)
	fldt	-96(%rbp)
	fsubrp	%st, %st(1)
	movl	-156(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -184(%rbp)
	fildl	-184(%rbp)
	fdivrp	%st, %st(1)
	fldt	-96(%rbp)
	faddp	%st, %st(1)
	fstpt	-96(%rbp)
	addl	$1, -156(%rbp)
.L4:
	movl	-156(%rbp), %eax
	movslq	%eax, %rbx
	movq	-176(%rbp), %rax
	addq	$8, %rax
	movq	(%rax), %rax
	movl	$10, %edx
	movl	$0, %esi
	movq	%rax, %rdi
	call	strtol@PLT
	cmpq	%rax, %rbx
	jl	.L13
	fldt	-96(%rbp)
	fldt	.LC4(%rip)
	fmulp	%st, %st(1)
	leaq	-16(%rsp), %rsp
	fstpt	(%rsp)
	leaq	.LC5(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	addq	$16, %rsp
	movl	$0, %eax
.L14:
	movq	-24(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L15
	call	__stack_chk_fail@PLT
.L15:
	movq	-8(%rbp), %rbx
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.section	.rodata
.LC7:
	.string	"../inputs/Day01.in"
	.text
	.globl	read_input
	.type	read_input, @function
read_input:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$208, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$0, %esi
	leaq	.LC7(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	open@PLT
	movl	%eax, -196(%rbp)
	leaq	-160(%rbp), %rdx
	movl	-196(%rbp), %eax
	movq	%rdx, %rsi
	movl	%eax, %edi
	call	fstat@PLT
	movq	-112(%rbp), %rax
	movq	%rax, %rsi
	movl	-196(%rbp), %eax
	movl	$0, %r9d
	movl	%eax, %r8d
	movl	$2, %ecx
	movl	$1, %edx
	movl	$0, %edi
	call	mmap@PLT
	movq	%rax, -168(%rbp)
	movq	-168(%rbp), %rax
	movq	%rax, -184(%rbp)
	movq	$0, -176(%rbp)
	jmp	.L17
.L18:
	leaq	-192(%rbp), %rcx
	movq	-184(%rbp), %rax
	movl	$10, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	strtol@PLT
	movl	%eax, %ecx
	movq	-176(%rbp), %rax
	leaq	0(,%rax,4), %rdx
	leaq	ARRAY(%rip), %rax
	movl	%ecx, (%rdx,%rax)
	movq	-192(%rbp), %rax
	addq	$1, %rax
	movq	%rax, -184(%rbp)
	addq	$1, -176(%rbp)
.L17:
	movl	$2000, %eax
	cmpq	%rax, -176(%rbp)
	jb	.L18
	movq	-112(%rbp), %rax
	movq	%rax, %rdx
	movq	-168(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	munmap@PLT
	movl	-196(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
	nop
	movq	-8(%rbp), %rax
	subq	%fs:40, %rax
	je	.L19
	call	__stack_chk_fail@PLT
.L19:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	read_input, .-read_input
	.section	.rodata
	.align 16
.LC3:
	.long	0
	.long	-294967296
	.long	16412
	.long	0
	.align 16
.LC4:
	.long	0
	.long	-198967296
	.long	16402
	.long	0
	.ident	"GCC: (GNU) 11.1.0"
	.section	.note.GNU-stack,"",@progbits
