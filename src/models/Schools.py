from enum import Enum

from src.models.Emojis import Emojis

COLLEGES_TO_RUN = {
    'arizona state': 'azst',
    'connecticut': 'connecticut',
    'duke': 'duke',
    'florida': 'florida',
    'fsu': 'fsu',
    'florida state': 'fsu',
    'florida state university': 'fsu',
    'georgia': 'georgia',
    'illinois': 'illinois',
    'kansas': 'kansas',
    'lsu': 'lsu',
    'louisiana state': 'lsu',
    'miami': 'miami',
    'michigan': 'michigan',
    'ohio state': 'ohiostate',
    'north carolina': 'northcarolina',
    'notre dame': 'notredame',
    'texas': 'texas',
    'texas-austin': 'texas',
    'virginia': 'virginia',
    'wisconsin': 'wisconsin'
}


class Schools(Enum):
    azst = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} ASU {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} ASU {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} ASU {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} ASU {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} ASU {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} ASU {Emojis.HOCKEY.value}\n'
            }
        }
    }
    connecticut = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} UConn {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} UConn {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} UConn {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} UConn {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} UConn {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} UConn {Emojis.HOCKEY.value}\n'
            }
        }
    }
    duke = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Duke {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Duke {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Duke {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Duke {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Duke {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Duke {Emojis.HOCKEY.value}\n'
            }
        }
    }
    florida = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Florida {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Florida {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Florida {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Florida {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Florida {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Florida {Emojis.HOCKEY.value}\n'
            }
        }
    }
    fsu = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} FSU {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} FSU {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} FSU {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} FSU {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} FSU {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} FSU {Emojis.HOCKEY.value}\n'
            }
        }
    }
    georgia = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Georgia {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Georgia {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Georgia {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Georgia {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Georgia {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Georgia {Emojis.HOCKEY.value}\n'
            }
        }
    }
    illinois = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Illinois {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Illinois {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Illinois {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Illinois {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Illinois {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Illinois {Emojis.HOCKEY.value}\n'
            }
        }
    }
    kansas = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Kansas {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Kansas {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Kansas {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Kansas {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Kansas {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Kansas {Emojis.HOCKEY.value}\n'
            }
        }
    }
    lsu = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} LSU {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} LSU {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} LSU {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} LSU {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} LSU {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} LSU {Emojis.HOCKEY.value}\n'
            }
        }
    }
    miami = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Miami {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Miami {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Miami {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Miami {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Miami {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Miami {Emojis.HOCKEY.value}\n'
            }
        }
    }
    michigan = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Michigan {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Michigan {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Michigan {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Michigan {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Michigan {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Michigan {Emojis.HOCKEY.value}\n'
            }
        }
    }
    northcarolina = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} UNC {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} UNC {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} UNC {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} UNC {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} UNC {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} UNC {Emojis.HOCKEY.value}\n'
            }
        }
    }
    notredame = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Notre Dame {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Notre Dame {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Notre Dame {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Notre Dame {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Notre Dame {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Notre Dame {Emojis.HOCKEY.value}\n'
            }
        }
    }
    ohiostate = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Ohio State {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Ohio State {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Ohio State {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Ohio State {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Ohio State {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Ohio State {Emojis.HOCKEY.value}\n'
            }
        }
    }
    texas = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Texas {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Texas {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Texas {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Texas {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Texas {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Texas {Emojis.HOCKEY.value}\n'
            }
        }
    }
    virginia = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Virginia {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Virginia {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Virginia {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Virginia {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Virginia {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Virginia {Emojis.HOCKEY.value}\n'
            }
        }
    }
    wisconsin = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} Wisconsin {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} Wisconsin {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} Wisconsin {Emojis.BASKETBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} Wisconsin {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} Wisconsin {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} Wisconsin {Emojis.HOCKEY.value}\n'
            }
        }
    }
