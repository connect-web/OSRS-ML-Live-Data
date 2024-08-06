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
            results = inference(activity=activity, activity_type=activity_type)
            if results is not None:
                print(f'Predicted {len(results)} players for {activity}.')
                db.submit_results(results, activity, activity_type)

    db.close()


if __name__ == '__main__':
    run_inference()
