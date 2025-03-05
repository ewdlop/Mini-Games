from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from random import randint
from heapq import heappush, heappop
from copy import deepcopy
from kivy.clock import Clock

class TileButton(Button):
    number = NumericProperty(0)
    background_color = ListProperty([0.3, 0.5, 0.8, 1])  # Blue color
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '20sp'
        self.bind(on_release=self.on_tile_click)  # Change to on_release for better response
    
    def on_tile_click(self, instance):
        print(f"Clicked tile number: {self.number}")  # Debug print
        # Notify the parent board
        if hasattr(self.parent, 'on_tile_press'):
            self.parent.on_tile_press(self)

class PuzzleState:
    def __init__(self, board, empty_pos, g_score=0, parent=None):
        self.board = board
        self.empty_pos = empty_pos
        self.g_score = g_score  # moves so far
        self.parent = parent
        self.h_score = self.manhattan_distance()
        self.f_score = self.g_score + self.h_score

    def __lt__(self, other):
        return self.f_score < other.f_score

    def manhattan_distance(self):
        distance = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != 0:  # Skip empty tile
                    # Calculate expected position
                    target_row = (self.board[i][j] - 1) // 4
                    target_col = (self.board[i][j] - 1) % 4
                    distance += abs(target_row - i) + abs(target_col - j)
        return distance

    def get_state_string(self):
        return ''.join(str(num) for row in self.board for num in row)

class PuzzleBoard(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.spacing = 2
        self.padding = 5
        
        # Initialize board state
        self.tiles = []
        self.empty_pos = (3, 3)  # Row, Column format
        self.moves_count = 0
        self.create_board()
        self.shuffle_board()
    
    def get_tile_pos(self, tile):
        # Get the row and column of a tile based on its current position in the grid
        idx = self.children.index(tile)  # Kivy stores children in reverse order
        # Convert from Kivy's bottom-up index to our top-down index
        idx = len(self.children) - 1 - idx
        row = idx // 4
        col = idx % 4
        print(f"Tile {tile.number} position: ({row}, {col})")  # Debug print
        return (row, col)
    
    def is_valid_move(self, tile):
        tile_pos = self.get_tile_pos(tile)
        # Check if the tile is adjacent to empty space
        valid = (
            (abs(tile_pos[0] - self.empty_pos[0]) == 1 and tile_pos[1] == self.empty_pos[1]) or
            (abs(tile_pos[1] - self.empty_pos[1]) == 1 and tile_pos[0] == self.empty_pos[0])
        )
        print(f"Checking move: Tile at {tile_pos}, Empty at {self.empty_pos}, Valid: {valid}")  # Debug print
        return valid
    
    def swap_tiles(self, tile):
        print(f"Swapping tile {tile.number}")  # Debug print
        # Get positions
        tile_idx = len(self.children) - 1 - self.children.index(tile)
        empty_idx = self.empty_pos[0] * 4 + self.empty_pos[1]
        
        # Swap in the tiles list
        self.tiles[tile_idx], self.tiles[empty_idx] = self.tiles[empty_idx], self.tiles[tile_idx]
        
        # Update empty position
        self.empty_pos = self.get_tile_pos(self.tiles[empty_idx])
        
        # Update widgets in the grid
        self.clear_widgets()
        for tile in self.tiles:
            self.add_widget(tile)
        
        self.moves_count += 1
        print(f"Move count: {self.moves_count}")  # Debug print
    
    def on_tile_press(self, tile):
        print(f"Tile pressed: {tile.number}")  # Debug print
        if self.is_valid_move(tile):
            self.swap_tiles(tile)
            if self.check_win():
                print("Congratulations! You solved the puzzle in", self.moves_count, "moves!")
    
    def check_win(self):
        # Check if all tiles are in correct position
        for i, tile in enumerate(self.tiles[:-1]):  # Exclude last tile (empty)
            if tile.number != i + 1:
                return False
        return True
    
    def shuffle_board(self, moves=100):
        # Perform random valid moves to shuffle the board
        from random import choice
        
        for _ in range(moves):
            # Get all valid moves
            valid_moves = []
            empty_row, empty_col = self.empty_pos
            
            # Check all adjacent positions
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = empty_row + dr, empty_col + dc
                if 0 <= new_row < 4 and 0 <= new_col < 4:
                    tile_idx = new_row * 4 + new_col
                    valid_moves.append(self.tiles[tile_idx])
            
            # Make a random valid move
            tile_to_move = choice(valid_moves)
            self.swap_tiles(tile_to_move)
        
        # Reset moves count after shuffling
        self.moves_count = 0
    
    def create_board(self):
        # Create board in solved state (1-15, then empty)
        numbers = list(range(1, 16)) + [0]  # 0 represents empty tile
        for num in numbers:
            tile = TileButton(
                number=num,
                text=str(num) if num != 0 else '',
                disabled=num == 0,
                background_color=[0.3, 0.5, 0.8, 1] if num != 0 else [1, 1, 1, 0]  # Make empty tile transparent
            )
            self.tiles.append(tile)
            self.add_widget(tile)

    def get_board_state(self):
        # Convert current board to 2D list
        board = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(16):
            row, col = i // 4, i % 4
            board[row][col] = self.tiles[i].number
        return board

    def solve_puzzle(self):
        print("Solving puzzle...")
        initial_board = self.get_board_state()
        solution = self.a_star_solve(initial_board)
        if solution:
            print("Solution found! Moves required:", len(solution) - 1)
            self.apply_solution(solution)
        else:
            print("No solution found!")

    def a_star_solve(self, initial_board):
        # Find empty position
        empty_pos = None
        for i in range(4):
            for j in range(4):
                if initial_board[i][j] == 0:
                    empty_pos = (i, j)
                    break

        initial_state = PuzzleState(initial_board, empty_pos)
        open_set = []
        heappush(open_set, initial_state)
        closed_set = set()

        while open_set:
            current = heappop(open_set)

            if current.manhattan_distance() == 0:  # Goal reached
                return self.reconstruct_path(current)

            state_string = current.get_state_string()
            if state_string in closed_set:
                continue

            closed_set.add(state_string)

            # Generate possible moves
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row = current.empty_pos[0] + dr
                new_col = current.empty_pos[1] + dc

                if 0 <= new_row < 4 and 0 <= new_col < 4:
                    new_board = deepcopy(current.board)
                    # Swap tiles
                    new_board[current.empty_pos[0]][current.empty_pos[1]] = \
                        new_board[new_row][new_col]
                    new_board[new_row][new_col] = 0

                    new_state = PuzzleState(
                        new_board,
                        (new_row, new_col),
                        current.g_score + 1,
                        current
                    )

                    if new_state.get_state_string() not in closed_set:
                        heappush(open_set, new_state)

        return None

    def reconstruct_path(self, final_state):
        path = []
        current = final_state
        while current:
            path.append(current.board)
            current = current.parent
        return path[::-1]

    def apply_solution(self, solution_path):
        # Apply each move in the solution
        for board_state in solution_path[1:]:  # Skip first state (current state)
            # Find the number that moved
            for i in range(4):
                for j in range(4):
                    if board_state[i][j] != self.get_board_state()[i][j]:
                        if board_state[i][j] != 0:  # Found the moved tile
                            # Find and move the corresponding tile
                            for tile in self.tiles:
                                if tile.number == board_state[i][j]:
                                    self.on_tile_press(tile)
                                    break
            Clock.schedule_once(lambda dt: None, 0.5)  # Add delay between moves

    def add_solve_button(self):
        solve_button = Button(
            text='Solve',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'right': 1, 'top': 1}
        )
        solve_button.bind(on_press=lambda x: self.solve_puzzle())
        self.add_widget(solve_button)

class FifteenPuzzleApp(App):
    def build(self):
        board = PuzzleBoard()
        board.add_solve_button()
        return board

if __name__ == '__main__':
    FifteenPuzzleApp().run()