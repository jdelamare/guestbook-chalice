from datetime import date
from .Model import Model
import boto3
import json
from datetime import datetime

# modeled my model after the example, resource is passed in as a parameter, 
class model(Model):
    def __init__(self, table_resource):
        self._table = table_resource

    def select(self):
        try: 
            ddb_entries = self._table.scan()
            ddb_entries = ddb_entries['Items'] # items contains a list of dictionaries representing each item
            print("ddb_entries: ", ddb_entries)
            # TODO: strange case when list is empty
            # hacky, but the string is just '[]', 
#            if len(ddb_entries) == 2: =
#                return []
            return ddb_entries

        except Exception as ex:
            print("There's been an error, need to fix this:\n", ex)
            return {
                'statusCode': 500,
                'headers': {
                    "Access-Control-Allow-Origin": "*"
                },
                'body': "It's not you, it's us. :("
            }

    def insert(self, name, email, message):
        if name is None or email is None or message is None:
            return {
                'statusCode': 400,
                'headers': {
                    "Access-Control-Allow-Origin": "*"
                },
                'body': "Missing parameters"
            }
        try:  
            self._table.put_item(
                Item={
                    'name': name,
                    'email': email,
                    'date': str(datetime.today()),
                    'message': message
                }
            )
            return None
        except Exception as ex:
            print("There's been an error, need to fix this")
            print(ex)
            return {
                'statusCode': 500,
                'headers': {
                    "Access-Control-Allow-Origin": "*"
                },
                'body': "It's not you, it's us. :("
            }
