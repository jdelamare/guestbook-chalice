from datetime import date
from .Model import Model
#import boto3


class model(Model):
    def __init__(self):
        self.guestentries = []
        # self.resource = boto3.resource("dynamodb", region_name="us-east-1")
        # self.table = self.resource.Table('guestbook')
        # try:
        #     self.table.load()
        # except:
        #     self.resource.create_table(
        #         TableName="guestbook",
        #         KeySchema=[
        #             {   
        #                 "AttributeName": "email",
        #                 "KeyType": "HASH"
        #             },  
        #             {   
        #                 "AttributeName": "date",
        #                 "KeyType": "RANGE"
        #             }   
        #         ],  
        #         AttributeDefinitions=[
        #             {   
        #                 "AttributeName": "email",
        #                 "AttributeType": "S" 
        #             },  
        #             {   
        #                 "AttributeName": "date",
        #                 "AttributeType": "S"
        #             }
        #         ],
        #         ProvisionedThroughput={
        #             "ReadCapacityUnits": 1,
        #             "WriteCapacityUnits": 1
        #         }
        #     )

    def select(self):
        return self.guestentries

    def insert(self, name, email, message):
        params = [name, email, date.today(), message]
        print("here2")
        self.guestentries.append(params)
        return True