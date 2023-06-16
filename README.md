This is the code for the localization simulator. The simulator can work both in Windows and Linux.

In Windows: 
- Install the VcXsrv Windows X Server (you can download it from here: https://sourceforge.net/projects/vcxsrv/). While installing, go with all the default settings, 
but do note to check “Disable access control”.
- Launch the x server. Try looking for xlaunch.exe at the default install location “C:\Program Files\VcXsrv\xlaunch.exe”
- Download the win_start.bat file from GitLab.
- Run the win_start.bat
- In case you wish to connect to the broker remotely using VPN, you can do this before clicking the send to broker button of the GUI.

In Linux:
- Install "x11-xserver-utils" Package by running this command: sudo apt-get install x11-xserver-utils.
- Download the lin_start.sh file from GitLab.
- Run lin_start.sh file. (You may need to make it executable first using the command: chmod +x lin_start.sh)
- In case you wish to connect to the broker remotely using VPN, you can do this before clicking the send to broker button of the GUI.

If you don't want to use Docker:

- Install all the requirements with the command: pip install -r requirements.txt
- Run the file print_path.py
