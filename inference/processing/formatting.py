from entities.leaderboards import skill_to_array, minigame_to_array
from entities.data_process import flatten

def format_row(row):
    """
    Converts the Skill, Minigame columns from Dict to Array
    """
    row = filter_row(row)  # first remove overalls from skills
    skill_indexes = [1, 2, 4]
    minigame_indexes = [3, 5]
    for i in skill_indexes:
        row[i] = skill_to_array(row[i])
    for i in minigame_indexes:
        row[i] = minigame_to_array(row[i])

    row = flatten(row)
    return row

def filter_row(row):
    skill_indexes = [1, 2, 4]
    for index in skill_indexes:
        row[index] = remove_overall(row[index])
    return row

def remove_overall(skills: dict):
    return {skill: value for skill, value in skills.items() if skill != 'Overall'}
