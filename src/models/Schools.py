from enum import Enum

from src.models.Emojis import Emojis

COLLEGES_TO_RUN = {
    'fsu': 'fsu',
    'florida state': 'fsu',
    'florida state university': 'fsu',
    'michigan': 'michigan'
}


class Schools(Enum):
    fsu = {
       'baseball': {
           'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} @FSUBaseball {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n'
       },
       'basketball': {
           'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} @FSUHoops {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
       }
    }
    michigan = {
        'baseball': {
            'header': f'{Emojis.BASEBALL.value} @umichbaseball {Emojis.BASEBALL.value}\n'
        },
        'basketball': {
            'header': f'{Emojis.BASKETBALL.value} @umichbball {Emojis.BASKETBALL.value}\n'
        }
    }
    notredame = {
        'baseball': {
            'header': f'{Emojis.BASEBALL.value} Notre Dame {Emojis.BASEBALL.value}\n'
        },
        'basketball': {
            'header': f'{Emojis.BASKETBALL.value} Notre Dame {Emojis.BASKETBALL.value}\n'
        }
    }
    illinois = {
        'baseball': {
            'header': f'{Emojis.BASEBALL.value} Illinois {Emojis.BASEBALL.value}\n'
        },
        'basketball': {
            'header': f'{Emojis.BASKETBALL.value} Illinois {Emojis.BASKETBALL.value}\n'
        }
    }
    connecticut = {
        'baseball': {
            'header': f'{Emojis.BASEBALL.value} UConn {Emojis.BASEBALL.value}\n'
        },
        'basketball': {
            'header': f'{Emojis.BASKETBALL.value} UConn {Emojis.BASKETBALL.value}\n'
        }
    }