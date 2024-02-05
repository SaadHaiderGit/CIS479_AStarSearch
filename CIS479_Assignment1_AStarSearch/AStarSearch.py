#Saad Haider
#Created 1/20/2023
#Last Modified 1/20/2023
#Artificial Intelligence P1: Windy Day 8-Puzzle w/ A* Search


#This project has a 8 puzzle with a north wind (step cost = 1 for moving south, 3 for moving north, 2 for moving east or west). We use A* search to find the solution.
#We create a starting 8-puzzle and a goal 8-puzzle. The start 8-puzzle will search for the goal, with the output showing each expansion node and the final result.

#imports go here
from collections import defaultdict
import copy


class Node:
    def __init__(self, state, parent, action, gval, hval, fval):
        """ Initialize the node with its state, parent, and action that created this state.
            Also stores hval (Manhattan distance), gval (path cost so far), and fval (hval + gval). (hval and fval are calculated in the EightPuzzle class.) """
        self.state = state
        self.parent = parent
        self.action = action
        self.gval = gval
        self.hval = hval
        self.fval = fval



    def generate_child(self):
        """ Generate child nodes from the given node by swapping the blank space with a neighboring non-blank space located in the four cardinal directions.

            NOTE: move_cost holds the cost position values and the associated direction for swapping a neighboring non-blank space with the blank space,
            with the cost being dependent on a wind blowing downward from the north. (Move South = 1, Move North = 3, Move East/West = 2.) The order 
            for which direction this neighbor is ORIGINALLY located is [west, north, east, south] respectively."""

        y, x = self.find_blank(self.state)
        children = []
        move_cost = [[2, y, x-1, "MoveEast"], [1, y-1, x, "MoveSouth"], [2, y, x+1, "MoveWest"], [3, y+1, x, "MoveNorth"]]
        for i in move_cost:
            child = self.space_swap(self.state, y, x, i[1], i[2])
            if child is not None:                                               #cannot have child nodes where the swap is out of bounds
                child_node = Node(child, self, i[3], self.gval+i[0], 0, 0)
                children.append(child_node)
        return children
        

    def space_swap(self, state, y1, x1, y2, x2):
        """ Swap the blank space with an associated non-blank neighbor, unless if the neighbor's given coordinates are out of bounds (as there is nothing to swap). """

        if y2 >= 0 and y2 < 3 and x2 >= 0 and x2 < 3:
            new_state = copy.deepcopy(state)                                    #copy the old state to create a new child state, complete with swapped values
            temp = new_state[y2][x2]
            new_state[y2][x2] = new_state[y1][x1]
            new_state[y1][x1] = temp
            return new_state
        else:
            return None
            

    def find_blank(self, state):
        """ Finds the location of the blank space in order to find possible swaps. """
        for i in range(0,3):
            for j in range(0,3):
                if state[i][j] == "_":
                    return i,j
        return -9999, -9999                   #shouldn't run (as "_" was already found in start & goal states); only for testing purposes


class EightPuzzle:
    def __init__(self):
        """ Initialize empty frontier and explored sets. The former is a priority queue list (ordered by the lowest f-value), the latter is a hash table. """
        self.frontier = []
        self.explored = defaultdict(list) 


    def record_input(self):
        """ Reads and records the user's inputted puzzle. If the puzzle has incorrect metrics, it will declare an error. """
        puzzle = []
        dupe_check = []
        for i in range(0,3):
            temp = input().lstrip(" ").split(" ")

            if len(temp) != 3:
                raise IndexError("This input doesn't conform to the required matrix size (3x3; three rows, each with three values). \nA re-input is required. \n\n")
            for val in temp:
               if val in dupe_check:
                   raise IndexError("This input has duplicates of the same value, which prevents puzzle solving. \nA re-input is required. \n\n")
               dupe_check.append(val)
            puzzle.append(temp)
        
        if self.blank_exists(puzzle) == False:
            raise AttributeError
        return puzzle


    def blank_exists(self, state):
        """ Ensures an inputted start or goal state has a '_' space. If not, return an error. """
        for i in range(0,3):
            for j in range(0,3):
                if state[i][j] == "_":
                    return True
        return False


    def h(self, cur, goal):
        """ Calculates the overall Manhattan distance for each space, finding the difference in position while accounting for windy cost. """
        total_h = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if cur[i][j] != goal[i][j] and cur[i][j] != '_':
                    total_h += self.h_single(cur, goal, i, j)                       #calculate the individual tile's h-value
        return total_h


    def h_single(self, cur, goal, y1, x1):
        """ Calculates a single space's h(n) by comparing its current and goal position, then calculates the cost to get from one to the other. """
        for y2 in range(0, 3):
            for x2 in range(0, 3):
                if cur[y1][x1] == goal[y2][x2]:
                    if y2 > y1:                                             #goal is southward
                        return (2 * (abs(x2 - x1)) + (abs(y2 - y1)) )
                    else:                                                   #goal is northward
                        return (2 * (abs(x2 - x1)) + 3 * (abs(y2 - y1)) )

        #If this runs, a non-blank space exists that is only in start or goal state, and not the other (which makes the puzzle unsolvable); only used d
        raise ValueError   


    def nodehash(self, state):
        """ Takes the 8-puzzle node state and turns it into a string for hashing, allowing nodes with the exact same state (but different info) to be hashed together."""
        code = ""
        for j in range(0, 3):
            for i in range(0, 3):
                code += state[j][i]
        return code


    def not_in_frontier(self, state):
        """ Detects if the current node's state already exists in the frontier queue. Used to prevent redundant paths. """
        for i in range(1, len(self.frontier)):
            if self.frontier[i].state == state:
                return False
        return True


    def main_process(self):
        """ The main body of the program! Takes a start and goal puzzle, then calculates its expansion order until it finds a solution, using A* search. """
        inputs_given = 0
        while inputs_given < 2:
            try:
                if inputs_given == 0:
                    print("Please insert the <STARTING> 8-puzzle matrix.\n")
                    start = self.record_input()
                else:
                    print("Please insert the <GOAL> 8-puzzle matrix.\n")        
                    goal = self.record_input()
                inputs_given += 1
                if inputs_given == 2:
                    first = Node(start, None, None, 0, 0, 0)
                    first.hval = self.h(first.state, goal)
                    first.fval = first.hval + first.gval
            except IndexError as err:
                print(err)
            except AttributeError:
                print('There is no "_" in this matrix, preventing the puzzle from functioning. \nA re-input is required. \n\n')
            except ValueError:
                print("The start or goal state has a non-empty space not found in the other state. \nYou must re-input both the start and goal state. \n\n")
                inputs_given = 0
            except:
                print("This error shouldn't be appearing. Please inform the maker of this program about it. \nA re-input is required. \n\n")

        
        #All inputs confirmed. Insert the starting node to the frontier, then begin A* search.
        self.frontier.append(first)                                        
        expansion_order_count = 0
        print("\n\nSearching for a solution. Please note that this might take a while, depending on your start and goal state.\n")

        #Loop until search is complete or failure occurs:
        while True:
            self.frontier.sort(key = lambda x:x.fval, reverse=False)      #sort frontier queue so nodes with the lowest fval are chosen next (with FIFO order for ties)
            cur = self.frontier[0]
            expansion_order_count += 1

            #print the current node state, along with its g(n), h(n), and expansion order count (only for testing and statistics)
            #if len(self.explored) > 0:                                    
            #    #print("")
            #    print("            | ")
            #    print("            | ")
            #    print("            V \n--------------------------")
            #for i in cur.state:
            #    print("        |", end=" ")
            #    for j in i:
            #        print(j,end=" ")
            #    print("|")
            #print("\n" + ("(g(n) = " + str(cur.gval) + " | h(n) = " + str(cur.hval) + ")").center(24))
            #print (("#" + str(expansion_order_count)).center(25))
            #print("--------------------------")

            #If the goal state has been reached, success! Exit the main process.
            if(self.h(cur.state, goal) == 0):            
                print("\nA solution was found! It is printed below, from start to finish.")
                print("Note: g(n) is the path cost so far, and h(n) is Manhattan distance, or how far all incorrectly placed values are from their proper positions.")
                print("(They're technical terms for the A* Search algorithm used for calculating the 8-puzzle solution. Don't worry if you don't understand them!)")
                print("\n--------------------------")
                solution_list = []
                while True:
                    solution_list.insert(0, cur)
                    if cur.parent is None:
                        break
                    cur = cur.parent
                for s in range(0, len(solution_list)):
                    if s > 0:                                    
                        #print("")
                        print("            | ")
                        print("            | ")
                        print("            V \n--------------------------")
                    for i in solution_list[s].state:
                        print("        |", end=" ")
                        for j in i:
                            print(j,end=" ")
                        print("|")
                    print("\n" + ("(g(n) = " + str(solution_list[s].gval) + " | h(n) = " + str(solution_list[s].hval) + ")").center(24))
                    print (("#" + str(s)).center(25))
                    print("--------------------------")
                print("\nThis puzzle takes " + str(len(solution_list) - 1) + " moves to solve.")
                break

            #Create node's children, unless the node already exists in the frontier / explored set
            code = self.nodehash(cur.state)              
            if self.not_in_frontier(cur.state) == True and code not in self.explored:
                for i in cur.generate_child():          
                    i.hval = self.h(i.state, goal)
                    i.fval = i.hval + i.gval
                    self.frontier.append(i)
            
            #Remove current node and place it in the explored hash table set. If no more nodes left in the frontier, return failure.
            self.explored[code].append(cur)              
            del self.frontier[0]
            
            if not self.frontier:
                print("\n\nNo solution found! It appears this puzzle is unsolvable.\n")
                break


#Program start
if __name__ == "__main__":

    puzzle = EightPuzzle()
    puzzle.main_process()

