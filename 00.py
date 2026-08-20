person_here = True
is_dark = False
def hallway_light(person: bool, dark: bool) -> bool:
    """복도 조명의 판단 규칙: 사람이 있고 어두울때만 켜진다."""
    return person and dark