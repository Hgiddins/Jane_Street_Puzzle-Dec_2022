# Jane_Street_Puzzle-Dec_2022

#    - This algorithm procedurally generates the values on each side of the die whilst using an adapted Trémaux maze-solving
#      algorithm to ensure all viable routes are explored and the correct path is found:

#       1. Checks what valid moves are open to the die.
#       2. If the value on the upright face of the die is currently empty then it will assign it the required value to
#          make an attempted move valid. Thus, it procedurally works out the sides of the die.
#       3. Makes a move. This involves, adding the new position and orientation of the die (and score and moves) to the
#          history. It also involves deleting the option of making that move from the history so that if the node is
#          revisited it will not try the same move twice.
#       4. If a dead-end is reached then the last visited node (square on the board) is deleted from the history until
#          a node is reached where there is an available move to make. Then repeat from step 1. 
#       5. Check if current node is destiantion node. If so, terminate algorithm. If not, repeat from step 1. 
