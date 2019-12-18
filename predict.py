import pickle
from ML.get_user_training_data import get_available_menus
from ML.trainer import parent_directory
from common import setup_logger


def predict(user):
    lg = setup_logger('predictor', 'predictor.log')
    file_name = f'{parent_directory}/models/user{user}.pkl'
    try:
        user_bot = pickle.load(open(file_name, 'rb'))
    except FileNotFoundError:
        lg.info(f'no training file for user {user}')
        return []

    available_options = get_available_menus()

    day_data = {}
    for x in available_options:
        predict_data = x[1:3] + [1 / x[3], 1 / x[4], 1 / x[5], 1 / x[6]]
        predicted = user_bot.predict(predict_data)[0]

        restaurant = str(x[6])
        tip = x[2]
        details = [tip] + [x[0]] + [predicted]

        try:
            if day_data[restaurant]:
                try:
                    day_data[restaurant][tip] += [details]
                except KeyError:
                    day_data[restaurant][tip] = [details]
        except KeyError:
            day_data[restaurant] = {}
            day_data[restaurant][tip] = [details]

    for restaurant_key, restaurant_value in day_data.items():
        full = []
        fitness = 0
        full_keys = []
        fitness_keys = []
        for type_key, type_value in restaurant_value.items():
            day_data[restaurant_key][type_key] = max(type_value, key=lambda m: m[2])

        for type_key, type_value in restaurant_value.items():
            if type_key == 2:
                fitness += type_value[2]
                fitness_keys.append(type_key)
            else:
                full.append(type_value[2])
                full_keys.append(type_key)
        full = sum(full) / len(full)

        if full > fitness:
            for k in fitness_keys:
                day_data[restaurant_key].pop(k)
            day_data[restaurant_key]["rating"] = full
        else:
            for k in full_keys:
                day_data[restaurant_key].pop(k)
            day_data[restaurant_key]["rating"] = fitness

    key_max = max(day_data.keys(), key=(lambda key: day_data[key]["rating"]))

    result = [None] * 3
    for menu in day_data[key_max].items():
        if menu[0] != "rating":
            result[menu[1][0]] = menu[1][1]
    lg.info(f'Order {result} for {user}')
    return result


if __name__ == '__main__':
    import sys

    user_id = int(sys.argv[1])
    print(predict(user_id))
