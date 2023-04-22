# $ docker run -it --name kcc-cli -v <yourComicsDirPath>:/home/kcc/chapters wesleympg/kindle-comic-converter-cli


import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request
import subprocess
import time

def downloadPage(pageURL, pageNumber, chapterDir, chapterNumber):
    try:
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        driver.get(pageURL)

        webPage = driver.page_source
        
        links = re.findall('https:\/\/static2.mangalivre.net\/firefox.+?(?=")', webPage)

        driver.quit()

        print("Page URL " + pageURL)

        pagePath = chapterDir + "/" + str(chapterNumber).zfill(3) +  "_" + str(pageNumber).zfill(3) + ".jpg"

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(links[len(links) - 1], pagePath)
        
        print("Download da página " + str(pageNumber).zfill(3) + " feito com sucesso.")
    except:
        print("Erro Download da página " + str(pageNumber).zfill(3))

def downloadChapter(url, chapterNumber, mangaDir):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    chapterDir = mangaDir + "/" + "Chapter_" + str(chapterNumber).zfill(3)

    if(not os.path.exists(chapterDir)):
        os.mkdir(chapterDir)
        print("Criando diretório para capítulo " + str(chapterNumber).zfill(3))

    page_index = 0

    print("Chapter url " + url)
    
    page_url = "https://mangalivre.net" + url + "#" + "/!page" + str(page_index)

    driver.get(page_url)

    webPage = driver.page_source

    total_pages_element = re.findall('<em reader-total-pages="">.*<\/em>', webPage)
    total_pages = re.findall('([0-9]+)', total_pages_element[0])
    total_pages = int(total_pages[0])

    driver.quit()

    for index in range(total_pages):
        pageURL = "https://mangalivre.net" + url + "#" + "/!page" + str(index)
        print("link " + pageURL)
        downloadPage(pageURL, index, chapterDir, chapterNumber)


    return chapterDir


def fetchChapters(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)

    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    webPage = driver.page_source

    links = re.findall('(\/ler.+?(?="))', webPage)

    driver.quit()

    return links

def main():
    manga = input("Qual nome do manga ?")
    mangaURL = input("Qual o link base do manga que deseja baixar ?")
    starting_chapter = int(input('Deseja começa baixando a partir de qual capítulo ?'))

    mainDir = "Mangas"
    mangaDir = mainDir + "/" + manga

    if(not os.path.exists(mainDir)):
        os.mkdir(mainDir)
        print("Criando pasta principal")

    if(not os.path.exists(mangaDir)):
        os.mkdir(mangaDir)
        print("Criando pasta do manga")

    print("Buscando capítulos")
    chapters = fetchChapters(mangaURL)

    chapters.reverse()

    starting_chapter = 0
    for i in range(len(chapters)):
        if(i + starting_chapter >= len(chapters)):
            break
        chapterDir = downloadChapter(chapters[i+starting_chapter], i+starting_chapter, mangaDir)
        print("docker exec -it kcc-cli kcc-c2e --format=EPUB -u -s --title='" + manga + " - " + str(i+starting_chapter).zfill(3) + "' '" + chapterDir + "'")
        subprocess.call('docker exec -it kcc-cli kcc-c2e --format=EPUB -u -s --title="' + manga + ' - ' + str(i+starting_chapter).zfill(3) + '" "' + chapterDir + '"', shell=True)

if __name__ == "__main__":
    main()