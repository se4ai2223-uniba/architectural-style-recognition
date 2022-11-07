import numpy as np
from src.data.dataset import Dataset
from src.models.model import Model
import os
import tensorflow as tf
import os
from sklearn.metrics import precision_recall_fscore_support as score
import cv2

def test_modelPerformances():
    model_ = Model()
    data = Dataset()
    testSet = data.getTestSet()
    # load the best model
    loaded_model = model_.loadModel(os.path.join('models', 'saved-model'))
    # Compile model
    loaded_model.compile(
    optimizer=tf.keras.optimizers.SGD(
        learning_rate=model_.params.learning_rate, momentum=model_.params.momentum
    ),
    loss=tf.keras.losses.CategoricalCrossentropy(
        from_logits=False, label_smoothing=model_.params.label_smoothing
    ),
    metrics=["accuracy"],
    )
    # get labels
    predictions_ = np.array([])
    labels_ =  np.array([])

    for x, y in testSet:
        predictions_ = np.concatenate([predictions_, np.argmax(loaded_model.predict(x),axis=-1)])
        labels_ = np.concatenate([labels_, np.argmax(y.numpy(), axis=-1)])
    print(predictions_, labels_)
    # get scores
    precision,recall,fscore,support=score(labels_, predictions_, average='macro')
    evals = loaded_model.evaluate(testSet) # type: ignore
    assert fscore > 0.20
    assert evals[1] >= 0.50
    

# directional test
# 2 immagini diverse 2 ouput diversi
def test_directional():
    model_ = Model()
    data = Dataset()
    testSet = data.getTestSet()
    # load the best model
    loaded_model = model_.loadModel(os.path.join('models', 'saved-model'))
    output = []
    label = -1
    # load two images of different classes from testSet
    for x, y in testSet:
        if(label != np.argmax(y.numpy(), axis=-1)):
            label = np.argmax(y.numpy(), axis=-1)
            prediction = loaded_model.predict(x)
            print(label, prediction)
            output.append(prediction)
            if (len(output) == 2):
                break
    print(output[0], output[1])    
    assert np.argmax(output[0]) != np.argmax(output[1])



# invariance test
# immagine con poche variazioni producono lo stesso output
def test_invariance():
    model_ = Model()
    data = Dataset()
    testSet = data.getTestSet()
    # load the best model
    loaded_model = model_.loadModel(os.path.join('models', 'saved-model'))
    example = list(testSet.as_numpy_iterator())

    image_matrix = np.squeeze(example[0][0])
    image = np.array(image_matrix ,dtype=np.uint8)

    cv2.imshow('img', image)
    cv2.waitKey(0)
    cv2.destroyWindow('i')


test_invariance()