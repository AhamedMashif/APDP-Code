import tkinter.messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as tk
from PIL import Image, ImageTk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from login import Login

from tkinter.filedialog import askopenfilename
from database import Database
from transactions import Transaction
from customer import Customer
from product import Product


class Option:
    def __init__(self, parent, menu, value, variable, is_division=None):
        if is_division is None:
            is_division = dict({"a": 1})
        self.parent = parent
        self.div = value
        self.section = parent.current_section
        self.variable = variable
        self.is_div = is_division

        if isinstance(self.is_div, dict):

            if self.div not in self.is_div.keys():
                menu.add_command(label=self.div, command=self.command)
                self.is_div[self.div] = self
        else:

            menu.add_command(label=self.div, command=self.command)

    def command(self):
        self.variable.set(self.div)
        self.parent.load_data()

        if self.section:
            Dashboard.switch_section(self.parent, self.section.get())


class Dashboard:
    def __init__(self, root):
        self.product_list_1 = dict()
        self.current_product_1 = ttk.StringVar(value="All")
        self.graph_frame = None
        self.root = root
        self.root.state("zoomed")
        ttk.Style().theme_use("sampathfoodcity")
        self.current_section = ttk.StringVar(value="Best-selling Products")
        self.nav_buttons = {}
        self.accent = "#FF1320"
        self.path = "supermarket_sales.csv"
        self.database = Database(self.path).df
        self.root.title("Dashboard")
        self.divisions_list = dict()
        self.product_list = dict()
        self.current_division = ttk.StringVar(value="All")
        self.divisions = None
        self.current_product = ttk.StringVar(value="All")
        self.transactions = Transaction.transactions

        self.main_frame = tk.CTkFrame(root, fg_color="white")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Sidebar (lest side navigation)
        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        image = Image.open("images/logo.jpg")
        image = image.resize((200, 200))
        self.logo = ImageTk.PhotoImage(image)

        # Logo
        ttk.Label(self.sidebar, text="🛒", font=("Segoe UI Emoji", 50), image=self.logo).pack()

        # Navigation buttons
        self.nav_items = {
            "Best-selling Products": self.best_sellers,
            "Product Performance": self.product_analysis,
            "Customer Behaviour": self.customer_behaviour
        }

        self.nav_frame = tk.CTkFrame(self.sidebar)
        self.nav_frame.pack(fill=BOTH)

        for name in self.nav_items:
            btn = tk.CTkLabel(
                self.nav_frame, text=name.upper(), font=("Segoe UI", 12, "bold"),

                height=int((self.nav_frame.winfo_screenheight()-280)/len(self.nav_items)), anchor="center", cursor="hand2"
            )
            btn.pack(fill=BOTH, pady=1)
            btn.bind("<Button-1>", lambda e, n=name: self.switch_section(n))
            self.nav_buttons[name] = btn

        # Body (right side)
        self.body = tk.CTkFrame(self.main_frame, fg_color="white")
        self.body.pack(side=RIGHT, fill=BOTH, expand=True)

        self.top_bar = ttk.Frame(self.body, height=50)
        self.top_bar.pack(fill=X, side=TOP)
        ttk.Label(self.top_bar, text="Region: ", font=("Segoe UI", 15, "bold")).pack(side=LEFT
                                                                                     )
        self.div_select = ttk.Menubutton(self.top_bar, style=LIGHT, textvariable=self.current_division, width=10)
        self.div_select.pack(side=LEFT)

        self.divisions = ttk.Menu(self.div_select)
        # self.divisions.add_command(label="All", command=lambda: self.current_division.set("All"))
        Option(self, self.divisions, "All", self.current_division, self.divisions_list)
        self.div_select["menu"] = self.divisions

        ttk.Button(self.top_bar, text="𓉘➡", style=SECONDARY, command=self.logout).pack(side=RIGHT, pady=10, padx=10)
        ttk.Button(self.top_bar, text="Select File (csv)", style=SUCCESS, command=self.select_file).pack(side=RIGHT,
                                                                                                         pady=10,
                                                                                                         padx=10)

        # Content area
        self.content = tk.CTkFrame(self.body, fg_color="white")
        self.content.pack(fill=BOTH, expand=True)
        self.load_data()

        self.switch_section(list(self.nav_items.items())[0][0])

    def load_data(self):
        Transaction.transactions = dict()
        Product.products = dict()
        Customer.customers = dict()
        Product.regional_sale = dict()
        for row in self.database.values:
            Transaction(*row)
        if self.current_division.get() != "All":
            temp = dict()
            for i in Transaction.regions[self.current_division.get()]:
                try:
                    temp[i] = Transaction.transactions[i]
                except:
                    pass
            Transaction.transactions = temp

        for div in Transaction.regions.keys():
            Option(self, self.divisions, div, self.current_division, self.divisions_list)
        self.div_select["menu"] = self.divisions

    def select_file(self):
        file = askopenfilename(title="Select CSV file", filetypes=[("csv files", "*.csv")])
        if file:
            temp = Database(file)
            if temp.is_same_format():
                self.database = temp.df
                self.clear_all()
                self.switch_section(self.current_section.get())

            else:
                tkinter.messagebox.showerror("Invalid Format", "Invalid file")


    def clear_all(self):
        Transaction.transactions = dict()
        Product.products = dict()
        Customer.customers = dict()
        Product.regional_sale = dict()
        self.load_data()
        self.transactions = Transaction.transactions

    def logout(self):
        for i in self.root.winfo_children():
            i.pack_forget()
        Login(self.root, Dashboard)

    def switch_section(self, section):
        # # Reset all buttons
        for name, btn in self.nav_buttons.items():
            btn.configure(text_color="white", fg_color=self.accent)

        # Highlight selected
        self.nav_buttons[section].configure(text_color=self.accent, fg_color="white", bg_color=self.accent)

        # Clear previous content
        for widget in self.content.winfo_children():
            widget.destroy()

        self.current_section.set(section)
        self.nav_items[self.current_section.get()]()

        # if self.current_section.get() == "Regional Sales":
        #     self.div_select.configure(state=DISABLED)
        # else:
        #     self.div_select.configure(state=ACTIVE)

    # Sample content loaders
    def best_sellers(self):
        counts = dict()
        for t in Transaction.transactions.values():
            counts[t.product.name] = counts.get(t.product.name, 0) + t.quantity

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        title = "Best-Selling Products"

        if self.current_division.get() == "All":
            ax.bar(list(map(lambda x: x.name, Product.products.values())), list(map(lambda x: x.sold, Product.products.values())), color="#FF1320")
        else:
            title = f"Best-Selling Products of {self.current_division.get()}"
            ax.bar(list(map(lambda x: x, Product.regional_sale[self.current_division.get()].keys())), list(map(lambda x: x, Product.regional_sale[self.current_division.get()].values())), color="#FF1320")

        tk.CTkLabel(self.content, text=title, font=("Segoe UI", 35, "bold"), fg_color="white",
                    text_color="#FF1320").pack(pady=15)

        graph_frame = ttk.Frame(self.content)
        graph_frame.pack(fill="both", expand=True)

        ax.set_title("Top-Selling Products")
        ax.set_xlabel("Product")
        ax.set_ylabel("Units Sold")
        ax.grid(axis='y', linestyle='--', alpha=0.6)

        # Embed figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def product_analysis(self):
        months = []

        for p in Product.products.values():
            for i in p.monthly_sale.keys():
                if i not in months:
                    months.append(i)

        product_row = tk.CTkFrame(self.content, fg_color="white")
        product_select = ttk.Menubutton(product_row, textvariable=self.current_product, width=10)

        product_menu = ttk.Menu(product_select, tearoffcommand=lambda x=self.current_section: self.switch_section(x))
        # product_menu.add_command(label="All", command=lambda: current_product.set("All"))
        Option(self, product_menu, "All", self.current_product)
        product_select["menu"] = product_menu

        months = sorted(sorted(months, key=lambda x: int(x.split("/")[0])), key=lambda x: int(x.split("/")[1]))

        products = dict()

        title = "Product Performance Analysis"

        if self.current_division.get() == "All":

            for i, p in enumerate(Product.products.values()):
                temp = 0
                for m in months:
                    products[p.name] = products.get(p.name, []) + [temp + p.monthly_sale.get(m, 0)]
                    temp = products[p.name][-1]

        else:
            title = f"Product Performance Analysis of {self.current_division.get()}"
            for i, p in enumerate(Product.products.values()):
                temp = 0
                for m in months:
                    products[p.name] = products.get(p.name, []) + [temp + p.monthly_regional_sells[self.current_division.get()].get(m, {p.name: 0})[p.name]]
                    temp = products[p.name][-1]

        for p in products.keys():
            Option(self, product_menu, p.title(), self.current_product)

        tk.CTkLabel(self.content, text=title, font=("Segoe UI", 35, "bold"), fg_color="white",
                    text_color="#FF1320").pack(pady=15)

        product_row.pack()

        product_select.pack(side=RIGHT, padx=10)
        tk.CTkLabel(product_row, text="Product: ", font=("Segoe UI", 15, "bold"),
                    fg_color="white",
                    text_color="#FF1320").pack(side=RIGHT)

        graph_frame = tk.CTkFrame(self.content, fg_color="gray")
        graph_frame.pack(fill="both", expand=True)

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        if self.current_product.get() in products.keys():
            ax.plot(months, products[self.current_product.get()], marker='o', label=self.current_product.get(), color="#FF1320")
            ax.set_title(f"Monthly Sales by {self.current_product.get()}")
        else:
            for product, sales in products.items():
                ax.plot(months, sales, marker='o', label=product)

            ax.set_title("Monthly Sales by All Product")
        ax.set_xlabel("Month")
        ax.set_ylabel("Units Sold")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def customer_behaviour(self):
        months = []
        products = dict()
        for p in Product.products.values():
            for i in p.monthly_sale.keys():
                if i not in months:
                    months.append(i)

        product_row = tk.CTkFrame(self.content, fg_color="white")
        product_select_1 = ttk.Menubutton(product_row, textvariable=self.current_product_1, width=10)

        product_menu_1 = ttk.Menu(product_select_1, tearoffcommand=lambda x=self.current_section: self.switch_section(x))
        # product_menu.add_command(label="All", command=lambda: current_product.set("All"))
        Option(self, product_menu_1, "All", self.current_product_1)
        product_select_1["menu"] = product_menu_1

        months = sorted(sorted(months, key=lambda x: int(x.split("/")[0])), key=lambda x: int(x.split("/")[1]))

        title = "Customer Behaviour Insights"

        if self.current_division.get() == "All":
            for i, p in enumerate(Product.products.values()):
                for m in months:
                    products[p.name] = products.get(p.name, []) + [p.monthly_sale.get(m, 0)]

            for p in products.keys():
                Option(self, product_menu_1, p.title(), self.current_product_1)

        else:
            title = f"Customer Behaviour Insights of {self.current_division.get()}"
            for i, p in enumerate(Product.products.values()):
                for m in months:
                    products[p.name] = products.get(p.name, []) + [p.monthly_regional_sells[self.current_division.get()].get(m, dict({p.name: 0}))[p.name]]

            for p in products.keys():
                Option(self, product_menu_1, p.title(), self.current_product_1)

        tk.CTkLabel(self.content, text=title, font=("Segoe UI", 35, "bold"),
                    fg_color="white",
                    text_color="#FF1320").pack(pady=15)

        product_row.pack()

        product_select_1.pack(side=RIGHT, padx=10)
        tk.CTkLabel(product_row, text="Product: ", font=("Segoe UI", 15, "bold"),
                    fg_color="white",
                    text_color="#FF1320").pack(side=RIGHT)

        graph_frame = tk.CTkFrame(self.content, fg_color="gray")
        graph_frame.pack(fill="both", expand=True)

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        if self.current_product_1.get() in products.keys():
            ax.plot(months, products[self.current_product_1.get()], marker='o', label=self.current_product_1.get(),
                    color="#FF1320")
            ax.set_title(f"Monthly Customer Purchases by {self.current_product_1.get()}")
        else:
            for product, sales in products.items():
                ax.plot(months, sales, marker='o', label=product)

            ax.set_title("Monthly Customer Purchases by All Product")
        ax.set_xlabel("Month")
        ax.set_ylabel("No. of Customers")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = ttk.Window()
    app = Dashboard(root)
    root.mainloop()
