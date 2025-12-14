# src/utils/file_helpers.py
from tkinter import filedialog, messagebox
import os

def save_dataframe_csv(df):
    try:
        file_path = filedialog.asksaveasfilename(
            title="Save processed file",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Processed file saved to:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")
