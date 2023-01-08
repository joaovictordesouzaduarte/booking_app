from db.database import client


def creating_user_collection_and_schema_validator():
    
    user_validator = {
        "$jsonSchema": {
            'bsonType': 'object',
             'required': ['username', 'email', 'password'],
             'properties': {
                'username': {
                    'bsonType': 'string',
                    'description': 'must be a string and required',
                    
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'password': {
                    'bsonType': 'string',
                    'description': 'must be a string and required'
                },
                'is_admin': {
                    'bsonType': 'bool'
                }
             }
        }
    }

    db = client.booking
    result = db.create_collection('user', validator=user_validator )
    return print('Collection created')

creating_user_collection_and_schema_validator()
