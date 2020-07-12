import os
from unittest import TestCase
from models import *
from app import check_image, CURR_USER_KEY
from PIL import Image
from flask_mail import Mail, Message
from secret import get_route

from app import app
#os.environ['DATABASE_URL'] = "postgresql:///capstone1-test"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///capstone1-test')



db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

"""These test cases test the admin routes and models."""
class AdminRoutesTestCases(TestCase):

    """Tests the clients navigation"""

    def setUp(self):
        """Create test client, add sample data."""
        Product.query.delete()
        Admin.query.delete()
        Mention.query.delete()
        Visit.query.delete()

        self.client = app.test_client()

        #add an admin. register will add it to the db.session
        self.admin = Admin.register(username='admin',password='password')

        #add a mention for admin home page to display
        self.mention = Mention(date='Jul 07 2020',tweetid='testid',hashtags='hash1, hash2',
        screenname='@testname',text='test text')
        db.session.add(self.mention)

        #add a visit for admin homepage to display
        self.visit = Visit(day='07',month='Jul',year='2020')
        db.session.add(self.visit)
        
        #preparing images
        img_file1 = open('testimage1.jpg', 'rb')
        img_file1 = check_image(img_file1)

        img_file2 = open('testimage2.jpg', 'rb')
        img_file2 = check_image(img_file2)

        self.testproduct = Product(image=img_file1, image1=img_file2, 
        category='box',description='test description1', price=35, 
        available=True, title='test title1')

        self.testgalleryproduct = Product(image=img_file1, image1=img_file2, 
        category='box',description='test description2', price=35, 
        available=False, title='test title2')
        db.session.add(self.testproduct)
        db.session.add(self.testgalleryproduct)

        db.session.commit()

        self.product1_id = self.testproduct.id
        self.product2_id = self.testgalleryproduct.id

        self.username = self.admin.username
        self.password = self.admin.password
        self.visit_year = self.visit.year

        #add a request for admin request. this will be converted into a sale
        self.request = Request(firstname='firstname',lastname='lastname',message='message',
        product=self.product1_id, email='request_test@test.com')
        db.session.add(self.request)

        #add a sale for admin sales page
        self.sale = Sale(email='test@test.com',firstname='firstname',lastname='lastname',
        product=self.product2_id)
        db.session.add(self.sale)
        db.session.commit()

        self.sale_email = self.sale.email
        self.request_id = self.request.id

    def tearDown(self):
        db.session.rollback()

    def test_get_admin_login_page(self):
        """This should display twitter stats and twitter mentions if logged in"""
        #first test getting the login page
        with self.client as c:
            resp = c.get(f'/{get_route()}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('username', html)

    def test_post_admin_login_page(self):
        #test logging in
        with self.client as c:
            #with c.session_transaction() as sess:
                #sess[CURR_USER_KEY] = self.admin
            resp = c.post(f'/{get_route()}', data={'username':'admin',
            'password':'password'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('@testname', html)
            self.assertIn('test text', html)
            self.assertIn('hash1, hash2', html)
            
            #the page creates buttons that use a year as innerText. This year comes
            #from a Visit model.
            self.assertIn(f'button-{self.visit_year}', html)

    def test_admin_session_on_admin_start_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('@testname', html)
            self.assertIn('test text', html)
            self.assertIn('hash1, hash2', html)
    
    def test_admin_session_on_admin_start_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('username', html)

    def test_admin_session_on_requests_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/view-requests', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Requests', html)

    def test_admin_session_on_requests_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}/view-requests', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('What is Rosemaling?', html)

    def test_admin_session_on_sales_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/sales', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{self.sale_email}', html)

    def test_admin_session_on_sales_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}/sales', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('What is Rosemaling?', html)

    def test_admin_delete_request_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/delete/request/{self.request_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'test@test.com', html)

    def test_admin_delete_request_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}/delete/request/{self.request_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('What is Rosemaling?', html)

    def test_admin_sold_request_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/sold/{self.request_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'test@test.com', html)

    def test_admin_sold_request_sales_route(self):
        """This test ensures a request turns into a sale,
        when a product is sold."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/sold/{self.request_id}', 
            follow_redirects=True)
            resp = c.get(f'/{get_route()}/sales')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'request_test@test.com', html)

    def test_admin_sold_request_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}/sold/{self.request_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'What is Rosemaling?', html)

    def test_admin_delete_product_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/delete/{self.product1_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'test title1', html)

    def test_admin_delete_product_from_gallery_logged_in(self):
        """This isn't much different from the one above. Products
        that aren't available are shown in the gallery vs the products."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/delete/{self.product2_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'test title2', html)

    def test_admin_delete_product_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}/delete/{self.product1_id}', 
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'What is Rosemaling?', html)

    def test_admin_view_products_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            resp = c.get(f'/{get_route()}/view-products',
            follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            #should see both test products because admin products page shows both
            self.assertIn('test title1', html)
            self.assertIn('test title2', html)

    def test_admin_view_products_route_logged_out(self):
        with self.client as c:
            resp = c.get(f'/{get_route()}/view-products',
            follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'What is Rosemaling?', html)

    def test_admin_add_product_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            
            #prepare data to post
            data = {'title':'test title','category':'box',
            'description':'test description', 'price':'34',
            'available':True,'image': open('testimage1.jpg', 'rb')}
            
            resp = c.post(f'/{get_route()}/view-products', data=data, 
            follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test title', html)
            self.assertIn('Product added to database', html)

    def test_admin_update_product_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            
            #prepare data to post. dont need as much data
            data = {'title':'changed title',
            'description':'test description','changeimage':True,
            'available':True,'image': open('testimage2.jpg', 'rb')}

            resp = c.post(f'/{get_route()}/{self.product1_id}', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('changed title', html)

    def test_admin_add_product_fail_route_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.username
            
            #prepare data to post
            data = {'title':'test title','category':'box',
            'description':'test description', 'price':'asdf',
            'available':True,'image': open('testimage1.jpg', 'rb')}
            
            resp = c.post(f'/{get_route()}/view-products', data=data, 
            follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Product not added to database.', html)