
import sys
import tkinter as tk
import tkinter.ttk as ttk

import source.constant as constant


class ViewWindow(tk.Tk):

    def __init__(self, command):

        super().__init__()

        self.page = 0

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=constant.bgcolor)
        self.style.configure('.', foreground=constant.fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[
            ('selected', constant.compcolor), ('active', constant.ana2color)
        ])

        self.geometry("1200x800+50+50")
        self.minsize(120, 1)
        self.maxsize(1924, 1061)
        self.resizable(1, 1)
        self.title("Substitute")
        self.configure(background=constant.bgcolor)

        self.command = command

    def clear_window(self):
        """ Clear all widget """

        widget_list = self.winfo_children()
        for item in widget_list:
            item.grid_forget()

    def aff_list_product(self, products, command):
        """ View of the product list """

        self.clear_window()
        self.aff_menu()

        index = 1

        for product in products:

            self.build_product(product,
                               lambda product=product:
                               command(product)
                               ).grid(row=index, column=0, sticky=tk.NSEW)
            index += 1

        self.aff_navigation()

    def aff_list_substitute(self, product, substitutes, command):
        self.clear_window()
        self.aff_menu()

        index = 1

        frame = tk.Frame(self)

        text_product = product.name + \
                       product.stores + \
                       """
'---detail---'
'---detail---'
'---detail---'
'---detail---'"""

        original_product = tk.Text(frame)
        original_product.insert(tk.END, text_product)

        original_product.grid(row=1, column=0, rowspan=5, sticky=tk.NSEW)

        for substitute in substitutes:

            self.build_substitute(
                frame,
                substitute,
                lambda product=product,
                substitute=substitute:
                command(product, substitute)
            ).grid(row=index, column=1, sticky=tk.NSEW)

            index += 1

        frame.grid(row=1, column=0, sticky=tk.NSEW)

    def aff_list_save(self, product_association):
        self.clear_window()
        self.aff_menu()

        index = 1

        for product, substitute in product_association:

            frame = tk.Frame(self)

            tk.Label(frame, text=product).pack()
            tk.Label(frame, text='V').pack()
            tk.Label(frame, text=substitute).pack()

            frame.grid(row=index, column=0, sticky=tk.NSEW)

            index += 1

    def aff_menu(self):
        menu = tk.Frame(self)

        tk.Button(menu,
                  text='Product list',
                  command=self.command['list_product']
                  ).grid(row=0, column=0)

        tk.Button(menu,
                  text='My saved product',
                  command=self.command['list_save']
                  ).grid(row=0, column=3)

        entry = tk.Entry(menu)
        entry.grid(row=0, column=1)

        tk.Button(menu,
                  text='Search',
                  command=lambda entry=entry:
                  self.command['list_product'](search=entry.get())
                  ).grid(row=0, column=2)

        menu.grid(row=0, column=0, sticky=tk.NSEW)

    def aff_navigation(self):
        navigation = tk.Frame(self)

        tk.Button(navigation,
                  text='<--',
                  command=self.command['previous_page']
                  ).grid(row=0, column=0, sticky=tk.W)

        tk.Button(navigation,
                  text='-->',
                  command=self.command['next_page']
                  ).grid(row=0, column=2, sticky=tk.E)

        navigation.grid(row=11, column=0, sticky=tk.NSEW)

    def build_product(self, product, command):

        product_view = ProductView(self,
                                   product,
                                   'find substitute',
                                   command)

        return product_view

    @staticmethod
    def build_substitute(parent, product, command):

        product_view = ProductView(parent,
                                   product,
                                   'save substitute',
                                   command)

        return product_view


class ProductView(tk.LabelFrame):

    def __init__(self, parent, product, text, command):
        super().__init__(parent)

        self.configure(relief='groove')
        self.configure(foreground="black")
        self.configure(text=product.name)
        self.configure(background=constant.bgcolor)

        self.detail = ttk.Label(self)

        self.detail.configure(background=constant.bgcolor)
        self.detail.configure(foreground=constant.fgcolor)
        self.detail.configure(font="TkDefaultFont")
        self.detail.configure(relief="flat")
        self.detail.configure(anchor='s')
        self.detail.configure(justify='center')
        self.detail.configure(text=product.stores)

        self.detail.grid(row=0, column=0, sticky=tk.NSEW)

        button = ttk.Button(self)

        button.configure(takefocus="")
        button.configure(text=text)
        button.configure(command=command)

        button.grid(row=1, column=0, sticky=tk.NSEW)
