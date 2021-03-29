import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Chocolate, Chocolatier

manager_token = str(os.environ['MANAGER'])
customer_token = str(os.environ['CUSTOMER'])
bad_token = str(os.environ['MANAGER_INVALID'])


class ChocolateTestCase(unittest.TestCase):

    def setUp(self):
        
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "chocolate"
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)

        self.new_chocolate = {
            'name':'truffle sublime',
            'chocolate_type':'dark chocolate',
            'vendor':'Divine Chocolate',
            'vendor_id':1, 
            'comments': 'Best truffles ever!'
        }
        self.new_chocolatier = {
            'name':'Divine Chocolate',
            'address':'123 Sweets Lane',
            'website':'www.testwebsite.com',
            'facebook':'www.facebook.com',
            'phone':'123-345-5678',
            'chef':'Beth Carrington',
            'comments':'Try our new truffles!'
        }

        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        print('***Test Setup Completed***')
    
    def tearDown(self):
        print('***Test TearDown Completed***')
        pass

    #TODO: Add token authentication to each
    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_chocolates(self):
        res = self.client().get('/chocolates', headers={'Authorization':'Bearer '+customer_token})
        print('debugging valid chocolates get request: '+str(res))
        #print(res.data)
        data = json.loads(res.data.decode('utf-8'))
        #print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Chocolates'])

    def test_chocolates_error_404(self):
        res = self.client().get('/chocolates/id', headers={'Authorization':'Bearer '+customer_token})
        print('debugging invalid chocolates get request: '+str(res))
        data=json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found. Sorry!')

    def test_get_chocolatiers(self):
        res = self.client().get('/chocolatiers', headers={'Authorization':'Bearer '+customer_token})
        print('debugging valid chocolatier get request: '+str(res))
        #print(res.data)
        data = json.loads(res.data.decode('utf-8'))
        #print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Chocolatiers'])

    def test_chocolatiers_error_404(self):
        res = self.client().get('/chocolatiers/id', headers={'Authorization':'Bearer '+customer_token})
        print('debugging invalid chocolatier get request: '+str(res))
        data=json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found. Sorry!')

    
    def test_create_chocolate(self):
        res = self.client().post('/chocolates', json=self.new_chocolate, headers={'Authorization':'Bearer '+customer_token})
        print('debugging successful create chocolate: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], True)
        self.assertEqual(data['name'], True)
        self.assertEqual(data['total_chocolates'], True)


    def test_create_chocolate_empty_422(self):
        res = self.client().post('/chocolates', headers={'Authorization':'Bearer '+customer_token})
        print('debugging create chocolate empty: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable. This request was formatted well, but may have semantic errors.')
    
    def test_create_chocolatier(self):
        res = self.client().post('/chocolatiers', json=self.new_chocolatier, headers={'Authorization':'Bearer '+manager_token})
        print('debugging successful create chocolatier: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], True)
        self.assertEqual(data['name'], True)
        self.assertEqual(data['total_chocolatiers'], True)

    def test_create_chocolatier_empty_422(self):
        res = self.client().post('/chocolatiers', headers={'Authorization':'Bearer '+manager_token})
        print('debugging create chocolatier empty: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable. This request was formatted well, but may have semantic errors.')

    def test_update_chocolate(self):
        res = self.client().patch('/chocolates/1', json={'comments':'updated comment'}, headers={'Authorization':'Bearer '+customer_token})
        print('debugging successful update chocolate: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['chocolate'], True)


    def test_update_chocolate_empty_405(self):
        res = self.client().patch('/chocolates', headers={'Authorization':'Bearer '+customer_token})
        print('debugging update chocolate empty: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'That method is not allowed for this endpoint.')

    def test_update_chocolatier(self):
        res = self.client().patch('/chocolatiers/1', json={'comments':'updated comment'}, headers={'Authorization':'Bearer '+manager_token})
        print('debugging successful update chocolatier: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['chocolatier'], True)


    def test_update_chocolatier_422(self):
        res = self.client().patch('/chocolatiers/17890', headers={'Authorization':'Bearer '+manager_token})
        print('debugging update chocolatier empty: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable. This request was formatted well, but may have semantic errors.')

    def test_delete_chocolate(self):
        res = self.client().delete('/chocolates/2', headers={'Authorization':'Bearer '+manager_token})
        print('debugging normal delete: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        chocolate=Chocolate.query.filter(Chocolate.id==3).one_or_none()
        print(chocolate)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(chocolate, None)

    def test_delete_nonexistent_chocolate_422(self):
        res = self.client().delete('/chocolates/29480238', headers={'Authorization':'Bearer '+manager_token})
        print('debugging delete nonexistent: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable. This request was formatted well, but may have semantic errors.')

    def test_delete_chocolatier(self):
        res = self.client().delete('/chocolatiers/2', headers={'Authorization':'Bearer '+manager_token})
        print('debugging normal delete: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        chocolatier=Chocolatier.query.filter(Chocolatier.id==2).one_or_none()
        print(chocolatier)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(chocolatier, None)

    def test_delete_nonexistent_chocolatier_422(self):
        res = self.client().delete('/chocolatiers/83970238', headers={'Authorization':'Bearer '+manager_token})
        print('debugging delete nonexistent: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable. This request was formatted well, but may have semantic errors.')

    def test_successful_search(self):
        res = self.client().post('/chocolates/search', json={'searchTerm':'choco'}, headers={'Authorization':'Bearer '+customer_token})
        print('debugging test_successful_search: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['chocolates'])

    def test_invalid_search(self):
        res = self.client().post('/chocolates/search', headers={'Authorization':'Bearer '+customer_token})
        print('debugging test_invalid_search: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found. Sorry!')

    #TODO: RBAC specific tests
    #Customer auth success
    def test_create_chocolate_allowed(self):
        res = self.client().post('/chocolates', json=self.new_chocolate)
        print('debugging customer successful create chocolate: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], True)
        self.assertEqual(data['name'], True)
        self.assertEqual(data['total_chocolates'], True)
    #Customer auth failure
    def test_create_chocolatier_not_allowed_401(self):
        res = self.client().post('/chocolatiers', json=self.new_chocolatier)
        print('debugging customer create chocolatier no permission : '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication failed')

    #Manager auth success
    def test_delete_chocolate_allowed(self):
        res = self.client().delete('/chocolates/3', headers={'Authorization':'Bearer '+manager_token})
        print('debugging manager delete auth success: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        chocolate=Chocolate.query.filter(Chocolate.id==3).one_or_none()
        print(chocolate)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)
        self.assertEqual(chocolate, None)
    #Manager failure(has permissions, but invalid token or some sort of corruption)
    def test_create_chocolatier_bad_token(self):
        res = self.client().post('/chocolatiers', json=self.new_chocolatier, headers={'Authorization':'Bearer '+bad_token})
        print('debugging create chocolatier manager invalid token: '+str(res))
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication failed')


    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()