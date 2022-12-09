[![TorSearch](cli/assets/torsearch_header_big.png)](https://github.com/ShubheshDixit/torsearch)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

# torsearch

A tool designed to help in finding torrent files on the internet gracefully. Can also download files when coupled with any torrent client like qBittorrent.

## Build Using Pyinstaller

```bash
 $ cd cli
```

For Windows:

```bash
 $ pyinstaller --noconfirm --onefile --console --icon "./assets/torsearch_logo_192.ico" --name "tors" --add-data "./torsearch/src/tors;."  "./torsearch/src/tors/__main__.py"
```

For Linux:

```bash
 $ pyinstaller --noconfirm --onefile --console --icon "./assets/torsearch_logo_192.png" --name "tors" --add-data "./torsearch/src/tors;."  "./torsearch/src/tors/__main__.py"
```

For Mac:

```bash
 $ pyinstaller --noconfirm --onefile --console --icon "./assets/torsearch_logo_apple.icns" --name "tors" --osx-bundle-identifier 'com.torsearch.tors' --add-data "./torsearch/src/tors:." --clean "./torsearch/src/tors/__main__.py"
```

## Usage

```bash
 $ tors search [SEARCH_TERM] -s [SOURCE_NUMBER] -p [PAGE_NUMBER]
```

## Download Support

Download [qBittorrent](https://www.qbittorrent.org/download.php) client and allow remote connections (Web User Interface).

[![qBittorrent](cli/assets/qbittorrent_setings.exe.png)](https://www.qbittorrent.org/download.php)
