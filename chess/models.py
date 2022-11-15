from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.
class APIUser(AbstractUser):
    id = models.AutoField(primary_key=True)

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    white = models.ForeignKey(APIUser, related_name='black', on_delete=models.CASCADE)
    black = models.ForeignKey(APIUser, related_name='white', on_delete=models.CASCADE)
    challenge_accepted = models.BooleanField(default=False)
    GAME_RESULT = {
        'C': 'Current',
        'S': 'Stalemate',
        'W': 'White won',
        'B': 'Black won',
    }
    status = models.CharField(max_length=1, choices=GAME_RESULT.items(), default='C')
    board = models.CharField(max_length=64, null=False,
        default='cnbqkbncppppppppssssssssssssssssssssssssssssssssPPPPPPPPCNBQKBNC')
    
    TURNS = {
        'W': 'white',
        'B': 'black',
    }
    turn = models.CharField(max_length=1, choices=TURNS.items(), default='W')

    def get_next_turn(self):
        return self.TURNS[self.turn]

    def get_opponant_id(self, user_id):
        if user_id == self.white.id:
            return self.black.id
        elif user_id == self.black.id:
            return self.white.id
        else:
            return None

    # convert a1 to 0 and h8 to 63
    @staticmethod
    def grid_ref(s):
        if re.match('^[a-h][1-8]$', s):
            return (ord(s[0]) - 97) + (ord(s[1]) - 49) * 8
        else:
            raise ValueError

    def move_piece(self, user_id, from_square, to_square):
        board = list(self.board)

        # it must be this user's turn
        if user_id == self.white.id and self.turn == 'B':
            return False
        elif user_id == self.black.id and self.turn == 'W':
            return False

        # it must be that player's piece
        if board[from_square] == 's':
            # can't move a space
            return False
        elif board[from_square].isupper() and self.turn == 'W':
            # a black piece can't be moved by white
            return False
        elif board[from_square].islower() and self.turn == 'B':
            # a white piece can't be moved by black
            return False

        # perform the move
        board[to_square] = board[from_square]
        board[from_square] = 's'
        self.board = "".join(board)

        if self.turn == 'W':
            self.turn = 'B'
        else:
            self.turn = 'W'

        self.save()
        return True
