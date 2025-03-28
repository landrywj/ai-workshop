import os
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, Response
from models import init_db, db, Dog, Breed, Cat

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "dogshelter.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
init_db(app)

@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    query = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed')
    ).join(Breed, Dog.breed_id == Breed.id)
    
    dogs_query = query.all()
    
    # Convert the result to a list of dictionaries
    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed
        }
        for dog in dogs_query
    ]
    
    return jsonify(dogs_list)

@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> tuple[Response, int] | Response:
    # Query the specific dog by ID and join with breed to get breed name
    dog_query = db.session.query(
        Dog.id,
        Dog.name,
        Breed.name.label('breed'),
        Dog.age,
        Dog.description,
        Dog.gender,
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    # Return 404 if dog not found
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name
    }
    
    return jsonify(dog)

@app.route('/api/cats/<int:id>', methods=['GET'])
def get_cat(id: int) -> tuple[Response, int] | Response:
    # Query the specific cat by ID
    cat_query = db.session.query(
        Cat.id,
        Cat.name,
        Cat.age,
        Cat.description,
        Cat.gender,
        Cat.status
    ).filter(Cat.id == id).first()
    
    # Return 404 if cat not found
    if not cat_query:
        return jsonify({"error": "Cat not found"}), 404
    
    # Convert the result to a dictionary
    cat: Dict[str, Any] = {
        'id': cat_query.id,
        'name': cat_query.name,
        'age': cat_query.age,
        'description': cat_query.description,
        'gender': cat_query.gender,
        'status': cat_query.status.name
    }
    
    return jsonify(cat)

if __name__ == '__main__':
    app.run(debug=True, port=5100) # Port 5100 to avoid macOS conflicts