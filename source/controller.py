
from sqlalchemy import create_engine
from source.constant import ENGINE, DBASE
from source.view import ViewWindow
from source.model import RequestDBase, OperationDBase


class Controller:

    def __init__(self):

        self.engine = None
        self.window = None
        self.page = 1

    def init_engine(self):
        """ Create engine """

        self.engine = create_engine(ENGINE, encoding='utf-8')
        self.engine.execute("USE " + DBASE)

    def init_window(self):
        """ Create the maine frame """

        command = {'list_save': self.save_substitute_page,
                   'list_product': self.load_main_page,
                   'next_page': self.next_page,
                   'previous_page': self.previous_page}

        self.window = ViewWindow(command)

        self.load_main_page()

        self.window.mainloop()

    def load_main_page(self, search=None):
        """ Call the view of the product list """

        products = RequestDBase.get_products(
            self.page, self.engine, search=search)
        self.window.aff_list_product(products, self.substitute_page)

    def next_page(self):
        """ Call the next page view """

        self.page += 1
        self.load_main_page()

    def previous_page(self):
        """ Call the previous page view """

        self.page -= 1 if self.page > 1 else 0
        self.load_main_page()

    def substitute_page(self, product):
        """ Call the view of the substitute list """

        products = RequestDBase.get_similar(
            product.product_id, self.engine)
        self.window.aff_list_substitute(
            product, products, self.save_substitute)

    def save_substitute_page(self):
        """ Call the view of the saved product """

        product_association = RequestDBase.get_save_substitute(1, self.engine)
        self.window.aff_list_save(product_association)

    def save_substitute(self, product, substitute):
        """ Call the saving method """

        OperationDBase.save(
            product.product_id, substitute.product_id, self.engine)

        self.load_main_page()


if __name__ == '__main__':
    controller = Controller()
    controller.init_engine()
    controller.init_window()
    controller.load_main_page()
