from shutil import copyfile
from importlib import import_module
import pickle
from os.path import isfile
import logging
logging.basicConfig(filename='latest.log', format='[%(asctime)s][%(levelname)s/%(name)s]: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S')

logging.info("Starting file manager ...")

lang_files_to_load = ['en_US', 'fr_FR']

lang_files_names = {"Français": "fr_FR", "English": "en_US"}

lang_list = ['English', 'Français']

lang_number = len(lang_files_to_load)  # Count the number of files entries


# settings loader

def new_settings():
    with open('settings.ini', 'wb') as settings_file:
        setting_list = ["English", False]
        pickle.dump(setting_list, settings_file)
        settings_file.close()
    return setting_list  # will create new settings, return it, and save it.


def save(setting_list, directory):
    with open(directory, 'wb') as settings_file:
        pickle.dump(setting_list, settings_file)
        settings_file.close()  # will overwrite existing file


def load(directory):
    with open(directory, 'rb') as loaded_file:
        settings_file = pickle.load(loaded_file)
        loaded_file.close()
    return settings_file  # will load file in the directory specified and return it.


if isfile("settings.ini"):  # load the save
    try:
        settings_list = load("settings.ini")
        logging.info("Loaded default settings.")
    except:
        settings_list = new_settings()
        logging.error("Failed to load settings, recreating them.")
else:
    settings_list = new_settings()
    logging.error("Default settings file was not found, creating a blank one !")

for x in range(0, lang_number):
    try:
        copyfile('resources/lang/' + lang_files_to_load[x] + ".txt",
                 "scripts/util/tmp/lang_" + lang_files_to_load[x] + ".py")  # will copy resource/lang file into tmp/lang
    except FileNotFoundError:
        logging.error("File '" + lang_files_to_load[x] + "' not found in resources folder !")

        copyfile('scripts/util/default/lang/' + lang_files_to_load[x] + '.py',
                 "resources/lang/" + lang_files_to_load[x] + ".txt")

for x in range(0, lang_number):
    try:
        import_module("scripts.util.tmp.lang_" + lang_files_to_load[x])  # load modified lang file
    except:
        copyfile('scripts/util/default/lang/' + lang_files_to_load[x] + '.py',
                 "resources/lang/" + lang_files_to_load[x] + ".txt")
        copyfile('resources/lang/' + lang_files_to_load[x] + '.txt',
                 "scripts/util/tmp/lang_" + lang_files_to_load[x] + ".py")
        logging.error("Failed to launch lang resource '" + lang_files_to_load[x] + "', using default !")
        import_module("scripts.util.tmp.lang_" + lang_files_to_load[x])
        # will replace modified files with the defaults because errors were found on them.

    finally:
        try:
            scripts = __import__("scripts.util.tmp.lang_" + lang_files_to_load[x])
            exec(lang_files_to_load[x] + " = " + 'scripts.util.tmp.lang_' + lang_files_to_load[x] + '.' +
                 lang_files_to_load[x]
                 + '_lang')
            # load list components as single vars containing info
            exec("logging.info('Successfully loaded resource " + "\\'" + lang_files_to_load[x] + ".txt" + "\\'" + "." +
                 "')")
        except:
            logging.error("Can\'t load resource \'" + lang_files_to_load[x] + "\' !")

logging.info("All files are loaded.")
