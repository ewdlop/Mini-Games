import tkinter as tk
from tkinter import messagebox
import copy

class Sokoban:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("倉庫番 (Sokoban)")
        
        # Create a frame to hold the game board
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True)
        
        # Game state
        self.level = [
            ["#", "#", "#", "#", "#"],
            ["#", " ", " ", " ", "#"], 
            ["#", " ", "@", " ", "#"],
            ["#", " ", "$", ".", "#"],
            ["#", "#", "#", "#", "#"]
        ]
        self.player_pos = [2, 2]
        
        # Create game board
        self.cells = []
        for i in range(len(self.level)):
            row = []
            for j in range(len(self.level[0])):
                cell = tk.Label(self.game_frame, width=2, height=1, relief="solid")
                cell.grid(row=i, column=j)
                row.append(cell)
            self.cells.append(row)
            
        # Bind keys
        self.root.bind("<Up>", lambda e: self.move("up"))
        self.root.bind("<Down>", lambda e: self.move("down")) 
        self.root.bind("<Left>", lambda e: self.move("left"))
        self.root.bind("<Right>", lambda e: self.move("right"))
        
        # Center the window after creating all elements
        self.center_window()
        
        self.update_display()
        
    def move(self, direction):
        dx, dy = 0, 0
        if direction == "up": dy = -1
        elif direction == "down": dy = 1
        elif direction == "left": dx = -1
        elif direction == "right": dx = 1
            
        x, y = self.player_pos
        new_x, new_y = x + dx, y + dy
        
        # Check if move is valid
        if self.level[new_y][new_x] == "#":
            return
            
        # Handle box pushing
        if self.level[new_y][new_x] in ["$", "*"]:
            box_x, box_y = new_x + dx, new_y + dy
            if self.level[box_y][box_x] in ["#", "$", "*"]:
                return
                
            # Move box
            if self.level[new_y][new_x] == "$":
                self.level[new_y][new_x] = " "
            else:
                self.level[new_y][new_x] = "."
                
            if self.level[box_y][box_x] == ".":
                self.level[box_y][box_x] = "*"
            else:
                self.level[box_y][box_x] = "$"
                
        # Move player
        self.level[y][x] = " " if self.level[y][x] == "@" else "."
        self.level[new_y][new_x] = "@"
        self.player_pos = [new_x, new_y]
        
        self.update_display()
        self.check_win()
        
    def update_display(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[0])):
                cell = self.cells[i][j]
                char = self.level[i][j]
                
                if char == "#":
                    cell.config(bg="gray", text="")
                elif char == " ":
                    cell.config(bg="white", text="")
                elif char == "@":
                    cell.config(bg="yellow", text="@")
                elif char == "$":
                    cell.config(bg="brown", text="$")
                elif char == ".":
                    cell.config(bg="green", text=".")
                elif char == "*":
                    cell.config(bg="blue", text="*")
                    
    def check_win(self):
        for row in self.level:
            for cell in row:
                if cell == "$":
                    return
        messagebox.showinfo("Congratulations!", "You won!")
        
    def run(self):
        self.root.mainloop()

    def center_window(self):
        # Wait for window to be rendered
        self.root.update_idletasks()
        
        # Get screen and window dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set the position
        self.root.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    game = Sokoban()
    game.run()
