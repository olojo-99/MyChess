from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
import json

class MessageSocket(WebsocketConsumer):
    def connect(self):
        if self.scope['user'] == "AnonymousUser":
            self.close(code=401)
        else:
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
            self.accept()
            group = "game_{}".format(self.game_id)
            async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    # received from elsewhere in django and forward to enduser
    def broadcast_move(self, event):
        self.send(text_data=json.dumps(event))

    def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        # validate json iuput
        try:
            j = json.loads(text_data)
            to_square = Game.grid_ref(j['to'])
            from_square = Game.grid_ref(j['from'])
        except(json.decoder.JSONDecodeError, ValueError, KeyError):
            self.send(text_data=json.dumps({
                "type": "error_message",
                "message": "Bad request",
            }))
            return

        # game must exist
        game = Game.objects.filter(id=self.game_id).first()
        if not game:
            self.send(text_data=json.dumps({
                "type": "error_message",
                "message": "Game does not exist!"
            }))
            return

        # make move
        if not game.move_piece(self.scope['user'].id, from_square, to_square):
            self.send(text_data=json.dumps({
                "type": "error_message",
                "message": "Invalid move",
            }))
            return

        # notify other player
        group = "game_{}".format(self.game_id)
        async_to_sync(self.channel_layer.group_send) (group, {
            "type": "broadcast_move",
            "moving_player": self.scope['user'].id,
            "from": j['from'],
            "to": j['to']
        })

        # return success to this player
        self.send(text_data=json.dumps({
            "type": "ok",
            "moving_player": self.scope['user'].id,
            "to": j['to'],
            "from": j['from'],
        }))

    def disconnect(self, close_code):
        group = "game_{}".format(self.game_id)
        super().disconnect(close_code)
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
