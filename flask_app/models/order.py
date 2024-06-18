from flask_app.config.mysqlconnection import connectToMySQL

class Order:
    db_name = 'rentals'

    @classmethod
    def create(cls, data):
        query = """INSERT INTO orders (user_id, vehicle_id, start_date, end_date, total_price)VALUES (%(user_id)s, %(vehicle_id)s, %(start_date)s, %(end_date)s, %(total_price)s);"""
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL(cls.db_name).query_db(query)
        orders= []
        if orders:
            for order in results:
                orders.append(order)
        return orders

    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM orders WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        orders=[]
        if results:
            for order in orders:
                orders.append(order)
        return orders
            