count = 0

class State():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __str__(self):
        return "State: \n Position = ({},{}) + h,g,f = {}, {}, {}".format(self.position[0], self.position[1], self.h, self.g, self.f) + "\n\n"

class Maze():
    def __init__(self, board):
        self.maze = board
        self.count = 0

    def get_parent_list(self, node):
        parents = []
        while node is not None:
            parents.append(node)
            node = node.parent
        return parents

    def solve(self):
        h = 0
        for i in range (len(self.maze)):
            for j in range (len(self.maze[i])):
                if(i == 0 and j == 0):
                    continue
                if(self.maze[i][j] == 'T'):
                    h+=1

        start_state = State(None, (0,0))
        start_state.g = 0
        start_state.h = h
        start_state.f = start_state.g + start_state.h
        end_state = State(None, (-1,-1))
        end_state.g = 0
        end_state.h = 0
        end_state.f = 0

        ol = []
        cl = []

        ol.append(start_state)

        while len(ol) > 0:

            curr_state = ol[0]
            ci = 0
            for index, item in enumerate(ol):
                if item.f < curr_state.f:
                    curr_state = item
                    ci = index

            ol.pop(ci)
            cl.append(curr_state)

            if curr_state.h == end_state.h:
                path = []
                cstate = curr_state
                while cstate is not None:
                    path.append(cstate.position)
                    cstate = cstate.parent
                return path[::-1]

            children_states = []
            for new_position in [(0, 1), (1, 0), (-1, 0), (0, -1)]:

                node_position = (curr_state.position[0] + new_position[0], curr_state.position[1] + new_position[1])

                if node_position[0] > (len(self.maze) - 1) or node_position[0] < 0 or node_position[1] > (len(self.maze[len(self.maze)-1]) -1) or node_position[1] < 0:
                    continue
                
                new_state = State(curr_state, node_position)
                children_states.append(new_state)

            for child_state in children_states:
                self.count+=1
                parents_list = self.get_parent_list(curr_state)
                for closed_child in cl:
                    if child_state == closed_child:
                        continue

                child_state.g = curr_state.g + 1
                temp_x = child_state.position[0]
                temp_y = child_state.position[1]

                if self.maze[temp_x][temp_y] == 'T' and child_state not in parents_list:
                    child_state.h = curr_state.h - 1
                else:
                    child_state.h = curr_state.h
                child_state.f = child_state.g + child_state.h

                ol.append(child_state)

def write_in_file(fname, content):
    f = open(fname, "w")
    f.write(content)
    f.close()

def pathfinding(filename):
    file = open(filename)
    file_data = []
    for row in file:
        row_data = row.split(',')
        if(row_data[-1][-1] == '\n'):
            row_data[-1] = row_data[-1][:-1]
        file_data.append(row_data)
    
    game = Maze(file_data)
    
    path = game.solve()
    write_in_file('num_states_explored.txt', str(game.count))
    write_in_file('optimal_path_cost.txt', str(len(path)-1))
    write_in_file('optimal_path.txt', str(path))
    print(path)
    



if __name__ == '__main__':
    pathfinding('data.csv')
    
