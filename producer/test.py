import unittest
import requests
import json
from flask_service.producer.model import *




class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pydb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        db.create_all()
        prod1 = Product (pname='Laptop',pqty='10',pprice='50000')
        db.session.add_all([prod1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_product(self):
        response = self.app.post('/producer/product/',data=dict(pnm='battery',pqty='76',pri='8765'),
                                 follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 201)


    def test_get_all_products(self):
        response = self.app.get('/producer/product/')
        self.assertEqual(len(response.json()),2)
        self.assertEqual(response.status_code, 200)


    def test_update_product(self):
        response = self.app.patch('/producer/product/1',data=dict(pnm='Laptop',pqty='10',pri='55555'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        response = self.app.delete('/producer/product/1',follow_redirects=True)
        self.assertEqual(response.status, '404 NOT FOUND')


if __name__ == '__main__':
    unittest.main()