from datetime import date
from .Model import Model
import boto3
import json


# modeled my model after the example, resource is passed in as a parameter, 
class model(Model):
    def __init__(self, table_resource):
        self._table = table_resource

    def select(self):
        try: 
            ddb_entries = self._table.scan()
            print("in model: ", end='')
            print(ddb_entries)
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': "*" # gross
                },
                'body': json.dumps(ddb_entries['Items'])
            }
        except Exception as ex:
            print(ex)
            return {
                'statusCode': 500,
                'headers': {
                    "Access-Control-Allow-Origin": "*"
                },
                'body': "It's not you, it's us. :("
            }


    def insert(self, name, email, message):
        params = [name, email, date.today(), message]
        self.guestentries.append(params)
        return True
