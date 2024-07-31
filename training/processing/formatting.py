from entities.leaderboards import skill_to_array, minigame_to_array

ROW_COLUMNS = [
    'Banned',
    'live_skills_experience',
    'live_skills_ratio',
    'live_minigames_score',
    'daily_skills_experience',
    'daily_minigames_score'
]

def format_row(row):
    """
    Converts the Skill, Minigame columns from Dict to Array
    """
    skill_indexes = [3,4,6]
    minigame_indexes = [5,7]
    for i in skill_indexes:
        row[i] = skill_to_array(row[i])
    for i in minigame_indexes:
        row[i] = minigame_to_array(row[i])

    # dropping pid, duration
    return row[2:]
