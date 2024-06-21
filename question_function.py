import tkinter as tk
from tkinter import ttk, messagebox
from nltk import word_tokenize
from nltk.corpus import stopwords

# Global variable to store filtered keywords
filtered_key_words = []

# Function to extract key words from a question in Spanish
def keys_from_question(question):
    tokens = word_tokenize(question)
    stop_words = stopwords.words('spanish')
    words = [word for word in tokens if word.isalpha()]
    key_words = [key for key in words if key not in stop_words]
    create_gui(key_words)
    return filtered_key_words

# Function to create the GUI and handle user interaction
def create_gui(key_words):
    # Create the main application window
    root = tk.Tk()
    root.title("Keyword Selector")

    # Function to handle the "Okay" button click
    def on_okay():
        global filtered_key_words
        filtered_key_words = [key_words[i] for i, var in enumerate(checkbox_vars) if var.get()]
        messagebox.showinfo("Selected Keywords", f"Filtered Keywords: {filtered_key_words}")
        root.destroy()

    # Create a frame to hold the checkboxes
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create a list to store the Checkbutton variables
    checkbox_vars = []

    # Add a Checkbutton for each keyword
    for idx, key in enumerate(key_words):
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame, text=key, variable=var)
        checkbox.grid(row=idx, column=0, sticky=tk.W)
        checkbox_vars.append(var)

    # Add the "Okay" button
    okay_button = ttk.Button(frame, text="Okay", command=on_okay)
    okay_button.grid(row=len(key_words), column=0, pady=10)

    # Start the main event loop
    root.mainloop()
