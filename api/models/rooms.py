from db.database import client


def creating_user_collection_and_schema_validator():
    
    room_validator = {
        "$jsonSchema": {
            'bsonType': 'object',
             'required': ['title', 'price', 'max_people', 'desc', 'room_number'],
             'properties': {
                'title': {
                    'bsonType': 'string',
                    'description': 'must be a string and required',
                    
                },
                'price': {
                    'bsonType': 'number',
                    'description': 'must be a number and required'
                },
                'max_people': {
                    'bsonType': 'number',
                    'description': 'must be a string and required'
                },
                'desc': {
                    'bsonType': 'string',
                    'description': 'must be a string and required',
                    
                },
                'room_numbers': {
                    'bsonType': [
                        "object"
                    ]
                }
             }
        }
    }

    db = client.booking
    result = db.create_collection('room', validator=room_validator )
    return print('Collection created')

creating_user_collection_and_schema_validator()
