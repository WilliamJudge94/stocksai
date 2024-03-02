from huggingface_hub import from_pretrained_keras
from utils import anomaly_prep

model = from_pretrained_keras("keras-io/
time-series-anomaly-detection-autoencoder")

prep = dict(anomaly=anomaly_prep)

def predict(data, prep_type='anomaly', model=model):
    prep_func = prep[prep_type]
    prepped_data = prep_func(data)
    return model.predict(prepped_data)