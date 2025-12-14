import tkinter as tk
from src.gui.main_window import IntankDataAnalyzerApp

if __name__ == "__main__":
    print("Starting InTank Data Analyzer GUI...")
    root = tk.Tk()
    root.geometry("1000x800")
    app = IntankDataAnalyzerApp(root)
    root.mainloop()