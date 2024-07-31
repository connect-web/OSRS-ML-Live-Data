from database.base.server_connection import ServerConnection

def get_hiscore_rows(activity, limit=1000, offset=0, activity_type='skills'):
    """
    returns a tuple of:
    Name,
    live_skills_experience, live_skills_ratio, live_minigames_score,
    daily_skills_experience, daily_minigames_score
    """
    column_names = {
        'skills': 'skills_experience',
        'minigames': 'minigames'
    }
    activity_type = column_names.get(activity_type)
    if activity_type is None:
        print("activity type can only be 'skills' or 'minigames'")
        quit()

    db = ServerConnection()
    query = f'''
            SELECT
            p.name,
            pl.skills_experience as live_skills_experience,
            pl.skills_ratio as live_skills_ratio,
            pl.minigames as live_minigames_score,
            gains.skills_experience as daily_skills_experience,
            -- gains.skills_ratio as daily_skills_ratio, -- not used currently
            gains.minigames as daily_minigames_score
        FROM player_gains gains
        LEFT JOIN player_live pl on pl.playerid = gains.playerid
        LEFT JOIN not_found nf on nf.playerid = gains.playerid
        LEFT JOIN players p on p.id = gains.playerid
        WHERE 
            nf.playerid IS NULL 
        and (gains.{activity_type} ->> %s)::numeric IS NOT NULL
        ORDER BY (gains.{activity_type} ->> %s)::numeric DESC
        LIMIT %s OFFSET %s
            '''
    rows = db.get(query, (activity, activity, limit, offset))
    db.close()
    return rows