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
            gains.minigames as daily_minigames_score,
            p.id,
            gains.last_updated - pl.last_updated as duration,
            case when results.playerid is not null then true else false end as Computed
        FROM player_gains gains
        LEFT JOIN player_live pl on pl.playerid = gains.playerid
        LEFT JOIN not_found nf on nf.playerid = gains.playerid
        LEFT JOIN players p on p.id = gains.playerid
        LEFT JOIN ml.results results on results.playerid = gains.playerid and results.activity = %s and results.duration = gains.last_updated - pl.last_updated
        
        WHERE 
            nf.playerid IS NULL 
            AND (gains.{activity_type} ->> %s)::numeric IS NOT NULL
            
        ORDER BY (gains.{activity_type} ->> %s)::numeric DESC
        LIMIT %s OFFSET %s
            '''
    rows = db.get(query, (activity, activity,activity, limit, offset))
    db.close()
    return rows