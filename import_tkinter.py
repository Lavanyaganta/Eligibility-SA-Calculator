import tkinter as tk

window = tk.Tk()

window.title("Sum Assured Calculator")
window.geometry("500x400")

# Customer Name
name_label = tk.Label(window, text="Customer Name")
name_label.pack()

name_entry = tk.Entry(window)
name_entry.pack()

# Age
age_label = tk.Label(window, text="Age")
age_label.pack()

age_entry = tk.Entry(window)
age_entry.pack()

# Annual Income
income_label = tk.Label(window, text="Annual Income")
income_label.pack()

income_entry = tk.Entry(window)
income_entry.pack()

window.mainloop()