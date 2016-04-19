import tornado.httpserver
import tornado.ioloop
import tornado.web
import sqlite3
import sys

_db = sqlite3.connect('database.db')
_cursor = _db.cursor()

class dbHandler(tornado.web.RequestHandler):
        def delete(self):
                _cursor.execute("DROP TABLE IF EXISTS item")
                _cursor.execute("CREATE TABLE item (item VARCHAR, price REAL, quantity INT)")
                _cursor.execute("INSERT INTO item VALUES ('grape',0.00,0)")
                _cursor.execute("INSERT INTO item VALUES ('bat',0.00,0)")
                _db.commit()
                self.write('OK')
        def get(self):
                for line in _db.iterdump():
                        self.write('%s\n' % line)

class grapeRequestHandler(tornado.web.RequestHandler):
        def put(self):
                price = self.get_argument("price",default="")
                quantity = self.get_argument("quantity",default="")
                if price != "":
                        _cursor.execute("UPDATE item SET price=? WHERE item = 'grape'", (price,))

                if quantity != "":
                        _cursor.execute("UPDATE item SET quantity=? WHERE item = 'grape'", (quantity,))

                _db.commit()
                self.write('OK')


        def get(self):
                price = self.get_argument("price", default="")
                quantity = self.get_argument("quantity", default="")
                value = self.get_argument("value",default="")
                if price != "":
                        _cursor.execute("SELECT price FROM item WHERE item = 'grape'")
                        price1 = 0.00
                        for row in _cursor:
                                price1 = row[0]
                        self.write('grape unit price: ' + str("{0:.2f}".format(price1)))

                elif quantity != "":
                        _cursor.execute("SELECT quantity FROM item WHERE item = 'grape'")
                        quantity = 0
                        for row in _cursor:
                                quantity1 = row[0]
                        self.write('grape stock level: ' + str("{0}").format(quantity1))

                elif value == 'true':
                        _cursor.execute("SELECT price,quantity FROM item WHERE item = 'grape'")
                        price1 = 0.00
                        quantity1 = 0
                        for row in _cursor:
                                price1 = row[0]
                                quantity1 = row[1]
                        val = price1*quantity1
                        self.write('grape total stock value: ' + str("{0:.2f}".format(val)))

class batRequestHandler(tornado.web.RequestHandler):
        def put(self):
                price = self.get_argument("price",default="")
                quantity = self.get_argument("quantity",default="")
                if price != "":
                        _cursor.execute("UPDATE item SET price=? WHERE item = 'bat'", (price,))

                elif quantity != "":
                        _cursor.execute("UPDATE item SET quantity=? WHERE item = 'bat'", (quantity,))

                _db.commit()
                self.write('OK')
        def get(self):
                quantity = self.get_argument("quantity", default="")
                price = self.get_argument("price", default="")
                value = self.get_argument("value", default="")
                if price != "":
                        _cursor.execute("SELECT price FROM item WHERE item = 'bat'")
                        price1 = 0.00
                        for row in _cursor:
                                price1 = row[0]
                        self.write('bat unit price: ' + str("{0:.2f}".format(price1)))
                elif quantity != "":
                        _cursor.execute("SELECT quantity FROM item WHERE item = 'bat'")
                        quantity1 = 0
                        for row in _cursor:
                                quantity1 = row[0]
                        self.write('bat stock level: ' + str("{0}").format(quantity1))
                elif value == 'true':
                        _cursor.execute("SELECT price,quantity FROM item WHERE item = 'bat'")
                        price1 = 0.00
                        quantity1 = 0
                        for row in _cursor:
                                price1 = row[0]
                                quantity1 = row[1]
                        val = price1*quantity1
                        self.write('bat total stock value: ' + str("{0:.2f}".format(val)))

application = tornado.web.Application([
        (r"/database", dbHandler),
        (r"/item/grape", grapeRequestHandler),
        (r"/item/bat", batRequestHandler),
])

if __name__ == "__main__":
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(43205)
        tornado.ioloop.IOLoop.instance().start()
