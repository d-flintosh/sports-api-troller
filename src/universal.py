
def is_fsu(school: str):
    _fsu = ['florida state', 'fsu', 'florida state university']

    if school and school and any(list(map(lambda x: x == school.lower(), _fsu))):
        return True
    return False
