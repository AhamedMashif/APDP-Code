import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


class Login:
    def __init__(self, root, dashboard):
        self.dashboard = dashboard
        ttk.Style().theme_use("sampathfoodcitylogin")
        self.root = root
        self.root.title("Sampath Food City")
        self.root.state("normal")

        self.root.geometry("1000x600")
        self.mode = "login"  # or "signup"
        self.accent_color = "#FF1320"
        self.account_type = ttk.StringVar(value="Account Type")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.left_frame = ttk.Frame(self.main_frame, width=500, height=600)
        self.left_frame.pack(side=LEFT, fill=BOTH)
        self.left_frame.configure(style="Custom.TFrame")
        self.left_frame.pack_propagate(False)

        image = Image.open("images/coverImage.png")
        self.cover_img = ImageTk.PhotoImage(image)

        ttk.Label(
            self.left_frame,
            image=self.cover_img
        ).pack(expand=True)

        self.right_frame = ttk.Frame(self.main_frame, width=500)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.right_frame.pack_propagate(False)

        self.top_frame = ttk.Frame(self.right_frame, width=500, padding=2)
        self.top_frame.pack(fill=X)

        self.form = ttk.Frame(self.right_frame, width=500)

        self.alert_l = ttk.Label(self.top_frame, width=500, font=("Segoe UI", 15, "bold"), padding=1,
                                 foreground="white", justify="center")
        self.alert_l.pack()

        self.log_sing_btn = ttk.Checkbutton(self.top_frame, text="SIGN IN", bootstyle="round-toggle", offvalue="LOGIN", onvalue="SIGN IN", command=self.toggle_mode, width=10)
        self.log_sing_btn.pack(side=RIGHT)

        ttk.Label(self.top_frame, text="LOGIN").pack(side=RIGHT)

        self.title_label = ttk.Label(self.right_frame, text="LOGIN", font=("Segoe UI", 40, "bold"))
        self.title_label.pack(pady=(15, 30))

        self.form.pack()

        self.f_name = ttk.Entry(self.form, width=30)
        self.f_name_l = ttk.Label(self.form, text="First Name", justify="left", width=32, foreground="black")

        self.l_name = ttk.Entry(self.form, width=30)
        self.l_name_l = ttk.Label(self.form, text="Last Name", justify="left", width=32, foreground="black")

        self.username = ttk.Entry(self.form, width=30)
        self.username_l = ttk.Label(self.form, text="Username", justify="left", width=32, foreground="black")

        self.password = ttk.Entry(self.form, width=30, show="*")
        self.password_l = ttk.Label(self.form, text="Password", justify="left", width=32, foreground="black")

        self.login_btn = ttk.Button(self.form, text="LOGIN", width=20, command=self.submit)

        self.inputs = [self.f_name_l, self.f_name, self.l_name_l, self.l_name, self.username_l, self.username, self.password_l, self.password]

        ttk.Label(self.form).pack(pady=5)

        for i in self.inputs[4:]:
            i.pack()
            if self.inputs.index(i) % 2:
                ttk.Label(self.form).pack(pady=10)

        self.login_btn.pack()

        # Style adjustments
        style = ttk.Style()
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white")
        style.configure("TEntry", fieldbackground="white")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Custom.TFrame", background="#FF1320")

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "signup"
            self.title_label.config(text="SIGN UP")
            self.login_btn.config(text="SIGN UP")
            for i in self.form.winfo_children():
                i.pack_forget()
            for i in self.inputs:
                i.pack()
                if self.inputs.index(i) % 2:
                    ttk.Label(self.form).pack(pady=2)

        else:
            self.mode = "login"
            self.title_label.config(text="LOGIN")
            self.login_btn.config(text="LOGIN")
            for i in self.form.winfo_children():
                i.pack_forget()
            ttk.Label(self.form).pack(pady=5)
            for i in self.inputs[4:]:
                i.pack()
                if self.inputs.index(i) % 2:
                    ttk.Label(self.form).pack(pady=10)

        # ttk.Label(self.form).pack(pady=10)
        self.alert_l.configure(background="white")
        self.login_btn.pack(pady=10)

    def submit(self):
        u = self.username.get()
        p = self.password.get()
        if (u == "user" and p == "123"):
            self.main_frame.pack_forget()
            self.dashboard(self.root)
        else:
            self.alert_l["text"] = "Invalid username or password"
            self.alert_l.configure(background="#FF1320")