# Windows Terminal Importer (PuTTy, KiTTy and SuperPuTTy)

This script was created to help session migration from PuTTy, KiTTy and SuperPuTTy to the brand new Microsoft Windows Terminal.

Windows Terminal GitHub Repository:  https://github.com/microsoft/terminal

Windows terminal Doc: https://docs.microsoft.com/en-us/windows/terminal/

# Requirments

- System Requirments

    - Latest version of Microsoft Windows 10
    - Latest version of Microsoft Windows Terminal
    - Python3.7+ (script was developed using Python3.8, but you can run with 3.7x) for Microsoft Windows

- Dependencies, you can run the following command:

      $ pip3 - r requirements
     
# Configuration

- To use this script you must set some parameter in config.yml configuration file as per sample below:

        ---
        importer:
        output_dir: 'output' # Define the output path, default is the output folder of the script
        max_sessions: 500 # Number of sessions to search for Putty or Kitty
        username: jsnow # Set the default username for the session, if no username or if empty
        output_method: # Set type of new Windows Terminal session do you want
            shortcut: False # Will create a shortcut file for each exported session
            session: True # Will create a new session on settings.json, will appear in Windows Terminal menu
            settings_json: 'AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json'
        icons: # you can add more icons for your session, but you're able to select only one...
            ssh: 'icons\ssh.ico'
            telnet: 'icons\telnet.ico'
            database: 'icons\database.ico'
            cloud: 'icons\cloud.ico'
            linux: 'icons\linux.ico'
            windows: 'icons\windows.ico'
            router: 'icons\router.ico'
            switch: 'icons\switch.ico'
        source: # Change chose the source and set True on enabled parameter, you can set multiples
            putty: 
            enabled: True
            kitty: 
            enabled: False
            super_putty:
            enabled: False
            input_file: 'all_sessions.xml' # Change for your SuperPutty exported sessions XML file

# How to run

- Check requirements
- Download this repo
- Configure config.yml with the corret parameters for your setup
- run the following:
           
        $ python main.py
