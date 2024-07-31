import pandas as pd
import numpy as np

from .data_collection import get_hiscore
from mlflow_methods.models import get_model_by_name

def inference(activity='Clue Scrolls (all)', activity_type='minigames'):
    # Fetch the model by name
    model_name = f'prod.{activity}'
    try:
        model = get_model_by_name(model_name)
    except:
        print(f'Model with name {model_name} not found.')
        return []

    # Get the live data
    rows = get_hiscore(activity,activity_type=activity_type)
    if len(rows) == 0:
        print(f'No data found for activity {activity}.')
        return []

    # Preprocess the data
    usernames, input_data = preprocess_input(rows)
    #print(input_data[0])
    # Run inference
    predictions = model.predict(input_data)

    # Bind predictions to usernames
    results = pd.DataFrame({
        'Username': usernames,
        'Prediction': predictions
    })

    predicted_bans = results[results['Prediction'] == 1]

    #print(predicted_bans)

    return predicted_bans['Username'].tolist()

def preprocess_input(rows):
    data = np.array(rows)

    # Extract usernames and features
    usernames = data[:, 0]
    X = np.delete(data, 0, axis=1)
    X=np.array(X, dtype=float)

    return usernames, X

if __name__ == "__main__":
    r = inference()
    print(r)
