from .models import MODELS_BY_NAME
from .experiments import get_experiment_metrics

from database.metrics_database import MetricsDatabase

from entities.leaderboards import Leaderboards

def get_all_metrics():
    activities = {
        'skills': Leaderboards.get_skill_names(),
        'minigames': Leaderboards.get_minigame_names()
    }

    model_metrics = {}

    for activity_type, activities in activities.items():
        for activity in activities:
            model_name = f'prod.{activity}'
            try:
                model_version = MODELS_BY_NAME.get(model_name)
                metrics = get_experiment_metrics(model_version.run_id)
            except:
                print(f'Model with name {model_name} not found.')
                continue

            print(f'Metrics: {metrics}')
            model_metrics[activity] = metrics
    return model_metrics


def update_metrics(frontend=True):
    db = MetricsDatabase(frontend=frontend)
    db.submit_metric_dict(get_all_metrics())
    db.close()


def update_metrics_front_and_backend():
    update_metrics(frontend=True)
    update_metrics(frontend=False)