
$DEST = "C:\Program Files (x86)\World_of_Tanks_NA\res_mods\2.2.1.1\scripts\client\gui\mods"
$IMAGE_DEST = "C:\Program Files (x86)\World_of_Tanks_NA\res_mods\2.2.1.1\gui\pademinune"

python27 -m py_compile mod_armor_pen_calculator.py
Move-Item -Force mod_armor_pen_calculator.pyc bin/

python27 -m py_compile pade_constants.py
Move-Item -Force pade_constants.pyc bin/

python27 -m py_compile pade_gui.py
Move-Item -Force pade_gui.pyc bin/

python27 -m py_compile pade_config.py
Move-Item -Force pade_config.pyc bin/


Copy-Item bin/mod_armor_pen_calculator.pyc $DEST
Copy-Item bin/pade_constants.pyc $DEST
Copy-Item bin/pade_gui.pyc $DEST
Copy-Item bin/pade_config.pyc $DEST

Copy-Item .\images\crosshair-16-green.png $IMAGE_DEST
Copy-Item .\images\crosshair-16-orange.png $IMAGE_DEST
Copy-Item .\images\crosshair-16-red.png $IMAGE_DEST


Write-Output "Compiled and copied nightly branch mod files to '$DEST'"
