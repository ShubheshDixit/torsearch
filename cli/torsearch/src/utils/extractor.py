import time
from bs4 import BeautifulSoup
from .browser import get_browser
from selenium.webdriver.common.by import By
import typer


def progressBar(iterable, prefix='Searching: ', suffix='', decimals=1, length=30, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function

    def printProgressBar(iteration):
        if total > 0:
            percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                            (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            typer.secho(
                f'\r{prefix} |{bar}| {percent}% {suffix} [{iteration}/{total}]{printEnd}', nl=False, fg="magenta")
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete 
    print()


class Extractor:
    @staticmethod
    def extract_piratebay(query, page=1):
        temp_list = []
        base = 'https://proxyninja.org/'
        browser = get_browser()
        browser.get(base)
        for i in progressBar(range(page)):
            # search_url = f'https://pbays.pw/s/?q={query.replace(" ", "+")}&page={i+1}&orderby=0'
            search_url = f'https://tpb.proxyninja.org/search.php?q={query}&all=on&search=Pirate+Search&page={i}&orderby='
            time.sleep(1)
            try:
                browser.get(search_url)
            except:
                _ = input("Reload and type done: ")
                browser.get(search_url)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')

            for li in progressBar(soup.findAll('li', {'id': 'st'})):
                name = li.find('span', {'class': 'item-title'}).find('a').text
                magnetURL = li.find(
                    'span', {'class': 'item-icons'}).find('a')['href']
                size = li.find('span', {'class': 'item-size'}).text
                det = {
                    'name': name + ' • ' + size,
                    'magnetURL': magnetURL
                }
                temp_list.append(det)
        browser.quit()
        return temp_list

    @staticmethod
    def extract_kickass(query, page=1):
        temp_list = []
        base = 'https://proxyninja.org/'
        base_url = 'https://kickasstorrents.proxyninja.org'
        browser = get_browser()
        browser.get(base)
        for page in progressBar(range(1, page+1)):
            search_url = f'{base_url}/search/{query}/{page}/'
            try:
                browser.get(search_url)
            except:
                _ = input("Reload and type done: ")
                browser.get(search_url)
            html = browser.page_source
            time.sleep(0.5)
            soup = BeautifulSoup(html, 'lxml')
            for a in progressBar(soup.findAll('a', {'class': 'cellMainLink'})):
                try:
                    name = a.text
                    url = a['href']
                    size = a.parent.parent.findNext('td').text
                    browser.get(base_url+url)
                    time.sleep(1)
                    html = browser.page_source
                    s = BeautifulSoup(html, 'lxml')
                    for a in s.findAll('a', {'title': 'Magnet link'}):
                        magnetURL = a['href']
                        break
                    det = {
                        'name': name + ' • ' + size,
                        'magnetURL': magnetURL
                    }
                    temp_list.append(det)
                except:
                    continue
        browser.quit()
        return temp_list

    @staticmethod
    def extract_yts(query, page=1):
        temp_list = []
        base = 'https://proxyninja.org/'
        browser = get_browser()
        browser.get(base)
        for i in progressBar(range(1, page+1), prefix="Loading: "):
            if i == 1:
                search_url = f'https://yts.proxyninja.org/browse-movies/{query}/all/all/0/latest/0/all'
            else:
                search_url = f'https://yts.proxyninja.org/browse-movies/{query}/all/all/0/latest/0/all?page={i}'
            browser.get(search_url)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            if len(soup.findAll('a', {'class': 'browse-movie-link'})) > 0:
                for a in progressBar(soup.findAll('a', {'class': 'browse-movie-link'})):
                    try:
                        link = a.get('href')
                        title = a.parent.find(
                            'a', {'class': 'browse-movie-title'}).text
                        thumbURL = a.find('img').get('src')
                        time.sleep(0.5)
                        browser.get(link)
                        mv_res = browser.page_source
                        s = BeautifulSoup(mv_res, 'lxml')
                        desc = s.find('div', {'id': 'synopsis'}).find(
                            'p', {'class': 'hidden-xs'}).text
                        info = s.find('div', {'id': 'movie-info'})
                        # genre = []
                        # for tag in info.find('div', {'class': 'mvici-left'}).findAll('a', {'rel': 'category tag'}):
                        #     genre.append(tag.text)
                        # genre = info.find('div',{'class':'mvici-left'}).find('a',{'rel':'category tag'}).text
                        # duration = info.find(
                        #     'div', {'class': 'mvici-right'}).find('span', {'itemprop': 'duration'}).text
                        year = info.find('h2').text

                        # imdb_R = year.findNext('div', {'class': 'imdb_r'}).find(
                        #     'p').find('span').text

                        downURLs = []
                        # for vidURL in s.findAll('a', {'class': 'lnk-lnk'}):
                        #     if 'magnet:?xt' in vidURL['href']:
                        #         downURLs.append(vidURL['href'])
                        for modal in s.find_all('div', {'class': 'modal-torrent'}):
                            quality = modal.find(
                                'div', {'class': 'modal-quality'}).find('span').text
                            type = modal.find_all(
                                'p', {'class': 'quality-size'})[0].text
                            size = modal.find_all(
                                'p', {'class': 'quality-size'})[1].text
                            text = quality + " • " + type + " • " + size
                            url = modal.find(
                                'a', {'class': 'magnet-download download-torrent magnet'})['href']
                            downURLs.append({'text': text, 'url': url})

                        movie_det = {
                            'name': title + " • " + year,
                            'thumbURL': thumbURL,
                            'desc': desc,
                            # 'duration': duration,
                            'year': year,
                            # 'rating': imdb_R,
                            'magnetURL': downURLs,

                        }
                        temp_list.append(movie_det)
                    except Exception as e:
                        pass
            else:
                continue
        return temp_list

    @staticmethod
    def extract_yify(query, page=1):
        temp_list = []
        base = 'https://yify.pl/movies'
        browser = get_browser()
        browser.get(base)
        try:
            submit = browser.find_element(By.XPATH,
                                          "//input[@class='button-green-download2-big'][@type='submit']")
            if submit is not None:
                browser.execute_script('arguments[0].click()', submit)
                time.sleep(0.5)
        except:
            pass
        for i in progressBar(range(1, page+1), prefix="Loading: "):
            search_url = f'https://yify.pl/movies?keyword={query}&quality=&genre=&rating=0&year=0&language=&order_by=latest&page={i}'
            browser.get(search_url)
            try:
                submit = browser.find_element(By.XPATH,
                                              "//input[@class='button-green-download2-big'][@type='submit']")
                if submit is not None:
                    browser.execute_script('arguments[0].click()', submit)
                    time.sleep(0.5)
            except:
                pass
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            if len(soup.findAll('a', {'class': 'browse-movie-link'})) > 0:
                for a in progressBar(soup.findAll('a', {'class': 'browse-movie-link'})):
                    try:
                        link = a.get('href')
                        title = a.parent.find(
                            'a', {'class': 'browse-movie-title'}).text
                        thumbURL = a.find('img').get('src')
                        time.sleep(0.5)
                        browser.get(link)
                        mv_res = browser.page_source
                        s = BeautifulSoup(mv_res, 'lxml')
                        desc = s.find('div', {'id': 'synopsis'}).find(
                            'p', {'class': 'hidden-xs'}).text
                        info = s.find('div', {'id': 'movie-info'})
                        # genre = []
                        # for tag in info.find('div', {'class': 'mvici-left'}).findAll('a', {'rel': 'category tag'}):
                        #     genre.append(tag.text)
                        # genre = info.find('div',{'class':'mvici-left'}).find('a',{'rel':'category tag'}).text
                        # duration = info.find(
                        #     'div', {'class': 'mvici-right'}).find('span', {'itemprop': 'duration'}).text
                        year = info.find('h2').text

                        # imdb_R = year.findNext('div', {'class': 'imdb_r'}).find(
                        #     'p').find('span').text

                        downURLs = []
                        # for vidURL in s.findAll('a', {'class': 'lnk-lnk'}):
                        #     if 'magnet:?xt' in vidURL['href']:
                        #         downURLs.append(vidURL['href'])
                        for modal in s.find_all('div', {'class': 'modal-torrent'}):
                            quality = modal.find(
                                'div', {'class': 'modal-quality'}).find('span').text
                            type = modal.find_all(
                                'p', {'class': 'quality-size'})[0].text
                            size = modal.find_all(
                                'p', {'class': 'quality-size'})[1].text
                            text = quality + " • " + type + " • " + size
                            url = modal.find(
                                'a', {'class': 'magnet-download download-torrent magnet'})['href']
                            downURLs.append({'text': text, 'url': url})

                        movie_det = {
                            'name': title + " • " + year,
                            'thumbURL': thumbURL,
                            'desc': desc,
                            # 'duration': duration,
                            'year': year,
                            # 'rating': imdb_R,
                            'magnetURL': downURLs,

                        }
                        temp_list.append(movie_det)
                    except Exception as e:
                        pass
            else:
                continue
        return temp_list
