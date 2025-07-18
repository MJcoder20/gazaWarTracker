from datetime import datetime

from openpyxl import Workbook
import openpyxl
import tkinter as tk
from tkinter import messagebox

from processing.calc import *
from visualization.visualize import *


def validate_date():
    date = date_entry.get()

    try:
        # Attempt to parse the date in the desired format (e.g., DD/MM/YYYY)
        valid_date = datetime.strptime(date, "%d/%m/%Y")
        return valid_date
    except ValueError:
        date_entry.delete(0, tk.END)
        messagebox.showerror("Error", "Invalid date format! Please use DD/MM/YYYY.")


def submit_data():
    date = date_entry.get()
    region = region_entry.get()
    martyr_count = martyr_count_entry.get()
    injured_count = injured_count_entry.get()
    damaged_homes_count = damaged_homes_count_entry.get()
    attack_type = attack_type_entry.get()

    if not date or not region or not martyr_count or not injured_count or not damaged_homes_count or not attack_type:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        # Open or create an Excel file
        try:
            workbook = openpyxl.load_workbook("data/Book1.xlsx")
            sheet = workbook.active
        except FileNotFoundError:
            workbook = Workbook()
            sheet = workbook.active
            # Add headers if creating a new file
            sheet.append(['Date', 'Region', "Martyr Count", 'Injured Count', 'Damaged Homes Count', 'Attack Type'])

        regions = ['Shigaeya', 'Baithanoun', 'Baitlahya', 'Nusairat', 'Deir-El-Balah', 'Zawaida', 'Khanyunis',
                   'Rafah', 'Gaza-Jalaa', 'Gaza-El_Saha', 'Gaza-Tuffah', 'Gaza-Rimal', 'Gaza-El_Menaa','Gaza-Tal_El_Hawaa',
                   'Gaza-El_Sheikh_Redawan', 'Gaza-El_Nasser']
        # Append user data
        if validate_date() and region and (region in regions) and martyr_count.isdigit() and injured_count.isdigit() \
                and damaged_homes_count.isdigit() and attack_type and attack_type in \
                ['Ground', 'Arial', 'Naval']:
            sheet.append([validate_date(), region, martyr_count, injured_count, damaged_homes_count, attack_type])
            workbook.save("data/Book1.xlsx")
            messagebox.showinfo("Success", "Data saved successfully!")
            date_entry.delete(0, tk.END)
            region_entry.delete(0, tk.END)
            martyr_count_entry.delete(0, tk.END)
            injured_count_entry.delete(0, tk.END)
            damaged_homes_count_entry.delete(0, tk.END)
            attack_type_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Please check your data! ")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def attacks_window():
    root2 = tk.Tk()
    root2.title("Attacks' Statistics")
    root2.geometry("400x600")
    root2.config(bg="light blue")
    tk.Label(root2, text='Total Martyr Count: ', font=("Helvetica", 9, "bold")).grid(row=7, column=0, padx=15, pady=10)
    tk.Label(root2, text=total_martyr_count()).grid(row=7, column=1, padx=15, pady=10)

    tk.Label(root2, text='Total Injured Count: ', font=("Helvetica", 9, "bold")).grid(row=8, column=0, padx=15, pady=10)
    tk.Label(root2, text=total_injured_count()).grid(row=8, column=1, padx=15, pady=10)

    tk.Label(root2, text='Total Victim Count: ', font=("Helvetica", 9, "bold")).grid(row=9, column=0, padx=15, pady=10)
    tk.Label(root2, text=total_martyr_injured_count()).grid(row=9, column=1, padx=15, pady=10)

    tk.Label(root2, text='Most Damaged Region: ', font=("Helvetica", 9, "bold")).grid(row=10, column=0, padx=15, pady=10)
    tk.Label(root2, text=most_damaged_region()).grid(row=10, column=1, padx=15, pady=10)

    tk.Label(root2, text='Least Damaged Region: ', font=("Helvetica", 9, "bold")).grid(row=11, column=0, padx=15, pady=10)
    tk.Label(root2, text=least_damaged_region()).grid(row=11, column=1, padx=15, pady=10)

    tk.Label(root2, text='Highest Victims Date: ', font=("Helvetica", 9, "bold")).grid(row=12, column=0, padx=15, pady=10)
    tk.Label(root2, text=highest_victims_date()).grid(row=12, column=1, padx=15, pady=10)

    tk.Label(root2, text='Lowest Victims Date: ', font=("Helvetica", 9, "bold")).grid(row=13, column=0, padx=15, pady=10)
    tk.Label(root2, text=lowest_victims_date()).grid(row=13, column=1, padx=15, pady=10)

    tk.Label(root2, text='Attack Type Count: ', font=("Helvetica", 9, "bold")).grid(row=14, column=0, padx=15, pady=10)
    tk.Label(root2, text=attack_type_count()).grid(row=14, column=1, padx=15, pady=10)

    regions = df['Region'].unique()
    tk.Label(root2, text='Martyr Percentage By Region: ', font=("Helvetica", 9, "bold")).grid(row=15, column=0, padx=5, pady=10)
    i = 0
    for region in regions:
        tk.Label(root2, text=region).grid(row=16+i, column=0, padx=10, pady=5)
        tk.Label(root2, text=martyr_percentage_by_region(region)).grid(row=16+i, column=1, padx=10, pady=5)
        i = i+1

    # Allow the window to resize automatically
    root2.update_idletasks()
    root2.minsize(root2.winfo_reqwidth(), root2.winfo_reqheight())

    #Run the application
    root2.mainloop()


def about_usage():
    root3 = tk.Tk()
    root3.title("Usage Instructions")
    root3.geometry("100x100")
    root3.config(bg="light gray")
    tk.Label(root3, text='Basic Usage guidelines ', font=("Helvetica", 12), bg="skyblue").grid(row=7, column=0, padx=15, pady=10)
    tk.Label(root3, text="1. Enter data into all the fields or else none of the data will be stored."
                         "\n\n2. Make sure to enter camel case data(eg., Gaza-Rimal, Zawaida, Gaza-Tal_El_Hawaa, etc.)."
                         "\n\n3. Recently submitted data won't appear in the statistics or the visuals windows, "
                         "so be sure to rerun the app if you have added any new information."
             , font=("Helvetica", 10))\
        .grid(row=8, column=0, padx=15, pady=10)

    # Allow the window to resize automatically
    root3.update_idletasks()
    root3.minsize(root3.winfo_reqwidth(), root3.winfo_reqheight())

    # Run the application
    root3.mainloop()


root = tk.Tk()
root.title("War Data Registry")
root.geometry("200x200")
root.config(bg="light green")


# Menu Bar
menubar = tk.Menu(root)
root.config(menu=menubar)  # Associate the menu bar with the window

statsMenu = tk.Menu(menubar, tearoff=0)  # tearoff=0 removes the dashed line
menubar.add_cascade(label="Statistics", menu=statsMenu)  # Add stats menu to the menubar
statsMenu.add_command(label="Attacks Data", command=attacks_window)  # creates a new window with the calculated stats

visualizeMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Visualization", menu=visualizeMenu)  # Add visualize menu to the menubar
#Each of the following menu items displays a different visual
visualizeMenu.add_command(label="Martyr Count By Date", command=line_chart)
visualizeMenu.add_command(label="Most Damaged Regions", command=damaged_regions_bar_chart)
visualizeMenu.add_command(label="Attack Type Distribution", command=pie_chart)
visualizeMenu.add_command(label="Days with the highest martyr counts", command=martyr_counts_bar_chart)
visualizeMenu.add_command(label="Heatmap of Damaged Homes by Region and Attack Type", command=heatmap)

aboutMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=aboutMenu)  # Add about menu to explain our app's functionality
aboutMenu.add_command(label="Usage", command=about_usage)

# Labels and Entry fields
tk.Label(root, text="Date (DD/MM/YYYY)").grid(row=0, column=0, padx=15, pady=10)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=2, padx=15, pady=10)

tk.Label(root, text="Region").grid(row=1, column=0, padx=15, pady=10)
region_entry = tk.Entry(root)
region_entry.grid(row=1, column=2, padx=15, pady=10)

tk.Label(root, text="Martyr Count").grid(row=2, column=0, padx=15, pady=10)
martyr_count_entry = tk.Entry(root)
martyr_count_entry.grid(row=2, column=2, padx=15, pady=10)

tk.Label(root, text="Injured Count").grid(row=3, column=0, padx=15, pady=10)
injured_count_entry = tk.Entry(root)
injured_count_entry.grid(row=3, column=2, padx=15, pady=10)

tk.Label(root, text="Damaged Homes Count").grid(row=4, column=0, padx=15, pady=10)
damaged_homes_count_entry = tk.Entry(root)
damaged_homes_count_entry.grid(row=4, column=2, padx=15, pady=10)

tk.Label(root, text="Attack Type").grid(row=5, column=0, padx=15, pady=10)
attack_type_entry = tk.Entry(root)
attack_type_entry.grid(row=5, column=2, padx=15, pady=10)

tk.Button(root, text="Submit", fg="white", bg="red", command=submit_data).grid(row=6, column=1, columnspan=1, pady=30)

# Allow the window to resize automatically
root.update_idletasks()
root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())

#Run the application
root.mainloop()
