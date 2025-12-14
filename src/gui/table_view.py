# src/gui/table_view.py
import tkinter as tk
from tkinter import ttk

def display_dataframe_table(parent_frame, df):
    """Display a pandas DataFrame in a Tkinter Treeview inside parent_frame."""

    # Destroy previous tree if exists
    for widget in parent_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(parent_frame, show='headings')
    tree.pack(fill='both', expand=True)

    # Add columns
    tree["columns"] = list(df.columns)
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Add rows
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # Add vertical scrollbar
    scrollbar = ttk.Scrollbar(parent_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    return tree
