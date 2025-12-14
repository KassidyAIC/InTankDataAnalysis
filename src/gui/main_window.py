# src/gui/main_window.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.core.analysis import load_log_file, process_dataframe

class IntankDataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InTank Data Analysis")
        self.df = None

        # Button to select file
        self.select_btn = tk.Button(root, text="Select Log File", command=self.load_file)
        self.select_btn.pack(pady=10)

        # Frame for table preview
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Save button
        self.save_btn = tk.Button(root, text="Save Processed File", command=self.save_file, state='disabled')
        self.save_btn.pack(pady=10)

        # Treeview for table preview
        self.tree = None

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select log file",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls")]
        )
        if not file_path:
            return

        try:
            self.df = load_log_file(file_path)         # returns DataFrame
            self.df = process_dataframe(self.df)       # process

            self.show_table()
            self.save_btn.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def show_table(self):
        from src.gui.table_view import display_dataframe_table  # import table helper
        display_dataframe_table(self.table_frame, self.df)

    def save_file(self):
        from src.utils.file_helpers import save_dataframe_csv
        save_dataframe_csv(self.df)
