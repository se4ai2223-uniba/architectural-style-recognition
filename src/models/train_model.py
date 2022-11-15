# -*- coding: utf-8 -*-
import os
import mlflow
from src.models.model import Model
from dotenv import dotenv_values
from dotenv import find_dotenv

model = Model()


# Init the mlflow connection and parameters to track
mlflow.set_tracking_uri(
    "https://dagshub.com/RobertoLorusso/architectural-style-recognition.mlflow"
)
conf = dotenv_values(find_dotenv())
os.environ["MLFLOW_TRACKING_USERNAME"] = conf["MLFLOW_TRACKING_USERNAME"]  # type: ignore
os.environ["MLFLOW_TRACKING_PASSWORD"] = conf["MLFLOW_TRACKING_PASSWORD"]  # type: ignore
mlflow.set_experiment("Training stage")
# Start MLFlow
mlflow.start_run()
mlflow.log_params(
    {
        "learning-rate": model.params.learning_rate,
        "momentum": model.params.momentum,
        "lable_smoothing": model.params.label_smoothing,
        "dropout-rate": model.params.dropout_rate,
        "regularized-l2": model.params.l2,
        "batch-size": model.params.batch_size,
        "epochs": model.params.epochs,
        "algorithm": model.params.algorithm,
        "loss": model.params.loss,
    }
)
model_trained, hist = model.trainModel()
SAVE_PATH = "models/saved-model"
model.saveModel(model_trained, SAVE_PATH)


train_loss = hist["loss"][-1]
val_loss = hist["val_loss"][-1]

train_accuracy = hist["accuracy"][-1]
val_accuracy = hist["val_accuracy"][-1]

print(train_loss, val_loss, train_accuracy, val_accuracy)

mlflow.log_metrics(
    {
        "train_accuracy": train_accuracy,
        "val_accuracy": val_accuracy,
        "train_loss": train_loss,
        "val_loss": val_loss,
    }
)

mlflow.sklearn.log_model(model, "model", registered_model_name="MobileNetV2Archinet")

mlflow.end_run()
