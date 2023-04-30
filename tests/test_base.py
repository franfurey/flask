from flask_testing import TestCase
from main import app
from flask import current_app, url_for
from urllib.parse import urljoin


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        return app
    
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'], True)

    # Este de abajo esta dando FAILURE cuando corro tests.
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        expected_location = url_for('hello', _external=True)
        self.assertEqual(response.location, expected_location)


    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)

    def test_hello_post(self):
        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_template(self):
        response = self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-pass'
        }

        response = self.client.post(url_for('auth.login'),
                                     data = fake_form)
    
        server_name = self.app.config['SERVER_NAME'] or 'localhost'
        expected_location = f"http://{server_name}{url_for('index')}"

        self.assertEqual(response.location, expected_location)
