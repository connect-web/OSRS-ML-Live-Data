import pandas as pd
import numpy as np

from .data_collection import get_hiscore
from mlflow_methods.models import get_model_by_name


def inference(activity='Attack', activity_type='skills'):
    # Fetch the model by name
    model_name = f'prod.{activity}'
    try:
        model = get_model_by_name(model_name)
    except Exception as e:
        print(e)
        print(f'Model with name {model_name} not found.')
        return

    # Get the live data
    rows = get_hiscore(activity, activity_type=activity_type)
    if len(rows) == 0:
        print(f'No data found for activity {activity}.')
        return

    # Preprocess the data
    usernames, player_ids, durations, input_data = preprocess_input(rows)
    if len(usernames) == 0:
        print(f'No data to process for {activity}.')
        return
    # Run inference
    predictions = model.predict(input_data)

    # Bind predictions to usernames
    results = pd.DataFrame({
        'Username': usernames,
        'PlayerId': player_ids,
        'Duration': durations,
        'Prediction': predictions
    })

    return results


def preprocess_input(rows):
    data = np.array(rows)

    # Extract usernames, player_ids, durations, and computed flags
    usernames = data[:, 0]
    player_ids = data[:, 225]
    durations = data[:, 226]
    computed = data[:, 227]

    # Remove rows where computed is True
    mask = computed.astype(bool) == False
    filtered_data = data[mask]

    # Remove unwanted columns from filtered data
    X = np.delete(filtered_data, [0, 225, 226, 227], axis=1)

    # Convert to float for numerical processing
    X = X.astype(float)

    # Update usernames, player_ids, and durations after filtering
    usernames = usernames[mask]
    player_ids = player_ids[mask]
    durations = durations[mask]
    return usernames, player_ids, durations, X


if __name__ == "__main__":
    r = inference()
