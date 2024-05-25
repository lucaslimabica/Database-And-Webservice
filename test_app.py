from app import app, get_db_connection
import unittest
import json


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True # Defino que estamos no modo de teste 
        app.config['DATABASE'] = ':memory:'
        self.app = app.test_client() # Teste cliente "roda" a app Flask para estar ativo durante o teste

#    def teste_get_units(self):
#        response = self.app.get('/units') # GET neste endpoint
#        self.assertEqual(response.status_code, 200) # Verifica se o status é 200
#        data = json.loads(response.data)
#        self.assertNotEqual(len(data), 0, 'ERROR: Table Unit empty!')
#
#    def test_post_unit(self):
#        response = self.app.post('/units', json={'unit': 'Nintendo Wii', 'description': 'Videogame'})
#        self.assertEqual(response.status_code, 201)
#        app_response = json.loads(response.data)
#        self.assertEqual(app_response['message'], 'Unit added successfully')
#
#        with app.app_context():
#            conn = get_db_connection()
#            cursor = conn.cursor()
#            cursor.execute("SELECT * FROM Unit WHERE unit = 'Nintendo Wii'")
#            select = cursor.fetchone()
#            self.assertIsNotNone(select)
#            self.assertEqual(select['unit'], 'Nintendo Wii')
#            sql = "DELETE FROM Unit WHERE unit = 'Nintendo Wii'"
#            cursor.execute(sql) # Cleaning...
#            conn.commit()
#            cursor.execute("SELECT * FROM Unit WHERE unit = 'Nintendo Wii'")
#            select = cursor.fetchone()
#            self.assertIsNone(select)
#            conn.close()

    def teste_get_sensor(self):
        response = self.app.get('/sensors') 
        self.assertEqual(response.status_code, 200) 
        data = json.loads(response.data)
        self.assertNotEqual(len(data), 0, 'ERROR: Table Sensors empty!')

    def test_post_sensor(self):
        response = self.app.post('/sensors', json={'idLocation': '007', 'name': 'Sensor Bar', 'unit': 'Nintendo Wii'})
        self.assertEqual(response.status_code, 201)
        app_response = json.loads(response.data)
        self.assertEqual(app_response['message'], 'Sensor added successfully')

        with app.app_context(): # Verifica se deu certinho
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNotNone(select, "ERROR: Sensor not added")
            self.assertEqual(select['unit'], 'Nintendo Wii')
            sql = "DELETE FROM Sensor WHERE unit = 'Nintendo Wii'"
            cursor.execute(sql) # Clean the database
            conn.commit()
            cursor.execute("SELECT * FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNone(select)
            conn.close()

    def test_delete_sensor(self):
        response = self.app.post('/sensors', json={'idLocation': '007', 'name': 'Sensor Bar', 'unit': 'Nintendo Wii'})
        self.assertEqual(response.status_code, 201)
        app_response = json.loads(response.data)
        self.assertEqual(app_response['message'], 'Sensor added successfully')

        with app.app_context(): # Realiza a exclusão e a testa
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT idSensor FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNotNone(select, "ERROR: Sensor not added")
            response = self.app.delete(f'sensors/{select['idSensor']}')
            self.assertEqual(response.status_code, 201)
            cursor.execute("SELECT * FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNone(select)
            conn.close()

    def test_put_sensor(self):
        response = self.app.post('/sensors', json={'idLocation': '007', 'name': 'Sensor Bar', 'unit': 'Nintendo Wii'})
        self.assertEqual(response.status_code, 201)
        app_response = json.loads(response.data)
        self.assertEqual(app_response['message'], 'Sensor added successfully')

        with app.app_context(): # Realiza a exclusão e a testa
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT idSensor FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNotNone(select, "ERROR: Sensor not added")
            response = self.app.put(f'sensors/{select['idSensor']}', json={'idLocation': '1903', 'name': 'Joy Sensor', 'unit': 'Nintendo Switch'})
            self.assertEqual(response.status_code, 201)
            cursor.execute("SELECT * FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNone(select)
            conn.close()

    def test_patch_sensor(self):
        response = self.app.post('/sensors', json={'idLocation': '007', 'name': 'Sensor Bar', 'unit': 'Nintendo Wii'})
        self.assertEqual(response.status_code, 201)
        app_response = json.loads(response.data)
        self.assertEqual(app_response['message'], 'Sensor added successfully')

        with app.app_context(): # Realiza a exclusão e a testa
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT idSensor FROM Sensor WHERE name = 'Sensor Bar'")
            select = cursor.fetchone()
            self.assertIsNotNone(select, "ERROR: Sensor not added")
            response = self.app.patch(f'sensors/{select['idSensor']}', json={'idLocation': '1903'})
            self.assertEqual(response.status_code, 201)
            cursor.execute("SELECT * FROM Sensor WHERE idLocation = '007'")
            select = cursor.fetchone()
            self.assertIsNone(select)
            conn.close()

        

if __name__ == '__main__':
    unittest.main()