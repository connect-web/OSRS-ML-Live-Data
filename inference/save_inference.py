from database import ResultsDatabase
from entities.leaderboards import Leaderboards
from .inference import inference

ACTIVITIES = {
    'skills': Leaderboards.get_skill_names(),
    'minigames': Leaderboards.get_minigame_names()
}


def run_inference():
    db = ResultsDatabase()

    for activity_type, activities in ACTIVITIES.items():
        for activity in activities:
            print(f'Running inference for {activity}...')
            usernames = inference(activity=activity, activity_type=activity_type)
            print(f'Predicted {len(usernames)} bans for {activity}.')
            if usernames:
                player_ids = db.usernamesToPlayerIds(usernames)
                db.submit_results(player_ids, activity, activity_type)

    db.close()


if __name__ == '__main__':
    run_inference()
