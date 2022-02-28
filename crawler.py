import urllib.request

import os

def downloadPage(pageNumber, chapter):
    url = "https://cdn.mangayabu.top/mangas/yahari-ore-no-seishun-love-comedy-wa-machigatteiru-monologue/capitulo-01/" + str(pageNumber).zfill(2) + ".jpg"

    fullPath = chapter + "/" + chapter + "_" + str(pageNumber).zfill(2)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(url, fullPath)

def main():
    totalNumberOfPages = 51

    currentChapter = 1
    chapter = "Chapter_" + str(currentChapter)

    if (not os.path.exists(chapter)):
        os.mkdir(chapter)

    i = 0
    for i in range(totalNumberOfPages):
        downloadPage(i, chapter)

if __name__ == "__main__":
    main()
