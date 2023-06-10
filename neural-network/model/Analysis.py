from train import *
import os

class Analysis:
    def __init__(self):
        self.accuracies = []
        self.errors_train = []
        self.errors_valid = []
        self.test_accuracy = []
        self.results = {}

    def partial(self, neurons, rate, momentum, error_train, error_valid, accuracy):
        if neurons not in self.results:
            self.results[neurons] = {}
        if rate not in self.results[neurons]:
            self.results[neurons][rate] = {}
        self.results[neurons][rate][momentum] = {
            'error_train' : error_train,
            'error_valid' : error_valid,
            'accuracy' : accuracy
        }

    def save_charts(self):
        for neurons, nested_dict in self.results.items():
            for learning_rate, nested_nested_dict in nested_dict.items():
                for momentum, metriche in nested_nested_dict.items():
                    error_train = metriche['error_train']
                    error_valid = metriche['error_valid']

                    plt.plot(error_train, label='Train Error')
                    plt.plot(error_valid, label='Valid Error')
                    plt.xlabel('Epoch')
                    plt.ylabel('Error')
                    plt.title(f'Neurons: {neurons}, Learning Rate: {learning_rate}, Momentum: {momentum}')
                    plt.legend()
                    plt.savefig(get_result_path(f"{neurons}-neurons-{learning_rate}-rate-{momentum}-momentum"))
                    plt.close()

    def get_result_path(name):
        return os.path.join(os.getcwd(), "results", name + ".png")

    def make_predictions(self, X, layers):
        """
        Execute forward propagation on network and gets prediction's class from result's array
        """
        forward_prop(X, layers)
        predictions = np.argmax(layers[-1].Z, 0)
        return predictions

    def test_prediction(self, index, layers, X, Y):
        """
        Gets the index of the image in the X array, prints the expected class and the label class.
        Next, visualize the image with matplotlib
        """
        current_image = X[:, index, None]
        prediction = self.make_predictions(X[:, index, None], layers)
        label = Y[index]
        print("Prediction: ", prediction)
        print("Label: ", label)
        
        current_image = current_image.reshape((28, 28)) * 255
        plt.gray()
        plt.imshow(current_image, interpolation='nearest')
        plt.show()