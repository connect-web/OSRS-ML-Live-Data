from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
import mlflow

from config.settings import MLFLOW_TRACKING_URI
# Configure MLFlow to connect to your local server
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

class Experiment:
    N_JOBS=16
    user_limit = 1000
    classifiers = [
        ("RandomForest", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=N_JOBS)),
        ("ExtraTrees", ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=N_JOBS)),
        ("GradientBoosting", GradientBoostingClassifier(random_state=42)),  # Does not support n_jobs
        ("SVM", SVC(probability=True, random_state=42)),  # Does not support n_jobs
        ("LogisticRegression", LogisticRegression(random_state=42, n_jobs=N_JOBS)),
        ("LGBMClassifier", LGBMClassifier(random_state=42, n_jobs=N_JOBS)),
        ("XGBClassifier",
         XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42, n_jobs=N_JOBS))
    ]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    activities = []

    def create_experiments(self):
        for activity in self.activities:
            try:
                mlflow.set_experiment(activity)  # Set your experiment name
            except:
                print(f"Created {activity} experiment")