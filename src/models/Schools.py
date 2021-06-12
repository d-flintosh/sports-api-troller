from enum import Enum

from src.models.Emojis import Emojis

fsu_school_names = ['florida state', 'fsu', 'florida state university']
COLLEGES_TO_RUN = {
    'fsu': 'fsu',
    'florida state': 'fsu',
    'florida state university': 'fsu',
    'michigan': 'michigan',
    'notre dame': 'notredame'
}


class Schools(Enum):
    fsu = {
       'baseball': {
           'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} @FSUBaseball {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n'
       }
    }
    michigan = {
        'baseball': {
            'header': f'{Emojis.BASEBALL.value} Michigan {Emojis.BASEBALL.value}\n'
        }
    }
    notredame = {
        'baseball': {
            'header': f'{Emojis.BASEBALL.value} Notre Dame {Emojis.BASEBALL.value}\n'
        }
    }