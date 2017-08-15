__author__ = 'Guilherme Matsumoto'

import logging, warnings
import numpy as np
from skmultiflow.classification.meta.oza_bagging import OzaBagging
from skmultiflow.classification.lazy.knn_adwin import KNNAdwin
from skmultiflow.data.generators.sea_generator import SEAGenerator


def demo():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    warnings.filterwarnings("ignore", ".*Passing 1d.*")
    stream = SEAGenerator(1, noise_percentage=6.7)
    stream.prepare_for_use()
    #print(stream.get_classes())
    clf = OzaBagging(h=KNNAdwin(k=8,max_window_size=2000,leaf_size=30), ensemble_length=2)
    sample_count = 0
    correctly_classified = 0
    max_samples = 100
    train_size = 8
    first = True
    if train_size > 0:
        X, y = stream.next_instance(train_size)
        clf.partial_fit(X, y, classes=stream.get_classes())
        first = False

    while sample_count < max_samples:
        if sample_count % (max_samples/20) == 0:
            logging.info('%s%%', str((sample_count//(max_samples/20)*5)))
        X, y = stream.next_instance()
        my_pred = clf.predict(X)

        if first:
            clf.partial_fit(X, y, classes=stream.get_classes())
            first = False
        else:
            clf.partial_fit(X, y)

        if my_pred is not None:
            if y[0] == my_pred[0]:
                correctly_classified += 1

        sample_count += 1

    print(str(sample_count) + ' samples analyzed.')
    print('My performance: ' + str(correctly_classified / sample_count))

if __name__ == '__main__':
    demo()