import tkinter as tk
import random
#data
data_bank = {
    "Fruit": ["mango", "banana", "cherry", "orange", "apple", "papaya", "grapes"],
    "Flower": ["rose", "lotus", "tulip", "jasmine", "lily"],
    "Country": ["india", "japan", "brazil", "canada", "france", "germany", "italy"],
    "Animal": ["tiger", "elephant", "rabbit", "giraffe", "monkey", "zebra", "panther"],
    "Foot Ball Player":["Messi","neymar","kaka","ronaldo"]
        }
phrases = [
    "Before the hangman arrives, guess the {cat}!",
    "Can you guess the {cat}?",
    "What do you think, which {cat} could it be?",
    "Let's see, maybe it's your favourite {cat}!",
    "Quick! Guess the {cat} before it's too late!"
]
cat, word, guesses, lives, msg = "", "", [], 6, ""
bg, fg, accent = "#141444", "#CDD6F4", "#FFBB29" 
box_bg = "#20224E"

def setup_game():
    global cat, word, guesses, lives, msg
    cat = random.choice(list(data_bank.keys()))
    word = random.choice(data_bank[cat])
    msg = random.choice(phrases).format(cat=cat.lower())
    guesses, lives = [], 6

def popup(title, text, color):
    win = tk.Toplevel(root)
    win.title(title)
    p_w, p_h = 300, 160
    cx = root.winfo_x() + (root.winfo_width() // 2) - (p_w // 2)
    cy = root.winfo_y() + (root.winfo_height() // 2) - (p_h // 2)
    win.geometry(f"{p_w}x{p_h}+{cx}+{cy}")
    win.config(bg=box_bg)
    win.transient(root)
    win.grab_set()
    
    tk.Label(win, text=title.upper(), font=("Arial", 14, "bold"), bg=box_bg, fg=color).pack(pady=10)
    tk.Label(win, text=text, font=("Arial", 10), bg=box_bg, fg="white", wraplength=250).pack()
    tk.Button(win, text="OK", command=win.destroy, bg=color, fg=bg, font=("Arial", 10,), width=10).pack(pady=15)

def redraw():
    hint_label.config(text=msg)
    display = " ".join([c if c in guesses else "_" for c in word])
    word_label.config(text=display)
    stats_label.config(text=f"Attempts left: {lives}")
    
    canvas.delete("man")
    if lives < 6: canvas.create_oval(115, 95, 185, 165, width=5, outline=fg, tags="man") 
    if lives < 5: canvas.create_line(150, 165, 150, 260, width=5, fill=fg, tags="man")    
    if lives < 4: canvas.create_line(150, 190, 100, 230, width=5, fill=fg, tags="man")    
    if lives < 3: canvas.create_line(150, 190, 200, 230, width=5, fill=fg, tags="man")    
    if lives < 2: canvas.create_line(150, 260, 110, 320, width=5, fill=fg, tags="man")    
    if lives < 1: canvas.create_line(150, 260, 190, 320, width=5, fill=fg, tags="man")    

def play(event=None):
    global lives
    char = input_box.get().lower()
    input_box.delete(0, tk.END)
    if len(char) != 1 or not char.isalpha():
        popup("WAIT! ✋", "Please enter exactly one letter (A-Z).", "#f1c40f")
        return
    if char in guesses:
        popup("ALREADY USED 🔁", f"You already tried '{char.upper()}'. Try something else!", "#3498db")
        return
    guesses.append(char)
    if char not in word:
        lives -= 1
    redraw()
    if all(c in guesses for c in word):
        popup("Winner!", "Brilliant! You saved him.", "#57E44A")
        reset()
    elif lives == 0:
        popup("Lost", f"The word was: {word.upper()}", "#F43D29")
        reset()

def reset():
    setup_game()
    redraw()
    input_box.focus_set()

root = tk.Tk()
root.title("HANGMAN")
root.config(bg=bg)

w, h = 500, 800
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

main_ui = tk.Frame(root, bg=bg)
main_ui.pack(expand=True)

hint_label = tk.Label(main_ui, text="", font=("Arial", 15, "bold italic"), bg=bg, fg="#89B4FA", wraplength=450)
hint_label.pack(pady=20)

game_box = tk.Frame(main_ui, bg=box_bg)
game_box.pack(pady=10, padx=25, fill="x")

canvas = tk.Canvas(game_box, width=300, height=350, bg=box_bg, highlightthickness=0)
canvas.pack(pady=10)
canvas.create_line(40, 330, 260, 330, width=6, fill=fg) 
canvas.create_line(220, 330, 220, 30, width=6, fill=fg)  
canvas.create_line(100, 30, 220, 30, width=6, fill=fg)   
canvas.create_line(150, 30, 150, 95, width=6, fill=fg)  

word_label = tk.Label(game_box, text="", font=("Courier", 38, "bold"), bg=box_bg, fg=accent)
word_label.pack(pady=15)

stats_label = tk.Label(game_box, text="", font=("Arial", 12, "bold"), bg=box_bg, fg=fg)
stats_label.pack(pady=(0, 20))

control_frame = tk.Frame(main_ui, bg=bg)
control_frame.pack(pady=25)

input_box = tk.Entry(control_frame, width=4, font=("Arial", 45, "bold"), justify="center", bg="white", fg="black")
input_box.grid(row=0, column=0, rowspan=2, padx=15)
input_box.focus_set()

tk.Button(control_frame, text="GUESS", command=play, bg="#00FF33", font=("Arial", 11), width=14, height=2).grid(row=0, column=1, pady=3)
tk.Button(control_frame, text="RESET", command=reset, bg="#FF4400", font=("Arial", 11), width=14).grid(row=1, column=1, pady=3)

setup_game()
redraw()
root.bind('<Return>', play)
root.mainloop()