import mlflow
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv
import os

load_dotenv()  

# Set MLflow Tracking URI
mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))

def register_best_model():
    client = MlflowClient()
    
    # 1. Get experiment details
    experiment_name = "Ship_Fuel_Consumption"
    experiment = client.get_experiment_by_name(experiment_name)
    
    if not experiment:
        print(f"Error: Experiment '{experiment_name}' not found.")
        return

    # 2. Search for the best run based on Test_R2
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.Test_R2 DESC"],
        max_results=1
    )

    if not runs:
        print("No runs found for this experiment.")
        return

    best_run = runs[0]
    best_run_id = best_run.info.run_id
    best_model_name = best_run.data.params.get("model_name", "Unknown")
    best_r2 = best_run.data.metrics.get("Test_R2", 0.0)

    print(f"--- Best Run Details ---")
    print(f"Model Type  : {best_model_name}")
    print(f"Best Test R2: {best_r2:.4f}")
    print(f"Run ID      : {best_run_id}")

    # 3. FIX: Dynamically find the correct artifact path
    # This prevents the "Unable to find a logged_model" error
    artifacts = client.list_artifacts(best_run_id)
    
    # Look for a directory that contains an 'MLmodel' file
    model_artifact_path = None
    for artifact in artifacts:
        if artifact.is_dir:
            # Check if this directory is the model folder
            sub_artifacts = client.list_artifacts(best_run_id, path=artifact.path)
            if any(sub.path.endswith("MLmodel") for sub in sub_artifacts):
                model_artifact_path = artifact.path
                break

    if not model_artifact_path:
        print("Error: Could not find a valid logged model in the artifacts.")
        return

    print(f"Detected Artifact Path: {model_artifact_path}")

    # 4. Register the model
    model_uri = f"runs:/{best_run_id}/{model_artifact_path}"
    model_name = "Ship_Fuel_Consumption_Model"
    
    result = mlflow.register_model(
        model_uri=model_uri,
        name=model_name
    )

    print(f"Successfully registered version {result.version} of '{model_name}'.")

if __name__ == "__main__":
    register_best_model()
