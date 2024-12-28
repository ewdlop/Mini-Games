import random

# Define the grid size
GRID_SIZE = 10

# Define a list of words to be used in the crossword puzzle
WORDS = ["python", "java", "ruby", "perl", "swift", "kotlin", "typescript", "javascript", "html", "css"]

# Initialize the crossword grid
grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def can_place_word_horizontally(word, row, col):
    if col + len(word) > GRID_SIZE:
        return False
    for i in range(len(word)):
        if grid[row][col + i] not in (' ', word[i]):
            return False
    return True

def can_place_word_vertically(word, row, col):
    if row + len(word) > GRID_SIZE:
        return False
    for i in range(len(word)):
        if grid[row + i][col] not in (' ', word[i]):
            return False
    return True

def place_word_horizontally(word, row, col):
    for i in range(len(word)):
        grid[row][col + i] = word[i]

def place_word_vertically(word, row, col):
    for i in range(len(word)):
        grid[row + i][col] = word[i]

def place_words(words):
    random.shuffle(words)
    for word in words:
        placed = False
        for _ in range(100):  # Try 100 times to place the word
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if random.choice([True, False]):
                if can_place_word_horizontally(word, row, col):
                    place_word_horizontally(word, row, col)
                    placed = True
                    break
            else:
                if can_place_word_vertically(word, row, col):
                    place_word_vertically(word, row, col)
                    placed = True
                    break
        if not placed:
            print(f"Failed to place the word: {word}")

def print_grid():
    for row in grid:
        print(' '.join(row))

def generate_clues(words):
    clues = {}
    for word in words:
        clues[word] = f"Clue for {word}"
    return clues

def print_clues(clues):
    for word, clue in clues.items():
        print(f"{word.upper()}: {clue}")

# Place the words in the crossword grid
place_words(WORDS)

# Print the crossword grid
print("Crossword Grid:")
print_grid()

# Generate and print the clues
clues = generate_clues(WORDS)
print("\nClues:")
print_clues(clues)
