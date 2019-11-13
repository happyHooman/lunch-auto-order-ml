from datetime import datetime

import mysql.connector as con

from local_settings import DB_CONNECT_ARGS


def add_log(log):
    db = con.connect(**DB_CONNECT_ARGS)
    sql = 'insert into LAOB_training_logs ' \
          '(user_id, start_time, nr_items, b_size, nr_batch, td_iter, err, accuracy, end_time, reason) ' \
          'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        curs = db.cursor()
        curs.nextset()
        curs.execute(sql, log)
        curs.close()
        db.commit()
    except con.Error as err:
        db.rollback()
        print(f"Failed inserting log: {err}")
    finally:
        db.close()


def do_sql(sql):
    db = con.connect(**DB_CONNECT_ARGS)
    curs = db.cursor()
    curs.execute(sql)
    r = curs.fetchall()
    curs.close()
    db.close()
    return r


def get_user_by_id(id):
    sql = f"select first_name, last_name from auth_user where id = {id}"
    return do_sql(sql)


def get_active_users():
    sql = "SELECT id FROM auth_user where id in (SELECT user_id FROM users_userprofile where auto_order =1) and last_login > date(now() - interval 3 month) and username not like 'intern%'"
    return [i[0] for i in do_sql(sql)]


def get_all_menus():
    sql = 'SELECT name FROM h_dishes;'
    return [i[0] for i in do_sql(sql)]


def get_words_dictionary():
    sql = 'SELECT wrong, correct FROM h_words_dictionary;'
    return do_sql(sql)


def get_words():
    sql = 'SELECT word FROM h_words;'
    return [x[0] for x in do_sql(sql)]


def get_user_orders(user):
    sql = f'SELECT first, second, fitness FROM h_orders where user = {user};'
    dishes = do_sql(sql)

    order_ids = []
    for x in dishes:
        order_ids.extend([a for a in x if a is not None])

    sql = f'SELECT date FROM h_dishes where old_id in {tuple(order_ids)}'
    dates_with_orders = tuple(set([str(x[0]) for x in do_sql(sql)]))

    sql = f'select * from h_dishes where date in {dates_with_orders}'
    return do_sql(sql), order_ids


def get_day_options(user, day):
    sql = f'SELECT first, second, fitness FROM h_orders where user = {user};'
    dishes = do_sql(sql)

    order_ids = []
    for x in dishes:
        order_ids.extend([a for a in x if a is not None])

    sql = f'SELECT date FROM h_dishes where old_id in {tuple(order_ids)}'
    dates_with_orders = list(set([str(x[0]) for x in do_sql(sql)]))
    dates_with_orders.sort(key=lambda d: datetime.strptime(d, '%Y-%m-%d'), reverse=True)
    sql = f'select * from h_dishes where date in (\'{dates_with_orders[day]}\')'
    dishes = do_sql(sql)
    ordered = [x[1] for x in dishes if x[1] in order_ids]

    return dishes, ordered


def get_next_day_options():
    sql = 'select id from menu_menu where date like (SELECT date from menu_menu order by date desc limit 1) and status=0 and restaurant_id !=4;'
    menu = [x[0] for x in do_sql(sql)]
    sql = 'select mi.id, mi.name, mi.type, mm.date, mm.restaurant_id from menu_item mi left join menu_menu mm on mi.menu_id = mm.id where menu_id in '
    if len(menu) == 1:
        sql += f'({menu[0]});'
    else:
        sql += f'{tuple(menu)};'

    return do_sql(sql)


def get_last_user_training(user_id):
    sql = f'SELECT start_time, reason FROM LAOB_training_logs where user_id = {user_id} order by start_time desc limit 1;'
    return do_sql(sql)[0]
