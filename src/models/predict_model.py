import tensorflow as tf
from tensorflow import keras
import os 
from tensorflow.keras.models import model_from_json
import tensorflow_hub as hub

dataset_path_test = 'data/processed/test'

def buildTestset():
    ds_test = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path_test,
    labels='inferred',
    label_mode = 'categorical',
    image_size = (224, 224),
    shuffle=True,
    seed=123,
    batch_size=1)
    return ds_test

def loadModel(path): 
    model_loaded = tf.keras.Sequential()
    # load json and create model
    json_file = open(os.path.join(path,'model.json'), 'r')
    model_json = json_file.read()
    json_file.close()
    model_loaded = model_from_json(model_json, custom_objects={'KerasLayer': hub.KerasLayer})
    # load weights into new model
    model_loaded.load_weights(os.path.join(path,"model.h5"))
    print("Loaded model from disk")
    return model_loaded

model = loadModel("models\saved-model")
test_set = buildTestset()
model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.005, momentum=0.9), 
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False, label_smoothing=0.1),
    metrics=['accuracy']
)
evaluations = model.evaluate(test_set)
predictions_test = model.predict(test_set)

print(evaluations)
print(predictions_test)

f = open("src/models/results.txt", "w")
f.write(str(evaluations)+"\n"+str(predictions_test))
f.close()


