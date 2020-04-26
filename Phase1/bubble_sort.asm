.data
array:
	.word 5,4,3
	.word 2
	.word 0
	.word 1
.text
.globl main

main:
	
	lui $s0 , 0x1001
	lw $t1 , 12($s0)
	lw $t3, 20($s0)
	lw $t2, 16($s0)
	lw $t4, 16($s0)
	
	big_while:
		
	bne $t2, $t1, sm_while
	sub $t2,$t2,$t4
	
	sm_while:
	lw $s1 , 0($s0)
	lw $s2, 4($s0) 
	slt $s3, $s2, $s1
	beq $s3, $t3, swap
	j temp
	
	swap:
	sw $s1, 4($s0)
	sw $s2, 0($s0)
	j temp
	
	temp:
	addi $s0 ,$s0, 4
	addi $t2, $t2, 1
	bne $t2, $t1, sm_while
		
	andi $s0,$s0,0x0000
	lui $s0, 0x1001
	lw $t2, 16($s0)
	addi $t4, $t4, 1
	bne $t4, $t1, big_while
	
	jr $ra
		