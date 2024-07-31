import mlflow
import pandas as pd

from config.settings import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)



def list_all_experiments():
    # List all experiments
    experiments = mlflow.search_experiments()

    # Create a list of tuples (experiment_id, experiment_name)
    experiment_list = [(exp.experiment_id, exp.name) for exp in experiments]

    return experiment_list

def fetch_experiment_data(experiment_id):
    # Fetch all runs from a specific experiment
    runs = mlflow.search_runs(experiment_id)

    # Check if DataFrame is empty
    if runs.empty:
        return None #print("No data found for experiment ID:", experiment_id)
    return runs

def get_experiment_metrics(run_id):
    # Initialize the MLFlow client
    client = mlflow.tracking.MlflowClient()

    # Get the run details
    run = client.get_run(run_id)

    # Extract and return the metrics
    metrics = run.data.metrics
    return metrics


def get_best_roc_auc_experiments():
    """
    Get the metrics for each experiment that has been run.

    :return: Dataframe of each experiment & it's metrics.
    """
    best_scores = []
    invalid_experiments = 0
    metrics_missing = 0

    total = list_all_experiments()
    for experiment in total:
        # Get all the iterations of experiments with different parameters.
        experiment_data = fetch_experiment_data(experiment_id=experiment[0])

        if experiment_data is None:
            invalid_experiments += 1
        else:
            # Make a copy of the best run
            if 'metrics.ROC-AUC' in experiment_data:
                best_roc_auc_row = experiment_data.loc[
                    experiment_data['metrics.ROC-AUC'] == experiment_data['metrics.ROC-AUC'].max()].copy()

                best_roc_auc_row.loc[:,'experiment_id'] = experiment[0]
                best_roc_auc_row.loc[:,'experiment_name'] = experiment[1]


                activity_name = experiment[1].split('Experience Model')[0]
                activity_name = activity_name.replace("'", '', -1)

                best_roc_auc_row.loc[:,'activity'] = activity_name

                best_scores.append(best_roc_auc_row)
            else:
                metrics_missing += 1
    df = pd.concat(best_scores).reset_index(drop=True)


    print(f'You have {len(df)} valid experiments & {invalid_experiments} invalid experiments & {metrics_missing} metrics were missing.')
    return df