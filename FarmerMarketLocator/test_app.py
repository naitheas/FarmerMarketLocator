from app import app
from flask import session
from unittest import TestCase

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FormsTestCase(TestCase):
    def test_register_form(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.asssertIn('<h2>Register!</h2>',html)

    def test_register_submit(self):
        with app.test_client() as client:
            res = client.post('/register',data={
                'username':'Testing@testing.com',
                'password':'Testing',
                'phone':9126565016
            })
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.asssertIn('<h1>Welcome!</h1>',html)

    def test_login_form(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.asssertIn('<h1>Login</h1>',html)

    def test_login_submit(self):
        with app.test_client() as client:
            res = client.post('/login',follow_redirects=True,data={
                'username':'Testing@testing.com',
                'password':'Testing'
            })
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.asssertIn('<h1>Welcome!</h1>',html)
            self.assertEqual(session[CURR_USER_KEY],user.id)

    def test_search(self):
        with app.test_client() as client:
            res = client.post('/search',data={'zip':80016})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<li class="market_link">',html)

class DeleteTestCase(TestCase):
    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post('/users/delete',follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)  
            self.asssertIn('<h2>Register!</h2>',html)


