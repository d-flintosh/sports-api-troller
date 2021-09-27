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
                'header': f'{Emojis.BASEBALL.value} #ForksUp {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #ForksUp {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #ForksUp {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #ForksUp {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #ForksUp {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #ForksUp {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #ForksUp {Emojis.HOCKEY.value}\n'
            }
        }
    }
    connecticut = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #BleedBlue #HookC #RollSkies {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #BleedBlue {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#ThisIsUConn\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #BleedBlue {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #BleedBlue {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #BleedBlue {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #BleedBlue {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #BleedBlue {Emojis.HOCKEY.value}\n'
            }
        }
    }
    duke = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoDuke {Emojis.BASEBALL.value}\n',
                'hashtag_header': '#BlueCollar\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoDuke {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#𝔗𝔥𝔢𝔅𝔯𝔬𝔱𝔥𝔢𝔯𝔥𝔬𝔬𝔡\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoDuke {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#𝕿𝖍𝖊𝕾𝖎𝖘𝖙𝖊𝖗𝖍𝖔𝖔𝖉\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoDuke {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#DukeGang\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoDuke {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoDuke {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoDuke {Emojis.HOCKEY.value}\n'
            }
        }
    }
    florida = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoGators {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoGators {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoGators {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoGators {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoGators {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoGators {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoGators {Emojis.HOCKEY.value}\n'
            }
        }
    }
    fsu = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} #GoNoles {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n',
                'hashtag_header': '#ProNoles\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} #GoNoles {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n',
                'hashtag_header': '#NewBlood #ProNoles\n'
            },
            'wnba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} #GoNoles {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n',
                'hashtag_header': '#ProNoles\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.FOOTBALL.value} #GoNoles {Emojis.FOOTBALL.value}{Emojis.FSU_SPEAR.value}\n',
                'hashtag_header': '#NoleFamily #ProNoles\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoNoles {Emojis.MAN_GOLFING.value}\n',
                'hashtag_header': '#ProNoles\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoNoles {Emojis.WOMAN_GOLFING.value}\n',
                'hashtag_header': '#ProNoles\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoNoles {Emojis.HOCKEY.value}\n'
            }
        }
    }
    georgia = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #CommitToTheG {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #CommitToTheG {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #CommitToTheG {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #CommitToTheG {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #CommitToTheG {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #CommitToTheG {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #CommitToTheG {Emojis.HOCKEY.value}\n'
            }
        }
    }
    illinois = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #Illini {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #Illini {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #Illini {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #Illini {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #Illini {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #Illini {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #Illini {Emojis.HOCKEY.value}\n'
            }
        }
    }
    kansas = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #RockChalk {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #RockChalk {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#PayHeed #KUbball\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #RockChalk {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#KUwbb\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #RockChalk {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#KUfball\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #RockChalk {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #RockChalk {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #RockChalk {Emojis.HOCKEY.value}\n'
            }
        }
    }
    lsu = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #LSU {Emojis.BASEBALL.value}\n',
                'hashtag_header': '#GeauxTigers\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #LSU {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#GeauxTigers #BootUp\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #LSU {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#GeauxTigers\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #LSU {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#GeauxTigers\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #LSU {Emojis.MAN_GOLFING.value}\n',
                'hashtag_header': '#GeauxTigers\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #LSU {Emojis.WOMAN_GOLFING.value}\n',
                'hashtag_header': '#GeauxTigers\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #LSU {Emojis.HOCKEY.value}\n',
                'hashtag_header': '#GeauxTigers\n'
            }
        }
    }
    miami = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #ItsAllAboutTheU {Emojis.BASEBALL.value}\n',
                'hashtag_header': '#ProCanes'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #ItsAllAboutTheU {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#ProCanes'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #ItsAllAboutTheU {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#ProCanes'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #ItsAllAboutTheU {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#ProCanes'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #ItsAllAboutTheU {Emojis.MAN_GOLFING.value}\n',
                'hashtag_header': '#ProCanes'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #ItsAllAboutTheU {Emojis.WOMAN_GOLFING.value}\n',
                'hashtag_header': '#ProCanes'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #ItsAllAboutTheU {Emojis.HOCKEY.value}\n',
                'hashtag_header': '#ProCanes'
            }
        }
    }
    michigan = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoBlue {Emojis.BASEBALL.value}\n',
                'hashtag_header': '#BlueCrew\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoBlue {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoBlue {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoBlue {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoBlue {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoBlue {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoBlue {Emojis.HOCKEY.value}\n'
            }
        }
    }
    northcarolina = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoHeels {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoHeels {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#CarolinaFamily\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoHeels {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#InPursuit\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoHeels {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#CarolinaFootball\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoHeels {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoHeels {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoHeels {Emojis.HOCKEY.value}\n'
            }
        }
    }
    notredame = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoIrish {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoIrish {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoIrish {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#IrishintheWNBA\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoIrish {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoIrish {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoIrish {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoIrish {Emojis.HOCKEY.value}\n'
            }
        }
    }
    ohiostate = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoBucks {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoBucks {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoBucks {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoBucks {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoBucks {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoBucks {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoBucks {Emojis.HOCKEY.value}\n'
            }
        }
    }
    texas = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #HookEm {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #HookEm {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #HookEm {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #HookEm {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#ThisIsTexas\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #HookEm {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #HookEm {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #HookEm {Emojis.HOCKEY.value}\n'
            }
        }
    }
    virginia = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoHoos {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoHoos {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoHoos {Emojis.BASKETBALL.value}\n',
                'hashtag_header': '#GoHoos\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoHoos {Emojis.FOOTBALL.value}\n',
                'hashtag_header': '#THEStandard\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoHoos {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoHoos {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoHoos {Emojis.HOCKEY.value}\n'
            }
        }
    }
    wisconsin = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #Badgers {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #Badgers {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #Badgers {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #Badgers {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #Badgers {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #Badgers {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #Badgers {Emojis.HOCKEY.value}\n'
            }
        }
    }
