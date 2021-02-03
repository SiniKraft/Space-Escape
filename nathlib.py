##########################################################
# This is the nathlib, a lib used by most of my programs #
# You are free to use it #
##########################################################
import pickle
import logging
import datetime
import json
import urllib.request

# nathlib version :
nl_v = "1.0.001"


def save(setting_list, directory):
    """Will save a python object in binary format
    Usage : save(my_var, "my_var.dat")"""
    with open(directory, 'wb') as settings_file:
        pickle.dump(setting_list, settings_file)
        settings_file.close()


def load(directory):
    """Will load a binary file into python object
    Usage : my_loaded_var = load("my_saved_var.dat")"""
    with open(directory, 'rb') as loaded_file:
        settings_file = pickle.load(loaded_file)
        loaded_file.close()
    return settings_file  # will load file in the directory specified and return it.


def start_logs(filename):
    """Start a basic logging configuration
    Usage : start_logs("latest.log")"""
    logging.basicConfig(filename=filename, format='[%(asctime)s][%(levelname)s/%(name)s]: %(message)s',
                        level=logging.DEBUG, datefmt='%H:%M:%S')


def get_date(date_type):
    """Will return desired date, useful !
    Warning : will return nothing if the argument isn't correct !
    usage : my_value = get_date("date_time_str")"""
    now = datetime.date.today()
    time_tmp = datetime.datetime.now()
    if date_type == "day":
        return now.day
    elif date_type == "year":
        return now.year
    elif date_type == "month":
        return now.month
    elif date_type == "date_str":
        return str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    elif date_type == "date_list":
        return [now.day, now.month, now.year]
    elif date_type == "date":
        return now
    elif date_type == "hour":
        return time_tmp.hour
    elif date_type == "minute":
        return time_tmp.minute
    elif date_type == "second":
        return time_tmp.second
    elif date_type == "time":
        return str(time_tmp.hour) + ":" + str(time_tmp.minute) + ":" + str(time_tmp.second)
    elif date_type == "time_list":
        return [time_tmp.hour, time_tmp.minute, time_tmp.second]
    elif date_type == "date_time_str":
        return str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str(time_tmp.hour) + ":" +\
               str(time_tmp.minute) + ":" + str(time_tmp.second)
    return None


def log(message, level):
    """Will print a log and save it into a file
    Usage : log("This is an error", "error")"""
    if level == "debug":
        logging.debug(message)
    elif level == "info":
        logging.info(message)
    elif level == "warn":
        logging.warn(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)
    print("[%s][%s/%s]: %s" % (get_date("time"), level.upper(), "main", message))


def check(value, filter_in):
    """Will check if string contains only characters of filter_in string
    Usage : my_check = check("abc", "abcdefghij")
    can also be used in if condition"""
    for letter in value:
        if letter not in filter_in:
            return False
    return True


def get_json_from_url(url_in):
    """Will load a json from url and convert it as python dictionary
    Usage : my_dict = get_json_from_url("https://my_json")"""
    with urllib.request.urlopen(url_in) as url:
        return json.loads(url.read().decode())


def save_json(dict_in, directory):
    """Will write txt file containing the json loaded from a python dictionary
    Usage : save_json(my_dict, "my_json.json")"""
    write_json = json.dumps(dict_in, indent=4)
    with open(directory, "w+") as file:
        file.write(write_json)
        file.close()  # create json


def load_json(directory):
    """Will load json from a file
    Usage : my_new_dict = load_json(my_json.json)"""
    with open(directory, "r") as file:
        data = json.load(file)
        file.close()
    return data
