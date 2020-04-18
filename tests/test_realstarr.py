import unittest
import os
import json
from app import create_app, db

class RealstarrTestCase(unittest.TestCase):
    """This class represents the realstarr test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.post = {'name': 'Most talented footballer of all times'}

        # binds the app to the current context
        with self.app.app_context():
            #create all tables
            db.create_all()

    def test_post_creation(self):
        """Test API can create a post. (POST request)"""
        res = self.client().post('/posts/', data = self.post)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/posts/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Most talented footballer of all times', str(res.data))

    def test_api_can_get_all_posts(self):
        """Test API can get all post. (GET request)"""
        res = self.client().post('/posts/', data=self.post)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/posts/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Most talented footballer of all times', str(res.data))

    def test_api_can_get_post_by_id(self):
        """Test API can get a single post using it's id."""
        rv = self.client().post('/posts/', data=self.post)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/posts/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Most talented footballer of all times', str(result.data))

    def test_post_name_can_be_edited(self):
        """Test API can edit name of existing post. (PUT request)"""
        rv = self.client().post(
            '/posts/',
            data={'name': 'world of sports'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/posts/1',
            data = {
                'name': 'Trending in the world of sports'
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/posts/1')
        self.assertIn('Trending in the', str(results.data))

    # def test_post_message_can_be_edited(self):
    #     """Test API can edit message of existing post. (PUT request)"""
    #     rv = self.client().post(
    #         '/posts/',
    #         data={'message': 'Cristiano Ronaldo shines again after leading his team to a win'
    #         })
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put(
    #         '/posts/1',
    #         data = {
    #             'message': 'Most talented player Cristiano Ronaldo shines again after leading his team to a win'
    #         })
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get('/posts/1')
    #     self.assertIn('Most talented player', str(results.data))

    def test_post_deletion(self):
        """Test API can delete an existing post. (DELETE request)"""
        rv = self.client().post(
            '/posts/',
            data={'name': 'world of sports'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/posts/1')
        self.assertEqual(res.status_code, 200)
        #Test to see whether it exists, should return a 404
        result = self.client().get('/posts/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """Teardown all initialized variables."""
        with self.app.app_context():
            #drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()


