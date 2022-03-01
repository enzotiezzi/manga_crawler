import os
import urllib.request
import time
import subprocess
import re

def downloadPage(pageNumber, chapter, currentChapter):
    url = "https://cdn.mangayabu.top/mangas/yahari-ore-no-seishun-love-comedy-wa-machigatteiru-monologue/capitulo-"+ str(currentChapter).zfill(2) +"/" + str(pageNumber).zfill(2) + ".jpg"

    fullPath = chapter + "/" + chapter + "_" + str(pageNumber).zfill(2) + ".jpg"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(url, fullPath)

    print("Download da página " + str(pageNumber).zfill(2) + " do capítulo " + str(currentChapter).zfill(2) + " feito com sucesso.")

def main():
    currentChapter = int(input("Qual capítulo desejar baixar ? "))

    totalNumberOfPages = int(input("Quantas páginas esse capítulo tem ? "))

    chapter = "Chapter_" + str(currentChapter)

    print("Verificando se pasta do capítulo já existe.")

    if (not os.path.exists(chapter)):
        os.mkdir(chapter)
        print("Pasta " + chapter + " criada.")

    print("Iniciando download...")

    i = 0
    for i in range(totalNumberOfPages):
        downloadPage(i, chapter, currentChapter)

    print("Capítulo " + str(currentChapter).zfill(2) + " baixado com sucesso")

    print("Iniciando processo para gerar MOBI.")

    subprocess.call("docker exec -it kcc-cli kcc-c2e --format=MOBI -u -s --title='Yahari Ore no Seishun Love Comedy wa Machigatteiru Monologue " + str(currentChapter).zfill(2) + "' " + chapter, shell=True)

if __name__ == "__main__":
    main()
