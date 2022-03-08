import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request
import subprocess


def downloadPage(pageURL, pageNumber, chapterDir, chapterNumber):
    print("Page URL " + pageURL)

    pagePath = chapterDir + "/" + str(chapterNumber).zfill(2) +  "_" + str(pageNumber).zfill(2) + ".jpg"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(pageURL, pagePath)
    
    print("Download da página " + str(pageNumber).zfill(2) + " feito com sucesso.")

def fetchChapters(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)
    webPage = driver.page_source
    driver.quit()

    links = re.findall('<a href="https:\/\/mangayabu\.top\/\?p=\d+" class="btn">Ler<\/a>', webPage)

    return links

def downloadChapter(url, chapterNumber, mangaDir):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    chapterDir = mangaDir + "/" + "Chapter_" + str(chapterNumber).zfill(2)

    if(not os.path.exists(chapterDir)):
        os.mkdir(chapterDir)
        print("Criando diretório para capítulo " + str(chapterNumber).zfill(2))

    url = re.search('"https:\/\/.+" ', url).group().strip().replace('"', "")

    print("Chapter url " + url)

    driver.get(url)
    webPage = driver.page_source
    driver.quit()

    links = re.findall('data-src=".+?"', webPage)

    i=1
    for l in links:
        print("link " + l)
        pageURL = l.replace("data-src=", "").replace('"', '')
        downloadPage(pageURL, i, chapterDir, chapterNumber)
        i+=1

    return chapterDir

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

    chapters.reverse()

    i = 0
    for i in range(len(chapters)):
        chapterDir = downloadChapter(chapters[i], i, mangaDir)
        print("docker exec -it kcc-cli kcc-c2e --format=MOBI -u -s --title='" + manga + " - " + str(i).zfill(2) + "' '" + chapterDir + "'")
        subprocess.call("docker exec -it kcc-cli kcc-c2e --format=MOBI -u -s --title='" + manga + " - " + str(i).zfill(2) + "' '" + chapterDir + "'", shell=True)

if __name__ == "__main__":
    main()