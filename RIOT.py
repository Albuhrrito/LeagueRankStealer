import tkinter as tk
from tkinter import ttk
from functions import fetch_data

# GUI CODE
root = tk.Tk()
root.title("Riot API GUI")

game_name_label = ttk.Label(root, text="Enter game name:")
game_name_label.pack(pady=10)

game_name_entry = ttk.Entry(root, width=30)
game_name_entry.pack(pady=5)

tag_line_label = ttk.Label(root, text="Enter tag line:")
tag_line_label.pack(pady=10)

tag_line_entry = ttk.Entry(root, width=30)
tag_line_entry.pack(pady=5)

output_label = ttk.Label(root, text="")
output_label.pack(pady=10)

def on_fetch_data():
    game_name = game_name_entry.get()
    tag_line = tag_line_entry.get()
    fetch_data(game_name, tag_line, output_label)

fetch_button = ttk.Button(root, text="Fetch Data", command=on_fetch_data)
fetch_button.pack(pady=10)

root.mainloop()
