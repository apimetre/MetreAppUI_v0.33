# Metre_AppUI_v0.32
** Whenever you do a new release, put latest version in updater.py AND the current version in MainMetre.py

1) MainMetre.py is the installer/code launcher. **If the root directory (MetreiOS) already exists** on your device, it will look for metre_ios_install_config.json and launch the most current version of the app (from a subdirectory in MetreiOS) OR it will download the most current version of the app from GitHub, installed as a subdirectory in MetreiOS. If an older version of the app exists, the log files (for remembering the device, timezone, storage of previous data) will get copied over to the new app subdirectory. **If the MetreiOS subdirectory does not exist** it will download that root directory and make metre_ios_install_config.json (version # is hard-coded into a dictionary written in MainMetre.py). The script that "does stuff" and makes the UI is the script MetreUI.py

2) The profile (MetreiOS shortcut) shortcut.py points to the first/oldest version of MainMetre.py in the MetreiOS.

3) There were two issues causing the previous update bugs--"self.cwd" instead of "cwd" (2 instances) and try-except in install_from_github (should not have "except" bc returns "None". Update error will persist if the first/oldest version of code in MetreiOS is NOT v 0.30 or v0.31 + 

4) MetreUI.py makes the UI. Currently, as written, this version of the code expects to receive a json file (similar to the format in temp_resources). It looks for files that are located in the folder temp_resources. It processes the test by calling the script process_test.py, which does the mV rolling mean and various metadata calculations, adds the keys to the dictionary. The dietionary gets returned to MetreUI.py (the main script) and pushes it to the cloud function 'https://us-central1-metre3-1600021174892.cloudfunctions.net/metre-7500'.

5) The cloud function writes the metadata to a common log, saves the incoming (single) json file, runs the prediction, and returns the prediction to MetreUI.py

6) MetreUI.py receives the response from the cloud function, displays the result and writes it to the log.

5) If multiple files are present in temp_resources, multiple files will be uploaded.

## Updates from v0.31:

1) Added back in bokeh plotting with a change directory option in case directory is not correct
