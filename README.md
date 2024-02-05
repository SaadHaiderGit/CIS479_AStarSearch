# Windy Day 8-Puzzle w/ A* Search
This simple Python script allows a user to input an 8-puzzle into the terminal and its intended solution. The program will then attempt to solve the puzzle in the shortest amount of moves possible, using an A* Search algorithm.

The 8-puzzle is under the effects of a north wind. As such, when a puzzle piece tries to shift northward, it will have a cost of 3 'steps'. Shifting southward will have a cost of 1 step, and shifting east or west will have a cost of 2 steps.

When a 8-puzzle is inputted, the program shows what moves to take in order to solve the puzzle. Statisical notes are given on the total cost of movements made so far (g(n)) and the collective Manhattan distance cost of how far away all values in the 8-puzzle are from their correct position (h(n)). The number of moves required are also given.

## How to Use
You will be prompted to insert an initial 8-puzzle matrix, then the solution that you want. To do so, you will need to input three rows, each with three values (3x3). You will insert a total of nine values for the initial and final puzzle each. Only insert a 3x3 matrix, with spaces in between each input in a row, and do not use duplicate values.

Although you can insert any character or number as your inputs, it is recommended that you use values 1-8 for both puzzles. You also must use the underscore character ('_') in both; it represents your empty tile, which is needed for valued tiles to move and change positions. 

Example:

![image](https://github.com/SaadHaiderGit/Windy8PuzzleSearch/assets/118562950/e3a13109-304a-40f0-9258-e518d8563d1a)


Once your inputs are entered, the system will take some time to process it, before printing out the solution, with all required steps for solving the puzzle being displayed. If a solution cannot be found or the system takes too long to find one, the system will print out a statement informing this.

![image](https://github.com/SaadHaiderGit/Windy8PuzzleSearch/assets/118562950/43be4491-56c4-42d6-a3e0-9d3cc5901028)

