import tkinter as tk
from src.gui.main_window import IntankDataAnalysisApp

if __name__ == "__main__":
    print("Starting InTank Data Analysis GUI...")
    root = tk.Tk()
    root.geometry("1000x800")
    app = IntankDataAnalysisApp(root)
    root.mainloop()