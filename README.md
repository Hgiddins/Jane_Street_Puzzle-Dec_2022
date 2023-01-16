## Jane Street's Monthly Puzzle: December-2022

**This algorithm procedurally generates the values on each side of the die whilst adapting  _Trémaux's_ maze-solving algorithm to ensure all viable routes are explored and the correct path is found:**

  1. Check if the current node is destination node. If so, terminate the algorithm. If not, repeat from step 1.
  2. Checks what valid moves are open to the die.
  3. If the value on the upright face of the die is currently empty then it will assign it the required value to make an attempted move valid. Thus, it procedurally works out the sides of the die.
  4. Makes a move. This involves, adding the new position and orientation of the die (and score and moves) to the history. It also involves deleting the option of making that move from the history so that if the node is revisited it will not try the same move twice.
  5. If a dead-end is reached then the last visited node (square on the board) is deleted from the history until a node is reached where there is an available move to make. Then repeat from step 1. 
  
