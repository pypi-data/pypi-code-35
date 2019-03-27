"""
    Edenchain configuration related
"""
import os

class EdenConfig:
    def __init__(self):
        self.apis=[
            {
            },
            {
                'api_key': 'AIzaSyCxBr_r3Q7d2letGIezVoO0cah0TtdZSeA',
                'api_end_point': 'https://api-ep-br.edenchain.io/api'
            }
        ]


    def getConfig(self, network):
        if len(self.apis) <= network or network < 0:
            return False,{}
            
        return True, self.apis[network] 
