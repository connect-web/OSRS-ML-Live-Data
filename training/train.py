import os
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import recall_score, accuracy_score, confusion_matrix, roc_auc_score

from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline as ImblearnPipeline
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd

from .data_collection import get_hiscore
from .experiment import Experiment
from mlflow_methods.models import publish_best_experiments
from entities.leaderboards import Leaderboards



class TrainExperiments(Experiment):
    completed_activities = [] # optional to skip a few activities.

    def __init__(self, mode = 'skills'):
        self.mode = mode
        activities = Leaderboards.get_skill_names(keep_overall=False) if self.mode == 'skills' \
            else activities = Leaderboards.get_minigame_names()

        self.activities = [activity for activity in activities if activity not in self.completed_activities]
        print(f'You have {len(self.activities)} activities to complete!')

    def get_data(self, activity):
        rows = get_hiscore(activity, limit=self.user_limit, activity_type=self.mode)
        data = np.array(rows)

        # Remove the 'Banned' column before processing
        X = np.delete(data, 0, axis=1)
        y = data[:, 0].astype(int)  # 'Banned' as target variable

        skills_experience_columns = list(range(0, 24))
        live_skills_ratio_columns = list(range(24, 48))
        live_minigames_score_columns = list(range(48, 124))
        daily_skills_experience_columns = list(range(124, 148))
        daily_minigames_score_columns = list(range(148, 224))

        # Define indices of columns to scale, adjusted after removing the 'Banned' column
        scale_columns = skills_experience_columns + live_minigames_score_columns + daily_skills_experience_columns + daily_minigames_score_columns

        # Passthrough columns, adjusted for 'live_skills_ratio'
        passthrough_columns = live_skills_ratio_columns

        # Define the transformers
        transformers = [
            ('scale', StandardScaler(), scale_columns),
            ('passthrough', 'passthrough', passthrough_columns)
        ]

        # Creating the ColumnTransformer
        preprocessor = ColumnTransformer(transformers=transformers)

        return X, y, preprocessor

    def run(self):
        for activity in self.activities:
            print(f'Training {activity}...')
            self.run_activity(activity)

    def run_activity(self, activity):
        X, y, preprocessor = self.get_data(activity)
        if len(y) < 500:
            print(f'Skipping {activity} due to lack of data. {len(y)}/500 required.')
            return
        mlflow.set_experiment(activity)

        for name, classifier in self.classifiers:
            with mlflow.start_run():
                # Create the pipeline
                pipeline = ImblearnPipeline([
                    ('preprocessor', preprocessor),
                    ('smote', SMOTE(random_state=42)),
                    ('classifier', classifier)
                ])


                # Log pipeline components and PCA components
                mlflow.log_param("Classifier", name)
                mlflow.log_param("Sampling", "SMOTE")

                # Calculate scores
                accuracy_scores = cross_val_score(pipeline, X, y, cv=self.cv, scoring='accuracy')
                y_pred_proba = cross_val_predict(pipeline, X, y, cv=self.cv)

                y_pred = (y_pred_proba >= 0.5).astype(int)
                accuracy_per_class = [
                    accuracy_score(y == k, y_pred == k) for k in [0, 1]
                ]
                roc_auc = roc_auc_score(y, y_pred)

                recall_per_class = recall_score(y, y_pred, average=None)

                # Confusion matrix
                conf_matrix = confusion_matrix(y, y_pred)

                mlflow.log_metric("Mean Accuracy", np.mean(accuracy_scores))
                mlflow.log_metric("ROC-AUC", roc_auc)
                mlflow.log_metric("Recall Class 0", recall_per_class[0])
                mlflow.log_metric("Recall Class 1", recall_per_class[1])

                mlflow.log_metric("Accuracy Class 0", accuracy_per_class[0])
                mlflow.log_metric("Accuracy Class 1", accuracy_per_class[1])

                df_conf_matrix = pd.DataFrame(conf_matrix, index=["True Neg", "True Pos"],
                                              columns=["Pred Neg", "Pred Pos"])
                conf_matrix_file_path = f"{name}_matrix.csv"
                df_conf_matrix.to_csv(conf_matrix_file_path)
                mlflow.log_artifact(conf_matrix_file_path)
                os.remove(conf_matrix_file_path)

                inference_pipeline = ImblearnPipeline([
                    ('preprocessor', preprocessor),
                    ('classifier', classifier)
                ])

                inference_pipeline.fit(X,y)

                mlflow.sklearn.log_model(inference_pipeline, "model")

                mlflow.end_run()


if __name__ == '__main__':
    TrainExperiments(mode='skills').run()
    TrainExperiments(mode='minigames').run()
    publish_best_experiments('v1')
