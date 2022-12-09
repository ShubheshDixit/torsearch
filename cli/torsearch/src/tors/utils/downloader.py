from qbittorrent import Client
import typer
from typing import Optional

from tors.utils.config import load_config


class QBitDownloader:
    def __init__(self, host="127.0.0.1", port="8080", username="admin", password="adminadmin"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.qb = Client('http://{}:{}'.format(self.host, self.port))
        self.qb.login(self.username, self.password)
        self.old_torrents = [torrent['hash'] for torrent in self.qb.torrents()]
        self.torrents = []
        self.DOWNLOAD_PATH = self.get_download_path()  # 'E:/Downloads/Videos/'

    def get_download_path(self):
        config = load_config()
        return config['default_download_path']

    def download_magnet_link(self, magnet_uri: str):
        self.qb.download_from_link(
            magnet_uri, savepath=self.DOWNLOAD_PATH)
        for torrent in self.qb.torrents():
            if torrent['hash'] not in self.old_torrents:
                self.torrents.append(torrent['hash'])
        self.old_torrents = [torrent['hash'] for torrent in self.qb.torrents()]
        self.show_downloads()

    def show_progress_bar(self, percent: int, width: int = 20):
        """
        Display a progress bar
        """
        filled = int(width * percent / 100)
        bar = "█" * filled + "-" * (width - filled)
        typer.secho(f"[{bar}] {percent}%", fg=typer.colors.BRIGHT_MAGENTA)

    def show_downloads(self, all=False, current=False):
        print("👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇")
        for torrent in self.qb.torrents():
            if (torrent['hash'] in self.torrents or all) or (current and torrent['progress'] < 1):
                print()
                typer.secho(
                    f"Torrent name: {torrent['name']}", fg=typer.colors.BRIGHT_CYAN)
                print("Hash:", torrent["hash"])
                print("Seeds:", torrent["num_seeds"])
                print("File size:", self.get_size_format(
                    torrent["total_size"]))
                print("Download speed:", self.get_size_format(
                    torrent["dlspeed"]) + "/s")
                print(f"Progress: {torrent['progress'] * 100:.2f} %")
                if not all:
                    self.show_progress_bar(int(torrent["progress"] * 100))

    def get_size_format(self, b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"


qbit_downloader: Optional[QBitDownloader] = None


def get_qbit_downloader():
    global qbit_downloader
    if qbit_downloader is None:
        try:
            qbit_downloader = QBitDownloader()
        except Exception as e:
            typer.secho(
                f"🔥[ERROR] Could not connect to QBit Torrent: {e}", fg=typer.colors.RED)
            # print("🔥[ERROR] Could not connect to QBit")
            # input("Kindly open QBit and retry by pressing [ENTER]")
            # get_qbit_downloader()
            raise typer.Exit(1)
    return qbit_downloader
