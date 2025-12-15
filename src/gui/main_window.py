import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

from src.core.analysis import process_dataframe
from src.config.app_config import load_config, AppConfig
from src.gui.table_view import display_dataframe_table


class IntankDataAnalysisApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("InTank Data Analysis")

        self.df = None
        self.config: Optional[AppConfig] = None
        self.config_path: Optional[str] = None

        # --- Config selection ---
        self.config_btn = tk.Button(root, text="Select Config File", command=self.load_config_file)
        self.config_btn.pack(pady=(10, 4))

        self.config_label = tk.Label(root, text="Config: (not loaded)")
        self.config_label.pack(pady=(0, 10))

        # --- Log file selection ---
        self.select_btn = tk.Button(root, text="Select Log File", command=self.load_log_file, state="disabled")
        self.select_btn.pack(pady=(0, 10))

        # Frame for table preview
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Save button
        self.save_btn = tk.Button(root, text="Save Processed File", command=self.save_file, state='disabled')
        self.save_btn.pack(pady=10)

    def load_config_file(self):
        file_path = filedialog.askopenfilename(
            title="Select config file",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            self.config = load_config(file_path)
            self.config_path = file_path

            # Show a small summary
            n = len(self.config.tanks)
            preview = ", ".join([f"{t.number}:{t.name} (BG{t.ballast_group})" for t in self.config.tanks[:3]])
            suffix = f" | {preview}..." if n > 3 else (f" | {preview}" if n else "")
            self.config_label.config(text=f"Config: {file_path}  (tanks: {n}){suffix}")

            # Enable log selection once config is loaded
            self.select_btn.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config:\n{e}")

    def load_log_file(self):
        file_path = filedialog.askopenfilename(
            title="Select log file",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            if self.config is None:
                raise RuntimeError("Config must be loaded before processing logs")
            
            self.df = process_dataframe(file_path, self.config)
            self.show_table()
            self.save_btn.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def show_table(self):
        if self.df is None:
            return
        display_dataframe_table(self.table_frame, self.df)

    def save_file(self):
        if self.df is None:
            return

        save_path = filedialog.asksaveasfilename(
            title="Save processed CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not save_path:
            return

        try:
            self.df.to_csv(save_path, index=False)
            messagebox.showinfo("Saved", f"Saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")