import os
import tensorflow as tf
import mlflow
from dotenv import find_dotenv
from dotenv import dotenv_values
from src.models.model import Model


mlflow.set_tracking_uri(
    "https://dagshub.com/RobertoLorusso/architectural-style-recognition.mlflow"
)
conf = dotenv_values(find_dotenv())
os.environ["MLFLOW_TRACKING_USERNAME"] = conf["MLFLOW_TRACKING_USERNAME"]  # type: ignore
os.environ["MLFLOW_TRACKING_PASSWORD"] = conf["MLFLOW_TRACKING_PASSWORD"]  # type: ignore
mlflow.set_experiment("Evaluation stage")
mlflow.start_run()

model = Model()
test_set = model.data.getTestSet()


model_loaded = model.loadModel(os.path.join("models", "saved-model"))

model_loaded.compile(
    optimizer=tf.keras.optimizers.SGD(
        learning_rate=model.params.learning_rate, momentum=model.params.momentum
    ),
    loss=tf.keras.losses.CategoricalCrossentropy(
        from_logits=False, label_smoothing=model.params.label_smoothing
    ),
    metrics=["accuracy"],
)


evaluations = model_loaded.evaluate(test_set)
predictions_test = model_loaded.predict(test_set)

mlflow.log_metrics(
    {"test-set-accuracy": evaluations[1], "test-set-loss": evaluations[0]}
)

mlflow.sklearn.log_model(model, "model", registered_model_name="MobileNetV2Archinet")
mlflow.end_run()

print(evaluations)
print(predictions_test)

with open("src/models/results.txt", "w") as f:
    f.write(str(evaluations) + "\n" + str(predictions_test))
    f.close()
