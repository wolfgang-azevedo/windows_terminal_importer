'''
Script to import terminal Sessions from Putty, Kitty or SuperPutty to
Microsoft Windows Terminal.
'''
__author__ = "Developed by: Wolfgang Azevedo"
__email__ = "wolfgang@ildt.io"
__license__ = "GPL"
__version__ = "1.0"

import os
import yaml
import argparse
import os, winshell
import json
import uuid
from win32com.client import Dispatch
from src import putty_exporter
from src import super_putty_exporter


def export_sessions(**kwargs):

    def win_terminal_shortcut(**kwargs):
        try:
            output_path = (os.path.join(kwargs.get('dest_dir'), f'{kwargs.get("session_name")}.lnk'))
            target_cmd = f'{os.environ["USERPROFILE"]}\AppData\Local\Microsoft\WindowsApps\wt.exe'
            cmd_arguments = f'ssh.exe {kwargs.get("session")}'
            shortcut_icon = config['importer']['icons']['ssh']
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(output_path)
            shortcut.Targetpath = target_cmd
            shortcut.Arguments = cmd_arguments
            shortcut.IconLocation = shortcut_icon
            shortcut.save()
        except Exception as error:
            print(f'[WIN_TERMINAL_SHORTCUT] Please check this error...{error}')
            pass

    def win_terminal_sessions(**kwargs):
        file_settings = f'{os.environ["USERPROFILE"]}\{config["importer"]["output_method"]["settings_json"]}'
        try:
            json_file = open(file_settings)
            output = []
            for line in json_file:
                if not "//" in line:
                    output.append(line)
            json_file.close()
            json_file = open(file_settings, 'w')
            json_file.writelines(output)
            json_file.close()        

            with open(file_settings, 'r+') as json_file:
                data = json.load(json_file)

                profile = data['profiles']['list']

                update_dict = {           
                            "guid": "{"+str(uuid.uuid4())+"}",
                            "name": f'{kwargs.get("session_name")}',
                            "commandline": f'ssh {kwargs.get("session")}',
                            "useAcrylic": True,
                            "acrylicOpacity": 0.7,
                            "icon": f'{os.getcwd()}\\{config["importer"]["icons"]["router"]}',
                            "hidden": False
                            }

                profile.append(update_dict)

            with open(file_settings,'w') as f:
                json.dump(data, f, indent=4) 

        except Exception as error:
            print(f'[WIN_TERMINAL_SESSIONS] Please check this error...{error}')
            pass

    def gen_files(**kwargs):
        try:
            source_app = kwargs.get('source')
            session_name = kwargs.get("values")[0]
            hostname = kwargs.get("values")[1]
            port = kwargs.get("values")[2]
            dest_dir = config['importer']['output_dir']
            dest_dir = f'{dest_dir}\\{source_app}'

            if kwargs.get('values')[3] == '':
                username = config["importer"]["username"]
            else:
                username = kwargs.get('values')[3]

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            if config['importer']['output_method']['shortcut'] is True:
                win_terminal_shortcut(dest_dir=dest_dir, session=f'{username}@{hostname} -p {port}', session_name=session_name)
            elif config['importer']['output_method']['session'] is True:
                win_terminal_sessions(session=f'{username}@{hostname} -p {port}', session_name=session_name)
                
            print(f'Session: {kwargs.get("values")[0]}, username: {username} has been exported succesfully!')
        except OSError as error:
            print(error)

    if kwargs.get('source') == 'putty' or kwargs.get('source') == 'kitty':
        for values in putty_exporter.reg_scanner(source=kwargs.get('source_app'), sessions=config['importer']['max_sessions']):
            gen_files(values=values, source=kwargs.get('source'))

    elif kwargs.get('source') == 'super_putty':
        for values in super_putty_exporter.gen_shortcuts(input_file=config['importer']['source']['super_putty']['input_file']):
            gen_files(values=values, source=kwargs.get('source'))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default='config.yml', help="set configuration file")
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError as error:
        print(f'Configuration file not found! Please check --> {error}....')
    
    for sources in config['importer']['source']:
        if sources == 'putty' or sources == 'kitty':
            if config['importer']['source'][sources]['enabled'] is True:
                source = sources
                export_sessions(source_app=source, source=source)
        elif sources == 'super_putty':
            if config['importer']['source'][sources]['enabled'] is True:
                source = sources
                export_sessions(source=source)