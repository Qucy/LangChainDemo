# There a number of soldiers standing in a line, with IDs from 1 to N, in ascending order.
# They are participating in a exercise consisting of Q actions.
# During the ith action, the Major calls S number of row i and col j th positions swap places, and so on until row i + m < col j + m
# Each of the soliders ID will be covered in the range [row i, col j] for at most one action.abs

# Write an algorithm to find the ID of the soldier at Kth position in the line after all the actions are completed.

# Input
# The first line of input consists of an integer N, representing the number of soldiers.
# The second line of input consists of two space-separated integers Q and S, representing the number of actions and number of soldiers called by Major.
# The next Q lines consist of S space-sparated integers, representing the row i and col j, representing the position of the soldiers called by Major.
# The last line consists of an integer posSoldier, representing the Kth position of the soldier in the line after all the actions are completed.

# Output
# Print an integer representing the ID of the soldier at Kth position in the line after all the actions are completed.

# Constraints
# 1 <= N <= 10^6
# 1 <= Q <= 10^6
# 1 <= S <= 10^6
# 1 <= row i, col j <= N
# 1 <= posSoldier <= N

# Example
# Input:
# 10
# 2 2
# 1 5
# 6 10
# 1

# Output:
# 5

import numpy as np

def swapSoliders(n, q, s, actions, posSoldier):

    soldiers = np.arange(1, n + 1)

    for idx, action in enumerate(actions):

        # make sure we are not out of bounds and follw the quantity of actions
        if idx >= q:
            break

        row = action[0] - 1
        col = action[1] -1 
        
        while row <= col:
            soldiers[row], soldiers[col] = soldiers[col], soldiers[row]
            row += 1
            col -= 1

    return soldiers[posSoldier - 1]



if __name__ == "__main__":

    print(swapSoliders(10, 2, 2, [[1, 5], [6, 10]], 1))
