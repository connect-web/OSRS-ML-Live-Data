from database.base.old_database import Connection
def get_hiscore_rows(activity, limit=500, offset=0, activity_type='skills'):
    """
    returns a tuple of:
    pid, duration, Banned, skills, minigames, agg_skills, agg_minigames
    """
    db = Connection(localhost=True)
    query = f'''
            SELECT 
                agg.pid,
                duration,
                CASE WHEN nf.pid IS NULL THEN FALSE ELSE TRUE END as Banned,
                pl.skills as live_skills_experience,  
                plr.skills as live_skills_ratio, 
                pl.minigames as live_minigames_score, 
                agg.skills as aggregated_skills_experience, 
                agg.minigames as aggregated_minigames_score
            FROM TASKS.aggregates agg
            LEFT JOIN player_live pl on pl.pid = agg.pid
            LEFT JOIN not_found nf on nf.pid = agg.pid
            LEFT JOIN player_live_ratio plr on plr.pid = agg.pid
            WHERE agg.HASNEGATIVE IS FALSE 
            AND (agg.{activity_type} ->> %s)::numeric IS NOT NULL
            ORDER BY (agg.{activity_type} ->> %s)::numeric DESC
            LIMIT %s OFFSET %s
            '''

    rows = db.get(query, (activity, activity, limit, offset))
    db.close()
    return rows