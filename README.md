## Jane Street's Monthly Puzzle: December-2022

**This algorithm procedurally generates the values on each side of the die whilst adapting  _Trémaux's_ maze-solving algorithm to ensure all viable routes are explored and the correct path is found:**

  1. Check if the current node is destination node. If so, terminate the algorithm. If not, continue.
  2. Check what valid moves are open to the die. If a dead-end is reached (no available moves)then the last visited node (square on the board) is deleted from the history and the dice 'moves back', and algorithm repeats from step 1. If there are available moves, the algroithm continues to step 3.
  3. If the value on the upright face of the die is currently empty then it will assign it the required value to make a valid move. Thus, it procedurally works out the sides of the die.
  4. Makes a move. This involves, adding the new position and orientation of the die (and score and moves) to the history. It also involves deleting the option of making that move from the history so that if the node is revisited it will not try the same move twice.
  5.  Repeat from step 1. 
  
