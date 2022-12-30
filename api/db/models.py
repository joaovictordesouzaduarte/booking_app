from database import client


def creating_collection_and_schema_validator():
    
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
                    'description': 'must be a string and required'
                },
                'room': {
                    'bsonType': ['int'],
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

    db = client.booking
    result = db.create_collection('hotels', validator=hotels_validator )
    return print('Collection created')

creating_collection_and_schema_validator()