from train import *
import pandas as pd
from model.Properties import *
from model.Dataset import *
from model.Analysis import *

def main():
    properties = Properties("properties.ini")
    ds = Dataset(shuffle=True)
    analysis = Analysis()

    print(f"epochs for each training : {properties.epochs}")
    for neurons in properties.neurons:
        for rate in properties.learning_rate:
            for momentum in properties.momentum:
                layers = get_layers(neurons, momentum, ds.train_data.shape[0], properties.act_function)
                results = gradient_descent(ds, layers, rate, properties.epochs, properties.error_function)
                analysis.partial(neurons, rate, momentum, *results)
                print(f"end with: momentum {momentum}, learning_rate {rate}, neurons {neurons}, accuracy: {results[2]}")
    
    analysis.save_charts()

def get_layers(neurons, momentum, columns, act_function):
    return [Layer((neurons, columns), act_function['function'], act_function['derivative'], momentum), 
            Layer((10, neurons), softmax, ReLU_deriv, momentum)
    ]

if __name__ == "__main__":
    main()