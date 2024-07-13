# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class PianoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        note = json.loads(text_data)['note']
