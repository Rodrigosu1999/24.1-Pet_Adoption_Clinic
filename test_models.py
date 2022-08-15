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


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_get_full_name(self):
        """Testing for 'full_name' function"""
        user = User(first_name="Test", last_name="Name")
        self.assertEquals(user.get_full_name(), "Test Name")

    def test_default_profile_image(self):
        """Testing if the default image url is set when the user is committed to the database"""
        user = User(first_name="Test", last_name="Name")

        db.session.add(user)
        db.session.commit()

        test_user = User.query.filter(user.id == 1).all()

        self.assertEquals(
            test_user[0].image_url, "https://thumbs.dreamstime.com/b/default-profile-picture-avatar-photo-placeholder-vector-illustration-default-profile-picture-avatar-photo-placeholder-vector-189495158.jpg")

    def test_post_user_relationship(self):
        """Testing post-user relationship"""
        user = User(first_name="Test", last_name="Name")

        db.session.add(user)
        db.session.commit()

        post = Post(title="Test Title", content="Content test",
                    created_at="08/09/22 02:35:5.523", users_id=user.id)

        db.session.add(post)
        db.session.commit()

        self.assertEquals(user.first_name, post.user.first_name)

    def test_post_tag_relationship(self):
        """Testing post_tag relationship"""
        user = User(first_name="Test", last_name="Name")

        db.session.add(user)
        db.session.commit()

        post = Post(title="Test Title", content="Content test",
                    created_at="08/09/22 02:35:5.523", users_id=user.id)

        db.session.add(post)
        db.session.commit()

        tag = Tag(name="Testag")

        db.session.add(tag)
        db.session.commit()

        post_tag = PostTag(post_id=post.id, tag_id=tag.id)

        db.session.add(post_tag)
        db.session.commit()

        self.assertEquals(user.first_name, post.user.first_name)
        self.assertEquals(post.post_tag[0].tags, tag)
