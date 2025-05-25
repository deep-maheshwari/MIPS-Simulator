.data
array:
	.word 3,2,1
	.word 2
	.word 0
	.word 1
.text
.globl main

main:
    # Setup constants
    lui $s0, 0x1001     # $s0 = base address of array (0x10010000)
    ori $t5, $zero, 5   # $t5 = N-1 = 5 (For N=6 elements: outer loop pass count N-1, and initial inner loop comparison count N-1)
    ori $t3, $zero, 1   # $t3 = 1 (constant for slt check: $s2 < $s1 is true)
    ori $t4, $zero, 0   # $t4 = 0 (outer loop counter i = 0)

big_while: # Outer loop (controls passes, i from 0 to N-2)
    # Loop condition: if $t4 == $t5 (i.e., i == N-1), exit outer loop
    beq $t4, $t5, end_big_while

    # Setup for inner loop pass
    lui $s0, 0x1001     # Reset $s0 to array base for current pass
    ori $t2, $zero, 0   # $t2 = 0 (inner loop counter j = 0)
    
    # Calculate inner loop comparison limit for this pass: $t1 = (N-1) - i
    # Example: Pass i=0 ($t4=0): $t1 = 5-0 = 5. Inner loop j runs 0..4 (5 comparisons)
    #          Pass i=4 ($t4=4): $t1 = 5-4 = 1. Inner loop j runs 0..0 (1 comparison)
    sub $t1, $t5, $t4   

sm_while: # Inner loop (controls comparisons within a pass, j from 0 to (N-1-i)-1 )
    # Loop condition: if $t2 == $t1 (i.e., j == (N-1-i) ), exit inner loop
    beq $t2, $t1, end_sm_while

    lw $s1, 0($s0)      # current_element = array[j] using current $s0
    lw $s2, 4($s0)      # next_element = array[j+1] using current $s0
    slt $s3, $s2, $s1   # $s3 = (next_element < current_element) ? 1 : 0
    beq $s3, $t3, swap  # if $s3 == 1 (true, $s2 < $s1), then branch to swap

    j temp_after_swap   # else, skip swap

swap:
    sw $s1, 4($s0)      # array[j+1] = current_element (which was in $s1)
    sw $s2, 0($s0)      # array[j]   = next_element (which was in $s2)

temp_after_swap:
    addi $s0, $s0, 4    # Advance array pointer for next pair ( conceptually j++ for array access)
    addi $t2, $t2, 1    # Increment inner loop counter j
    j sm_while          # Loop back to inner loop check

end_sm_while:
    addi $t4, $t4, 1    # Increment outer loop counter i
    j big_while         # Loop back to outer loop check

end_big_while:
    jr $ra              # End of program
