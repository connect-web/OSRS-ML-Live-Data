import mlflow

from .experiments import get_best_roc_auc_experiments
from .get_models import get_models
from config.settings import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = mlflow.tracking.MlflowClient()

MODELS_BY_NAME = get_models()

def get_model_by_name(name):
    model_version = MODELS_BY_NAME.get(name)
    if model_version is None:
        raise ValueError(f'Model with name {name} not found.')
    model_uri = model_version.source
    model = mlflow.pyfunc.load_model(model_uri)
    return model

def publish_best_experiments(version_alias):
    df = get_best_roc_auc_experiments()
    for index, row in df.iterrows():
        create_model(row['run_id'], row['activity'], version_alias)

def create_model(run_id, activity_name, version_alias, environment="prod"):
    artifact_path = "model"
    model_uri = f"runs:/{run_id}/{artifact_path}"

    # Register the model in the Model Registry specific to the environment
    model_name = f"{environment}.{activity_name}"
    model_details = mlflow.register_model(model_uri=model_uri, name=model_name)

    # Get the version of the registered model
    version = model_details.version

    # Set model version tags to denote its status within the environment
    client.set_model_version_tag(name=model_name, version=version, key="validation_status", value="pending")

    # Assign environment-specific alias (e.g., dev_champion, staging_champion, prod_champion)
    alias_name = f"{environment}_{version_alias}"
    client.set_registered_model_alias(name=model_name, alias=alias_name, version=version)

    print(f"Model registered in {environment} environment and assigned alias '{alias_name}'; version: {version}")

