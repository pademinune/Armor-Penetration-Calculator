
$DEST = "C:\Program Files (x86)\World_of_Tanks_NA\res_mods\2.2.1.1\scripts\client\gui\mods"

python27 -m py_compile mod_armor_pen_calculator.py
Move-Item -Force mod_armor_pen_calculator.pyc bin/

python27 -m py_compile pade_constants.py
Move-Item -Force pade_constants.pyc bin/

python27 -m py_compile pade_gui.py
Move-Item -Force pade_gui.pyc bin/

python27 -m py_compile pade_config.py
Move-Item -Force pade_config.pyc bin/

python27 -m py_compile mod_pade_settings_gui.py
Move-Item -Force mod_pade_settings_gui.pyc bin/


Copy-Item bin/mod_armor_pen_calculator.pyc $DEST
Copy-Item bin/pade_constants.pyc $DEST
Copy-Item bin/pade_gui.pyc $DEST
Copy-Item bin/pade_config.pyc $DEST
Copy-Item bin/mod_pade_settings_gui.pyc $DEST -Force


Write-Output "Compiled and copied nightly branch mod files to '$DEST'"
