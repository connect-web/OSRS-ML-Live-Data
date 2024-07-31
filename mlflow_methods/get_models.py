import mlflow
from config.settings import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = mlflow.tracking.MlflowClient()


def get_models():
    model_version_objects = {}

    # Fetch all registered models
    registered_models = client.search_registered_models()

    # Iterate through all registered models
    for model in registered_models:
        # Get all versions of the registered model
        model_versions = client.search_model_versions(f"name='{model.name}'")

        # Store reference to only the latest version of the model
        all_versions = {
            int(version.version) : version
            for version in model_versions
        }
        # print(f'all versions: {all_versions}')
        version_options = list(all_versions.keys())

        if version_options:
            best_version_id = max(version_options)
            model_version_objects[model.name] = all_versions[best_version_id]

    return model_version_objects