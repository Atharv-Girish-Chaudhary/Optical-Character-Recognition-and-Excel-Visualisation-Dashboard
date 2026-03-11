import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def read_data(file_path):
    df = pd.read_csv(file_path)
    return df

def plot_chart(ax, x, y, title, xlabel, ylabel):
    ax.bar(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

def update_chart(selection, ax, df, canvas):
    ax.clear()
    if selection in df.columns:
        plot_chart(ax, range(len(df)), df[selection], f"{selection} by Index", "Index", selection)
    else:
        ax.set_title("Invalid Selection")
    canvas.draw()

def create_gui(df, columns_to_exclude=None):
    if columns_to_exclude is None:
        columns_to_exclude = []

    root = tk.Tk()
    root.title("Dashboard")
    root.state('zoomed')

    # Ensure application exits properly on close
    def on_close():
        print("Closing the application.")
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    side_frame = tk.Frame(root, bg="#4C2A85")
    side_frame.pack(side="left", fill="y")

    label = tk.Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
    label.pack(pady=50, padx=20)

    label1 = tk.Label(side_frame, text='Select a column to plot:', bg="#4C2A85", fg="#FFF", font=25)
    label1.pack(padx=20)

    column_names = [col for col in df.columns if col not in columns_to_exclude]
    if not column_names:
        print("No columns available for plotting. Please check the data.")
        return

    combo = ttk.Combobox(side_frame, values=column_names, width=30, font=25)
    combo.pack(padx=10, pady=10)
    combo.current(0)

    charts_frame = tk.Frame(root)
    charts_frame.pack(expand=True)

    fig, ax = plt.subplots(figsize=(15, 9))
    plot_chart(ax, range(len(df)), df[column_names[0]], f"{column_names[0]} by Index", "Index", column_names[0])

    canvas = FigureCanvasTkAgg(fig, charts_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side="left", fill="both", expand=True)

    # Add NavigationToolbar
    toolbar = NavigationToolbar2Tk(canvas, charts_frame)
    toolbar.update()

    def on_combo_change(event):
        selection = combo.get()
        update_chart(selection, ax, df, canvas)

    combo.bind("<<ComboboxSelected>>", on_combo_change)

    root.mainloop()

def main():
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])
    file_path = r'data\raw\CreatedCsvFile.csv'
    
    # Read data
    df = read_data(file_path)

    # Columns to exclude from the GUI
    columns_to_exclude = []

    create_gui(df, columns_to_exclude)

if __name__ == "__main__":
    main()
