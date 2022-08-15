from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_users_23-1_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserPostTestCase(TestCase):
    """Tests for routes of blogly app."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        Post.query.delete()
        Tag.query.delete()
        PostTag.query.delete()

        user = User(first_name="Test", last_name="Name")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="Test Post", content="Test post content",
                    created_at="08/09/22 02:35:5.523", users_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

        tag = Tag(name="Testag")
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

        post_tag = PostTag(post_id=post.id,
                           tag_id=tag.id)
        db.session.add(post_tag)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_homepage(self):
        """Testing for the root route to display posts"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)

    def test_show_user(self):
        """Testing for the users image and buttons to display as long as id is correct"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Name</h1>', html)
            self.assertIn(' <button class="edit">Edit</button>', html)

    def test_edit_user_get_request(self):
        """Testing for the edit form to display"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)
            self.assertIn('<input type="text" name="image_url" />', html)
            self.assertIn('<button class="cancel">Cancel</button>', html)

    def test_edit_user_post_request(self):
        """Testing for the post request to edit a user and change the data in our database"""

        data = {'first_name': 'New', 'last_name': 'Name',
                'image_url': 'https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg'}

        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>New Name</h1>', html)
            self.assertIn(' <button class="edit">Edit</button>', html)

    def test_create_user_get_request(self):
        """Testing for the create user form to display"""
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)
            self.assertIn('<form action="/users/new" method="POST">', html)
            self.assertIn('<button class="cancel">Cancel</button>', html)

    def test_create_user_post_request(self):
        """Testing for the create user post request to insert a new user into our database and update the user's listdisplayed"""

        data = {'first_name': 'Second', 'last_name': 'User',
                'image_url': 'https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg'}

        with app.test_client() as client:
            resp = client.post(f"/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('Second User', html)
            self.assertIn('Add user', html)

    def test_create_post_get_request(self):
        """Testing for the create post form to     display"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add post for Test Name',     html)
            self.assertIn(
                f'<form action="/users/{self.user_id}/posts/new" method="POST">', html)
            self.assertIn('<button class="cancel">Cancel</button>', html)

    def test_create_post_post_request(self):
        """Testing for the create post POST request to insert a new post into our database and update the user's  posts list displayed"""

        data = {'title': 'Second Post', 'content': 'Second test post'}

        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Name</h1>', html)
            self.assertIn('Test Post', html)
            self.assertIn('Second Post', html)

    def test_view_post(self):
        """Testing for a specific post to be displayed"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post',     html)
            self.assertIn(
                'Return', html)
            self.assertIn('Test post content', html)
            self.assertIn('Posted by Test Name on', html)
            self.assertIn(' 08-09-22 02:05 AM', html)

    def test_view_tag_list(self):
        """Testing for tag list to be displayed"""
        with app.test_client() as client:
            resp = client.get(f"/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testag',     html)
            self.assertIn(
                'Create tag', html)
            self.assertIn('Tags', html)

    def test_view_tag(self):
        """Testing for a specific tag to be displayed"""
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testag',     html)
            self.assertIn(
                'Edit', html)
            self.assertIn('Delete', html)

    def test_create_tag(self):
        """Testing for the create tag form to be displayed"""
        with app.test_client() as client:
            resp = client.get(f"/tags/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a new tag!',     html)
            self.assertIn('Name', html)
            self.assertIn('Save', html)

    def test_create_tag_post_request(self):
        """Testing for the create tag POST request to insert a new tag into our database and update the tag's list displayed (including previous data)"""

        data = {'name': 'Second Tag'}

        with app.test_client() as client:
            resp = client.post(
                f"/tags/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Second Tag', html)
            self.assertIn('Testag', html)

    def test_edit_tag(self):
        """Testing for the edit tag form to be displayed"""
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit "Testag"',     html)
            self.assertIn('Name', html)
            self.assertIn('Save', html)

    def test_edit_tag_post_request(self):
        """Testing for the edit tag POST request to modify a tag from  our database"""

        data = {'name': 'Changed Tag'}

        with app.test_client() as client:
            resp = client.post(
                f"/tags/{self.tag_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Changed Tag', html)
            self.assertIn('Edit', html)
