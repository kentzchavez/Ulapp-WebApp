import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import subprocess

# Initialize df as a global variable
df = None

# Function to handle the submission of data
def submit_data():
    global df  # Declare df as a global variable
    day = int(day_var.get())
    month = int(month_var.get())
    year = int(year_var.get())

    try:
        date = datetime(year, month, day).strftime("%Y-%m-%d")  # Format the date
    except ValueError:
        messagebox.showerror("Error", "Invalid date. Please select a valid date.")
        return

    url = entry_url.get()
    title = entry_title.get()
    author = entry_author.get()
    source = source_var.get()  # Get the selected source from the dropdown

    # Read the existing Excel file, if it exists
    try:
        df = pd.read_excel("articles.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "URL", "Title", "Author", "Source", "Logo"])

    # Check for duplicate titles in the Excel file
    if title in df['Title'].values:
        messagebox.showerror("Error", "Article with the same title already exists in the Excel file.")
    else:
        # Define the logo mapping
        logo_mapping = {
            "ABS-CBN News": "external/abs_cbn.png",
            "Inquirer": "external/inquirer.png",
            "GMA News": "external/gma.png",
            "PNA": "external/pna.png",
            "Rappler": "external/rapppler.png"  # Add the corresponding value for Rappler if available
        }

        # Append the new data to the DataFrame
        new_data = {'Date': date, 'URL': url, 'Title': title, 'Author': author, 'Source': source, 'Logo': logo_mapping.get(source, "")}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Save the entire DataFrame to the Excel file
        df.to_excel("articles.xlsx", index=False)

        # Prompt the user to add another entry and clear the form
        messagebox.showinfo("Success", "Article added successfully!")
        clear_entries()

        # Run the 'sort_ex.py' script
        subprocess.run(["python", "sort_ex.py"])

# Function to clear the text entry fields
def clear_entries():
    day_var.set("1")
    month_var.set("1")
    year_var.set("2023")
    entry_url.delete(0, 'end')
    entry_title.delete(0, 'end')
    entry_author.delete(0, 'end')

# Create the main window
window = tk.Tk()
window.title("Article Entry App")

# Create drop-down lists and labels for date selection
day_var = tk.StringVar()
month_var = tk.StringVar()
year_var = tk.StringVar()

source_var = tk.StringVar()
sources = ["Rappler", "GMA News", "PNA", "Inquirer", "ABS-CBN News"]

days = [str(i) for i in range(1, 32)]
months = [str(i) for i in range(1, 13)]
years = [str(i) for i in range(2000, 2030)]

tk.Label(window, text="Day:").grid(row=0, column=0)
day_dropdown = tk.OptionMenu(window, day_var, *days)
day_dropdown.grid(row=0, column=1)

tk.Label(window, text="Month:").grid(row=1, column=0)
month_dropdown = tk.OptionMenu(window, month_var, *months)
month_dropdown.grid(row=1, column=1)

tk.Label(window, text="Year:").grid(row=2, column=0)
year_dropdown = tk.OptionMenu(window, year_var, *years)
year_dropdown.grid(row=2, column=1)

tk.Label(window, text="URL:").grid(row=3, column=0)
entry_url = tk.Entry(window)
entry_url.grid(row=3, column=1)

tk.Label(window, text="Title:").grid(row=4, column=0)
entry_title = tk.Entry(window)
entry_title.grid(row=4, column=1)

tk.Label(window, text="Author:").grid(row=5, column=0)
entry_author = tk.Entry(window)
entry_author.grid(row=5, column=1)

tk.Label(window, text="Source:").grid(row=6, column=0)
source_dropdown = tk.OptionMenu(window, source_var, *sources)
source_dropdown.grid(row=6, column=1)

# Create a submit button
submit_button = tk.Button(window, text="Submit", command=submit_data)
submit_button.grid(row=7, column=0, columnspan=2)

# Read the existing Excel file, if it exists
try:
    df = pd.read_excel("articles.xlsx")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "URL", "Title", "Author", "Source", "Logo"])

window.mainloop()
