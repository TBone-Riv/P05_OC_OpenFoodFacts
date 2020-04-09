
import sys
import tkinter as tk
import tkinter.ttk as ttk
from sqlalchemy.sql import select
from sqlalchemy import create_engine

import source.constant as constant
import source.model as model


def create_windows():

    engine = create_engine(constant.ENGINE, encoding='utf-8')
    engine.execute("USE " + constant.DBASE)

    windows = tk.Tk()
    Windows(windows, engine)

    windows.mainloop()


class Windows:

    def __init__(self, windows, engine):

        self.engine = engine

        self.windows = windows

        self.page = 0

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=constant.bgcolor)
        self.style.configure('.', foreground=constant.fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
            [('selected', constant.compcolor), ('active', constant.ana2color)])

        self.windows.geometry("600x450+650+150")
        self.windows.minsize(120, 1)
        self.windows.maxsize(1924, 1061)
        self.windows.resizable(1, 1)
        self.windows.title("Substitue")
        self.windows.configure(background=constant.bgcolor)

        self.products = []

        self.packpage()

    def find(self, product):

        widget_list = self.windows.winfo_children()
        for item in widget_list:
            item.grid_forget()

        detail = ttk.Label(self.windows)

        detail.configure(background=constant.bgcolor)
        detail.configure(foreground=constant.fgcolor)
        detail.configure(font="TkDefaultFont")
        detail.configure(relief="flat")
        detail.configure(anchor='s')
        detail.configure(justify='center')
        detail.configure(text=product.name)

        detail.grid(row=0, column=1, padx=0.2, pady=0.2)

        row = model.Substitute().find(product.product_id)
        self.products = [Substitute(self, product, substitute)
                         for substitute in row][:5]

        row = 0
        column = 1

        for product in self.products:
            product.grid(row=row, column=column)

            row += 1

    def save(self, product_id, association_id):

        model.Substitute().save(product_id, association_id)

        self.packpage()



    def packpage(self):

        widget_list = self.windows.winfo_children()
        for item in widget_list:
            item.grid_forget()

        query = select([model.Product])
        row = [i for i in self.engine.execute(query)][
              0 + 10 * self.page: 10 + 10 * self.page]

        self.products = [Product(windows=self, product=p) for p in row]

        row = 0
        column = 1

        for product in self.products:
            product.grid(row=row, column=column)

            row += 1

            if row == 10 :
                column += 0
                row = 0

        ttk.Button(self.windows, text="<-", command=self.pageplus).grid(row=10, column=0)
        ttk.Button(self.windows, text="->", command=self.pagemoin).grid(row=10, column=2)

    def pageplus(self):

        self.page = self.page - 1 if self.page > 1 else 0

        self.packpage()

    def pagemoin(self):
        self.page = self.page + 1 if self.page < 18 else 19

        self.packpage()


class Product(tk.LabelFrame):

    def __init__(self, windows, product):
        super().__init__(windows.windows)

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
        self.detail.configure(text="info")

        self.detail.grid(row=0, column=0, padx=0.2, pady=0.2)

        self.button = ttk.Button(self)

        self.button.configure(takefocus="")
        self.button.configure(text="find substitute")
        self.button.configure(command= lambda p=product: windows.find(p))

        self.button.grid(row=1, column=0, padx=0.2, pady=0.2)


class Substitute(tk.LabelFrame):

    def __init__(self, windows, product, association):
        super().__init__(windows.windows)

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
        self.detail.configure(text="info")

        self.detail.grid(row=0, column=0, padx=0.2, pady=0.2)

        self.button = ttk.Button(self)

        self.button.configure(takefocus="")
        self.button.configure(text="save")
        self.button.configure(command=
                              lambda p=product.product_id,
                                     a=association.product_id:
                              windows.save(p, a))

        self.button.grid(row=1, column=0, padx=0.2, pady=0.2)


if __name__ == '__main__':
    create_windows()
