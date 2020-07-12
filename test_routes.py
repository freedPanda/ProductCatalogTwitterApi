import os
from unittest import TestCase
from models import *
from app import check_image
from PIL import Image
from flask_mail import Mail, Message

from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///capstone1-test')


db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

"""These test cases test the navigation from one page to another."""
class ClientRoutesTestCases(TestCase):

    """Tests the clients navigation"""

    def setUp(self):
        """Create test client, add sample data."""
        Product.query.delete()

        self.client = app.test_client()

        """example: Product(image=image, image1=image1,image2=image2,
            image3=image3,category=category,description=description,
            price=price, available=available, title=title)"""

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

    def tearDown(self):
        db.session.rollback()

    def test_home_route(self):
        with self.client as c:

            resp = c.get(f'/index')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('HISTORY', html)

    def test_product_route(self):
        with self.client as c:

            resp = c.get(f'/products')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test title1', html)

    def test_product_individual_route(self):
        with self.client as c:

            resp = c.get(f'/products/{self.product1_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test description1', html)

    def test_gallery_route(self):
        with self.client as c:

            resp = c.get(f'/gallery')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test title2', html)

    def test_gallery_product(self):
        with self.client as c:

            resp = c.get(f'/gallery/{self.product2_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test description2', html)

    def test_events_route(self):
        with self.client as c:

            resp = c.get(f'/events')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Upcoming Events', html)

    def test_contact_route(self):
        with self.client as c:

            resp = c.get(f'/contact')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Contact Me', html)

    def test_request_route(self):
        """This route sends emails. If the confirmation page is displayed then the email was sent."""
        with self.client as c:
            #NEED TO PROVIDE OWN EMAIL
            data = {'email':'hjorth.chris@yahoo.com', 'firstname':'test fn', 'lastname':'test ln',
            'message':'test message'}
            resp = c.post(f'/products/{self.product1_id}', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Request Confirmed!', html)

            #TEST SENDING PROVIDING BAD EMAIL ADDRESS
            data = {'email':'awefawf.com', 'firstname':'test fn', 'lastname':'test ln',
            'message':'test message'}
            resp = c.post(f'/products/{self.product1_id}', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please provide a valid email', html)

            
