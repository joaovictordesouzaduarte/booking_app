from db import get_db

def creating_user_collection_and_schema_validator():
    
    hotels_validator = {
        "$jsonSchema": {
            'bsonType': 'object',
             'required': ['name', 'type', 'city', 'address', 'distance', 
                            'photos', 'title', 'desc', 'rating',
                            'rooms', 'cheapestPrice', 'featured'],
             'properties': {
                'name': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'type': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'address': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'distance': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'photos': {
                    'bsonType': ['string'],
                    'description': 'must be a list and required'
                },
                'title': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'desc': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'rating': {
                    'bsonType': 'int',
                    'minimum': 0,
                    'maximum': 5,
                    'description': 'must be a integer and required'
                },
                'rooms': {
                'bsonType': 'array',
                'items': {
                    'bsonType': 'string'
                },
                
                },
                'cheapestPrice': {
                    'bsonType': 'number'
                },
                'featured': {
                    'bsonType': 'bool'
                }
             }
        }
    }

    db = get_db.booking
    result = db.create_collection('hotels', validator=hotels_validator )
    return print('Collection created')

creating_user_collection_and_schema_validator()