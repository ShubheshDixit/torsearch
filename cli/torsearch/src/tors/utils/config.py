import sys
import typer
import yaml
import os

def load_config():
    # Load the config yaml file
    try:
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as exc:
        print(exc)
    except FileNotFoundError:
        create_config_file()
        typer.secho(f"🔥[ERROR] Could not find config.yaml file",
                    fg=typer.colors.RED)
        # typer.Exit(1)
        return load_config()


def create_config_file(path: str = None):
    try:
        with open("config.yaml", 'w') as f:
            default_download_path = path if path is not None else get_default_download_path()
            yaml.dump({
                'default_download_path': default_download_path}, f)
    except yaml.YAMLError as exc:
        print(exc)
    except Exception as e:
        typer.secho(f"🔥[ERROR] Could not create config.yaml file",
                    fg=typer.colors.RED)
        typer.Exit(1)


def get_default_download_path():
    if sys.platform == 'win32':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')
