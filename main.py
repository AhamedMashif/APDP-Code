import ttkbootstrap as ttk
from login import Login
from dashboard import Dashboard


if __name__ == "__main__":
    root = ttk.Window()
    dashboard = Dashboard
    app = Login(root, dashboard)
    root.mainloop()
