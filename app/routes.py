from flask import jsonify, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from .model import User, Recipe
from sqlalchemy import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'User is already logged in.'}), 200
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    login_user(user)
    return jsonify({'message': 'Logged in successfully'}), 200


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'message': 'User is already logged in.'}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists. Please choose a different one.'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Your account has been created. You can now log in.'}), 201


@app.route('/')
def index():
    recipes = Recipe.query.all()
    recipe_list = []
    for recipe in recipes:
        recipe_list.append({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_by': recipe.author.username
        })
    return jsonify({'recipes': recipe_list}), 200


@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe_json = {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'created_by': recipe.author.username
    }
    return jsonify(recipe_json), 200


@app.route('/recipe/<username>', methods=['GET'])
def view_recipe_by_username(username):
    # Perform a case-insensitive search for the provided username
    author = User.query.filter(func.lower(User.username) == username.lower()).first_or_404()

    # Get all recipes created by the user
    recipes = Recipe.query.filter_by(author=author).all()

    # Convert recipes to JSON format
    recipe_list = []
    for recipe in recipes:
        recipe_json = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_by': recipe.author.username
        }
        recipe_list.append(recipe_json)

    return jsonify(recipe_list), 200


@app.route('/recipe/add', methods=['POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        description = data.get('description')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')

        if current_user.is_authenticated:
            new_recipe = Recipe(title=title, description=description, ingredients=ingredients,
                                instructions=instructions,
                                user_id=current_user.id)
            db.session.add(new_recipe)
            db.session.commit()
            return jsonify({'message': 'Recipe added successfully'}), 201
        else:
            flash('Please log in before adding a recipe.', 'error')
            return jsonify({'message': 'Please log in before adding a recipe'}), 401
    else:
        # If the request method is not POST, return a 405 error
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/recipe/edit/<int:recipe_id>', methods=['PUT'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        return jsonify({'message': 'You are not authorized to edit this recipe'}), 403
    data = request.json
    recipe.title = data.get('title')
    recipe.description = data.get('description')
    recipe.ingredients = data.get('ingredients')
    recipe.instructions = data.get('instructions')
    db.session.commit()
    return jsonify({'message': 'Recipe updated successfully'}), 200


@app.route('/recipe/delete/<int:recipe_id>', methods=['DELETE'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        return jsonify({'message': 'You are not authorized to delete this recipe'}), 403
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully'}), 200
