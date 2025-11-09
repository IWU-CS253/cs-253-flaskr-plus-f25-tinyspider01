import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def test_edit(self):
        rv = self.app.get('/edit', data=dict(
            title='<Hello>'
        ), follow_redirects=True)
        assert b'&lt;Hello&gt;' in rv.data

    def test_sort(self):
        rv = self.app.post('/sort', data=dict(
            category = 'A category'
        ), follow_redirects=True)
        assert b'A category'

    def test_delete(self):
        rv = self.app.post('/delete', data=dict(
            title='<Hello>'
        ), follow_redirects=True)
        assert b'&lt;Hello&gt;' not in rv.data

if __name__ == '__main__':
    unittest.main()