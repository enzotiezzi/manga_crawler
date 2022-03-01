import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def downloadPage(pageURL, pageNumber, chapterDir):
    print("Page URL " + pageURL)

    pagePath = chapterDir + "_" + str(pageNumber).zfill(2)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(pageURL, pagePath)
    
    print("Download da página " + str(pageNumber).zfill(2) + " feito com sucesso.")

def fetchChapters(url):
    driver.get(url)
    webPage = driver.page_source

    links = re.findall('<a href="https:\/\/mangayabu\.top\/\?p=\d+" class="btn">Ler<\/a>', webPage)

    return links

def downloadChapter(url, chapterNumber, manga, mainDir):
    chapterDir = mainDir + "/" + manga + "/" + "Chapter_" + str(chapterNumber).zfill(2)

    if(not os.path.exists(chapterDir)):
        os.mkdir(chapterDir)
        print("Criando diretório para capítulo " + str(chapterNumber).zfill(2))

    url = re.search('"https:\/\/.+" ', url).group().strip().replace('"', "")

    print("Chapter url " + url)

    driver.get(url)
    webPage = driver.page_source
    driver.quit()

    links = re.findall('<img alt="Página \d+" .+>', webPage)

    i=1
    for l in links:
        print("link " + l)
        pageURL = re.search('"https:\/\/.+.jpg" ', l).group().strip().replace('"', '')
        downloadPage(pageURL, i, chapterDir)
        i+=1

def main():
    manga = input("Qual nome do manga ?")
    mangaURL = input("Qual o link base do manga que deseja baixar ?")

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

    i = 0
    for i in range(len(chapters)):
        downloadChapter(chapters[i], i, manga, mainDir)

if __name__ == "__main__":
    main()