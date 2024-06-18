from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Vehicle:
    db_name = 'rentals'
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.type = data['type']
        self.model = data['model']
        self.description = data['description']
        self.image= data['image']
        self.price= data['price']
        self.created_at = data['created_at']
        self.updated_at= data['updated_at']

    @classmethod
    def create(cls,data):
        query = 'INSERT INTO vehicles (user_id, type, model, description, image, price) VALUES ( %(user_id)s, %(type)s, %(model)s, %(description)s, %(image)s, %(price)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllVehicles(cls):
        query = 'SELECT * FROM vehicles;'
        results = connectToMySQL(cls.db_name).query_db(query)
        vehicles= []
        if vehicles:
            for vehicle in results:
                vehicles.append(vehicle)
        return vehicles

    @classmethod
    def get_logged_vehicles(cls,data):
        query = "SELECT * FROM vehicles where user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        vehicles=[]
        if results:
            for vehicle in results:
                vehicles.append(vehicle)
        return vehicles
            

    @classmethod
    def get_vehicle_by_id(cls,data):
        query = "SELECT * FROM vehicles left join users on vehicles.user_id = users.id WHERE vehicles.id = %(vehicle_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete_vehicle(cls,data):
        query = 'DELETE FROM vehicles WHERE id=%(vehicle_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_vehicle(cls,data):
        query = 'UPDATE vehicles set type = %(type)s, model = %(model)s, description = %(description)s, price = %(price)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_users_vehicles(cls,data):
        query = 'DELETE FROM vehicles Where vehicles.user_id=%(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def addFavourite(cls,data):
        query= 'INSERT INTO favourites (user_id, vehicle_id) VALUES (%(id)s, %(vehicle_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeFavourite(cls,data):
        query= 'DELETE FROM favourites where vehicle_id = %(vehicle_id)s and user_id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllFavourites(cls,data):
        query = 'SELECT user_id from favourites where favourites.vehicle_id = %(vehicle_id)s;'
        results =connectToMySQL(cls.db_name).query_db(query, data)
        allFavourites=[]
        if results:
            for person in results:
                allFavourites.append(person['user_id'])
        return allFavourites
    
    @classmethod
    def getAllFavouritesInfo(cls,data):
        query = 'SELECT * FROM favourites left join users on favourites.user_id = user_id where favourites.vehicle_id=%(vehicle_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        favourites =[]
        if results:
            for person in results:
                favourites.append(person)
        return favourites
    
    @classmethod
    def delete_all_favourites(cls,data):
        query = 'DELETE FROM favourites Where vehicle_id =%(vehicle_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_vehicle(data):
        is_valid = True
        if len(data['type'])<2:
            flash('Type of vehicle should include more than 2 characters!','type')
            is_valid=False
        if len(data['model'])<2:
            flash('Model of vehicle should include more than 2 characters!', 'model')
            is_valid=False
        if len(data['description'])<2:
            flash('Description should include more than 2 characters!', 'description')
            is_valid=False
        if not data['price']:
            flash('Price of vehicle must not be blank!', 'price')
            is_valid=False
        return is_valid