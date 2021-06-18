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
                'header': f'{Emojis.BASEBALL.value} @ASU_Baseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @SunDevilHoops {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @SunDevilWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    connecticut = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @UConnBSB {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @UConnMBB {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @UConnWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    duke = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @DukeBASE {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @DukeMBB {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @DukeWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    florida = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @GatorsBB {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @GatorsMBK {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @GatorsWBK {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    fsu = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} @FSUBaseball {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} @FSUHoops {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} @fsuwbb {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        }
    }
    georgia = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @BaseballUGA {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @UGABasketball {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @UGA_WBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    illinois = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @IlliniBaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @IlliniMBB {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @IlliniWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    kansas = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @KUBaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @KUHoops {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @KUWBball {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    lsu = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @LSUbaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @LSUBasketball {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @LSUwbkb {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    miami = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @CanesBaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @CanesHoops {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @CanesWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    michigan = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @umichbaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @umichbball {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @umichwbball {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    northcarolina = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @DiamondHeels {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @UNC_Basketball {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @uncwbb {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    notredame = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @NDBaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @NDmbb {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @ndwbb {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    ohiostate = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @OhioStateBASE {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @OhioStateHoops {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @OhioStateWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    texas = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @TexasBaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @TexasMBB {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @TexasWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
    virginia = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} @UVABaseball {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} @UVAMensHoops {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @UVAWomensHoops {Emojis.BASKETBALL.value}\n'
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
                'header': f'{Emojis.BASKETBALL.value} @BadgerMBB {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} @BadgerWBB {Emojis.BASKETBALL.value}\n'
            }
        }
    }
