import os
import urllib.request
import time
import subprocess
import re

def downloadPage(pageNumber, chapter, currentChapter):
    url = "https://cdn.mangayabu.top/mangas/tonikaku-kawaii/capitulo-"+ str(currentChapter).zfill(2) + "/" + str(pageNumber).zfill(2) + ".jpg"

    fullPath = chapter + "/" + chapter + "_" + str(pageNumber).zfill(2) + ".jpg"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(url, fullPath)

    print("Download da página " + str(pageNumber).zfill(2) + " do capítulo " + currentChapter.zfill(2) + " feito com sucesso.")

def main():
    subprocess.call('docker exec -it kcc-cli kcc-c2e --format=EPUB -u -s --title="Shingeki no Kyojin - 02" "Mangas/Shingeki no Kyojin/Chapter_02"', shell=True)
if __name__ == "__main__":
    main()
