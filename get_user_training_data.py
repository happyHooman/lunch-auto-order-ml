from datetime import date

from ML.prepare_data import *
from ML.DBfunctions import get_user_orders, get_day_options, get_next_day_options


def get_training_data(user_id):
    orders, order_ids = get_user_orders(user_id)

    dish_names = format_dish_names([x[2] for x in orders])
    dish_names = [pad_names(x) for x in dish_names]

    orders = [list(x[3:6]) + ([1] if x[1] in order_ids else [0]) for x in orders]
    today = date.today()
    orders = [[x[0], x[1].month, x[1].weekday() + 1, (today - x[1]).days if (today - x[1]).days < 0 else (today - x[1]).days + 1] + x[2:] for x in orders]
    orders = [[x[0], 1 / x[1], 1 / x[2], 1 / x[3], 1 / x[4], x[5]] for x in orders]

    t = []
    for name, order in zip(dish_names, orders):
        t.append(([name] + order[:-1], [order[-1]]))
    return t


def get_day_menus(user_id, day):
    orders, order_ids = get_day_options(user_id, day)

    dish_names = format_dish_names([x[2] for x in orders])
    dish_names = [pad_names(x) for x in dish_names]

    orders = [list(x[3:6]) + ([1] if x[1] in order_ids else [0]) for x in orders]
    today = date.today()
    orders = [[x[0], x[1].month, x[1].weekday() + 1, (today - x[1]).days + 1] + x[2:] for x in orders]
    orders = [[x[0], 1 / x[1], 1 / x[2], 1 / x[3], 1 / x[4], x[5]] for x in orders]

    t = []
    for name, order in zip(dish_names, orders):
        t.append(([name] + order[:-1], [order[-1]]))
    return t


def get_available_menus():
    orders = get_next_day_options()

    dish_names = format_dish_names([x[1] for x in orders])
    dish_names = [pad_names(x) for x in dish_names]
    today = date.today()
    orders = [
        [x[0], name, x[2], x[3].month, x[3].weekday() + 1, (today - x[3]).days if (today - x[3]).days < 0 else (today - x[3]).days + 1,
         x[4]] for x, name in
        zip(orders, dish_names)]

    return orders


if __name__ == '__main__':
    import pandas as pd

    user = 55
    training_data = get_training_data(user)
    pd.DataFrame(training_data).to_excel('test.xlsx', sheet_name='sheet1')
