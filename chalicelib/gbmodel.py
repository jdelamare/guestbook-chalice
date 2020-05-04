from datetime import date
from .Model import Model
import boto3
import json
from datetime import datetime

class model(Model):
    """ Represent the model as DynamoDB table.

    Attributes:
        _table: A handle to the DynamoDB table, documentation exists at Boto 3
    """
    def __init__(self, table_resource):
        self._table = table_resource

    def select(self):
        """ Retrieves all of the entries from the table.
        
        Returns:
            ddb_entries['Items']: A list of dictionaries, each dictionary represents an item. 
            String literal: If this is sent then there's been an error.

        Raises:
            A generic exception, prints to STDOUT and returns the string.
        """
        try: 
            ddb_entries = self._table.scan()

            # Items contains a list of dictionaries representing each item
            return ddb_entries['Items'] 

        except Exception as ex:
            print("There's been an error, need to fix this:\n", ex)
            return "It's not you, it's us. :("

    def insert(self, name, email, message):
        """ Inserts the params into the database.
        Args: 
            name (String): A simple field in the table.
            email (String): A simple field in the table.
            message (String): A simple field in the table.

        Returns:
            None: If the insertion was successful.
            String literal: If the insertion failed, possibly due to lack of credentials.

        Raises:
            A generic exception, prints to STDOUT and returns the string.
        """
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
            print("There's been an error, need to fix this:\n", ex)
            return "It's not you, it's us. :("
