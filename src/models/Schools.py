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
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} ASU {Emojis.FOOTBALL.value}\n'
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
                'header': f'{Emojis.BASEBALL.value} #BleedBlue #HookC #RollSkies {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #BleedBlue #ThisIsUConn {Emojis.BASKETBALL.value}\n'
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
                'header': f'{Emojis.BASEBALL.value} #BlueCollar #GoDuke {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #GoDuke #𝔗𝔥𝔢𝔅𝔯𝔬𝔱𝔥𝔢𝔯𝔥𝔬𝔬𝔡 {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoDuke #𝕿𝖍𝖊𝕾𝖎𝖘𝖙𝖊𝖗𝖍𝖔𝖔𝖉 {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoDuke #DukeGang {Emojis.FOOTBALL.value}\n'
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
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} #GoNoles #ProNoles {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} #GoNoles #NewBlood #ProNoles {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.BASKETBALL.value} #GoNoles #ProNoles {Emojis.BASKETBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FSU_SPEAR.value}{Emojis.FOOTBALL.value} #GoNoles #NoleFamily #ProNoles {Emojis.FOOTBALL.value}{Emojis.FSU_SPEAR.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #GoNoles #ProNoles {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #GoNoles #ProNoles {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #GoNoles #ProNoles {Emojis.HOCKEY.value}\n'
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
                'header': f'{Emojis.BASKETBALL.value} #RockChalk #PayHeed #KUbball {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #RockChalk #KUwbb {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value}  #KUfball #RockChalk {Emojis.FOOTBALL.value}\n'
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
                'header': f'{Emojis.BASEBALL.value} #LSU #GeauxTigers {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #LSU #GeauxTigers #BootUp {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #LSU #GeauxTigers {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #LSU #GeauxTigers {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #LSU #GeauxTigers {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #LSU #GeauxTigers {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #LSU #GeauxTigers {Emojis.HOCKEY.value}\n'
            }
        }
    }
    miami = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #ItsAllAboutTheU #ProCanes {Emojis.BASEBALL.value}\n'
            }
        },
        'basketball': {
            'nba': {
                'header': f'{Emojis.BASKETBALL.value} #ItsAllAboutTheU #ProCanes {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #ItsAllAboutTheU #ProCanes {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #ItsAllAboutTheU #ProCanes {Emojis.FOOTBALL.value}\n'
            }
        },
        'golf': {
            'pga': {
                'header': f'{Emojis.MAN_GOLFING.value} #ItsAllAboutTheU #ProCanes {Emojis.MAN_GOLFING.value}\n'
            },
            'lpga': {
                'header': f'{Emojis.WOMAN_GOLFING.value} #ItsAllAboutTheU #ProCanes {Emojis.WOMAN_GOLFING.value}\n'
            }
        },
        'hockey': {
            'nhl': {
                'header': f'{Emojis.HOCKEY.value} #ItsAllAboutTheU #ProCanes {Emojis.HOCKEY.value}\n'
            }
        }
    }
    michigan = {
        'baseball': {
            'mlb': {
                'header': f'{Emojis.BASEBALL.value} #GoBlue #BlueCrew {Emojis.BASEBALL.value}\n'
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
                'header': f'{Emojis.BASKETBALL.value} #GoHeels #CarolinaFamily {Emojis.BASKETBALL.value}\n'
            },
            'wnba': {
                'header': f'{Emojis.BASKETBALL.value} #GoHeels #InPursuit {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #GoHeels #CarolinaFootball {Emojis.FOOTBALL.value}\n'
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
                'header': f'{Emojis.BASKETBALL.value} #GoIrish #IrishintheWNBA {Emojis.BASKETBALL.value}\n'
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
                'header': f'{Emojis.FOOTBALL.value} #ThisIsTexas #HookEm {Emojis.FOOTBALL.value}\n'
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
                'header': f'{Emojis.BASKETBALL.value} #GoHoos #WeCavaliers {Emojis.BASKETBALL.value}\n'
            }
        },
        'football': {
            'nfl': {
                'header': f'{Emojis.FOOTBALL.value} #THEStandard #GoHoos {Emojis.FOOTBALL.value}\n'
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
