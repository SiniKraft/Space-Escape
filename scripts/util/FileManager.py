import os
import shutil

shutil.copyfile(os.path.dirname(__file__) + '/../../ressources/lang/fr_FR.txt',
                "tmp/lang_fr_FR.py")

try:
    from tmp.lang_fr_FR import fr_FR_lang
except:
    shutil.copyfile('default/lang/fr_FR.py',
                    os.path.dirname(__file__) + "/../../ressources/lang/fr_FR.txt")
    shutil.copyfile(os.path.dirname(__file__) + '/../../ressources/lang/fr_FR.txt',
                    "tmp/lang_fr_FR.py")
    print("[ERROR]: Failed to launch lang resource 'fr_FR', using default !")
    from tmp.lang_fr_FR import fr_FR_lang

