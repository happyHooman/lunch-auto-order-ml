import pickle
import time

import numpy as np

from ML.NeuralNetwork_old import NeuralNetwork
from ML.get_user_training_data import get_training_data
from ML.DBfunctions import add_log
from common import parent_directory, TRAINING_MODES, setup_logger


def train(user_id, mode=0):
    """
    :param user_id: id of the user to train
    :param mode:
    :return: Doesn't return anything
    The function trains a model for the user based on it's previous orders
    """
    # CONFIGURABLE VARIABLES
    precision = .02  # finish the training when the error is less
    batch_size = 100  # number of training iterations between tests
    timeout_minutes = TRAINING_MODES[mode]['duration']  # training time limit in minutes
    precision_fitting_occurence = 5  # how many times in a row the condition should check before stopping the training
    accuracy_width = .4  # accepted deviation from expected result
    acceptable_accuracy = 80  # acceptable accuracy for a good training
    train_data_ratio = .8  # the rest is the test data ratio

    # INITIALIZATION
    d = NeuralNetwork([85, 16, 16, 1])
    batch = 0
    td_iter = 0
    err = 0
    accuracy = 0
    t_data = get_training_data(user_id)
    np.random.shuffle(t_data)
    zzz = int(len(t_data) * train_data_ratio)
    training_data = t_data[:zzz]
    test_data = t_data[zzz:]

    lg = setup_logger('train', 'trainer.log')
    lg.info(f'Training for user {user_id} started with priority {mode}')

    log_entry = [user_id, str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), len(t_data), batch_size]

    if len(t_data) < 300:
        log_entry += [0, 0, 0, 0, str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 2]
        add_log(log_entry)
        return 1
    del t_data

    # TRAINING GOES HERE
    try:
        stop = False
        last_precision_fitting = 0
        timeout = time.time() + 60 * timeout_minutes
        positives = [x for x in training_data if x[-1][0] == 1]
        negatives = [x for x in training_data if x[-1][0] == 0]
        while not stop:
            td_iter += 1
            np.random.shuffle(negatives)
            training_set = positives + negatives[:len(positives)]
            np.random.shuffle(training_set)
            batch_end = len(training_set)
            while batch_end > 1:
                batch += 1
                err = 0
                accuracy = 0

                for data in training_set[max(batch_end - batch_size, 0):batch_end]:
                    d.train(*data)
                    err += d.cost

                for data in test_data:
                    expected = data[-1][0]
                    predicted = d.predict(data[0])[0]
                    accuracy += 1 if (expected == 1 and predicted > 1 - accuracy_width) or \
                                     (expected == 0 and predicted < accuracy_width) else 0

                err = err / min(batch_size, batch_end)
                accuracy = (accuracy / len(test_data)) * 100

                if batch > 300 and (err < precision or accuracy > acceptable_accuracy):
                    if last_precision_fitting == batch - 1:
                        precision_fitting_occurence -= 1
                    else:
                        precision_fitting_occurence = 5
                    last_precision_fitting = batch

                if precision_fitting_occurence == 0:
                    stop = True
                    reason = TRAINING_MODES['accuracy_reason']
                if time.time() > timeout:
                    stop = True
                    reason = TRAINING_MODES[mode]['reason']

                if stop:
                    log_entry += [batch, td_iter, err, accuracy,
                                  str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())),
                                  reason]
                    add_log(log_entry)
                    break

                batch_end -= batch_size

    except KeyboardInterrupt:
        log_entry += [batch, td_iter, err, accuracy, str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())), 1]
        add_log(log_entry)
        pass

    finally:
        lg.info(f'Training for user {user_id} finished')
        file_name = f'{parent_directory}/models/user{user_id}.pkl'
        pickle.dump(d, open(file_name, 'wb'), pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    train(12)
