import main
import tkinter as tk
from tkinter import ttk
# Create the tkinter window
window = tk.Tk()
window.title("Search Page")

# Define the search function


def search():
    global raushan
    raushan = search_box.get()
    # print("Searched value:", raushan)
    window.quit()  # exit the tkinter event loop


# Create the search box and search button
search_box = ttk.Entry(window)
search_button = ttk.Button(window, text="Search", command=search)

# Add the widgets to the window
search_box.pack(pady=10)
search_button.pack(pady=10)

# Start the tkinter event loop

window.mainloop()
window.update()
main.name = raushan
print(main.name)
main.run1()
