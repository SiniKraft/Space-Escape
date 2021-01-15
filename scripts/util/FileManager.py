import os
import shutil
import importlib

lang_files_to_load = ['fr_FR', 'en_US']

lang_number = len(lang_files_to_load)  # Count the number of files entries

for x in range(0, lang_number):
    shutil.copyfile(os.path.dirname(__file__) + '/../../ressources/lang/' + lang_files_to_load[x] + ".txt",
                    "tmp/lang_" + lang_files_to_load[x] + ".py")  # will copy resource/lang file into tmp/lang.

for x in range(0, lang_number):
    try:
        importlib.import_module("tmp.lang_" + lang_files_to_load[x])  # load modified lang file
    except:
        shutil.copyfile('default/lang/' + lang_files_to_load[x] + '.py',
                        os.path.dirname(__file__) + "/../../ressources/lang/" + lang_files_to_load[x] + ".txt")
        shutil.copyfile(os.path.dirname(__file__) + '/../../ressources/lang/' + lang_files_to_load[x] + '.txt',
                        "tmp/lang_" + lang_files_to_load[x] + ".py")
        print("[ERROR]: Failed to launch lang resource '" + lang_files_to_load[x] + "', using default !")
        importlib.import_module("tmp.lang_" + lang_files_to_load[x])
        # will copy default to modified, because error where found.
