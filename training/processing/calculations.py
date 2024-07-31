SECONDS_IN_DAY = 86400

def daily_rate(row):
    row = list(row)
    days = row[1].total_seconds()/SECONDS_IN_DAY
    row[6], row[7] = divide_all(row[6], row[7], days)
    return row

def divide_all(skills: dict, minigames: dict, days: float):
    skills_divided = {skill: value/days for skill, value in skills.items()}
    minigames_divided = {minigame: value/days for minigame, value in minigames.items()}
    return skills_divided, minigames_divided

def remove_overall(skills: dict):
    return {skill: value for skill, value in skills.items() if skill != 'Overall'}
