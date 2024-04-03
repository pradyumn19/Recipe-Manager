import pytest
from app import app, db
from app.model import User, Recipe


uusername = 'aadminaa'
upassword = 'abc12361'


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database tables
            yield client
            db.session.remove()  # Clean up the session after each test
            db.drop_all()  # Drop all tables after each test


def test_register(test_client):
    # Register a new user
    response = test_client.post('/register', json={'username': uusername, 'password': upassword})
    assert response.status_code == 201

    # Try to register with an existing username
    response = test_client.post('/register', json={'username': 'admina', 'password': 'abc12345'})
    assert response.status_code == 400


def test_login(test_client):
    # Create a test user
    test_user = User(username='uusername', password='mno123')
    db.session.add(test_user)
    db.session.commit()

    # Try to login with correct credentials
    response = test_client.post('/login', json={'username': uusername, 'password': upassword})
    assert response.status_code == 200

    # Try to login with incorrect credentials
    response = test_client.post('/login', json={'username': uusername, 'password': 'xyz@123'})
    assert response.status_code == 401


def test_add_recipe(test_client):
    # Create a test user
    test_user = User(username=uusername, password=upassword)
    db.session.add(test_user)
    db.session.commit()

    # Login with the test user
    test_client.post('/login', json={'username': uusername, 'password': upassword})

    # Add a recipe
    response = test_client.post('/recipe/add', json={
        'title': 'Test Recipe',
        'description': 'This is a test recipe',
        'ingredients': 'Test ingredient 1, Test ingredient 2',
        'instructions': 'Test instructions'
    })
    assert response.status_code == 201


def test_view_recipe(test_client):
    # Create a test user
    test_user = User(username=uusername, password=upassword)
    db.session.add(test_user)
    db.session.commit()

    # Create a test recipe
    test_recipe = Recipe(title='Test Recipe', description='This is a test recipe', ingredients='Test ingredient 1, Test ingredient 2', instructions='Test instructions', user_id=test_user.id)
    db.session.add(test_recipe)
    db.session.commit()

    # View the test recipe
    response = test_client.get(f'/recipe/{test_recipe.id}')
    assert response.status_code == 200

    # Check if the recipe details are correct
    data = response.get_json()
    assert data['title'] == 'Test Recipe'
    assert data['description'] == 'This is a test recipe'


def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_edit_recipe(test_client):
    # Create a test user
    test_user = User(username=uusername, password=upassword)
    db.session.add(test_user)
    db.session.commit()

    # Login with the test user
    test_client.post('/login', json={'username': uusername, 'password': upassword})

    # Create a test recipe
    test_recipe = Recipe(title='Test Recipe', description='This is a test recipe', ingredients='Test ingredient 1, Test ingredient 2', instructions='Test instructions', user_id=test_user.id)
    db.session.add(test_recipe)
    db.session.commit()

    # Edit the test recipe
    response = test_client.put(f'/recipe/edit/{test_recipe.id}', json={'title': 'Updated Recipe', 'description': 'Updated description', 'ingredients': 'Updated ingredients', 'instructions': 'Updated instructions'})
    assert response.status_code == 200


def test_logout(test_client):
    # Create a test user
    test_user = User(username=uusername, password=upassword)
    db.session.add(test_user)
    db.session.commit()

    # Login with the test user
    test_client.post('/login', json={'username': uusername, 'password': upassword})

    # Logout the user
    response = test_client.post('/logout')
    assert response.status_code == 200


def test_delete_recipe(test_client):
    # Create a test user
    test_user = User(username=uusername, password=upassword)
    db.session.add(test_user)
    db.session.commit()

    # Login with the test user
    test_client.post('/login', json={'username': uusername, 'password': upassword})

    # Create a test recipe
    test_recipe = Recipe(title='Test Recipe', description='This is a test recipe', ingredients='Test ingredient 1, Test ingredient 2', instructions='Test instructions', user_id=test_user.id)
    db.session.add(test_recipe)
    db.session.commit()

    # Delete the test recipe
    response = test_client.delete(f'/recipe/delete/{test_recipe.id}')
    assert response.status_code == 200
