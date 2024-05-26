import unittest
import warnings
from final import app
import json



class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
    warnings.simplefilter("ignore", category=DeprecationWarning)
    warnings.simplefilter("ignore", category=DeprecationWarning)
        
    def test_get_equipment(self):
        response = self.app.get('/equipment')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)  

    def test_get_equipment_by_id(self):
        response = self.app.get('/equipment/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)  

    def test_add_equipment(self):
        new_equipment = {
            "equipment_type_code": "ETC456",
            "equipment_details": "New equipment details"
        }
        response = self.app.post('/equipment', json=new_equipment)
        self.assertEqual(response.status_code, 201)

    def test_update_equipment(self):
        updated_equipment = {
            "equipment_type_code": "ETC789",
            "equipment_details": "Updated equipment details"
        }
        response = self.app.put('/equipment/1', json=updated_equipment)
        self.assertEqual(response.status_code, 200)

    def test_delete_equipment(self):
        response = self.app.delete('/equipment/1')
        self.assertEqual(response.status_code, 200)

    def test_get_equipment_params(self):
        response = self.app.get('/equipment/format?equipment_type_code=ETC123&equipment_details=Details')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data["equipment_type_code"], "ETC123")
        self.assertEqual(data["equipment_details"], "Details")


if __name__ == "__main__":
    unittest.main()
