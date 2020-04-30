from .Model import Model
from datetime import datetime
import boto3

class model(Model):
    def __init__(self, table_resource):
        # the table already exists, load it up from the environment variable
        self._table = table_resource

    def select(self):
        try:
            gbentries = self.table.scan()
        except Exception as e:
            return([['scan failed', '.', '.', '.']])

        return([ [f['name'], f['email'], f['date'], f['message']] for f in gbentries['Items']])

    def insert(self,name,email,message):
        gbitem = {
            'name' : name,
            'email' : email,
            'date' : str(datetime.today()),
            'message' : message
            }

        try:
            self.table.put_item(Item=gbitem)
        except:
            return False

        return True
