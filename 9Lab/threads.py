from PIL import Image
import numpy as np
import time
import sys
import threading

def processNegative(imageArray, rowStart, rowEnd):
    imageArray[rowStart:rowEnd] = 255 - imageArray[rowStart:rowEnd]

def processImage(imageArray, threadNumber):
    height = imageArray.shape[0]
    chunkSize = height // threadNumber
    threads = []

    for i in range(threadNumber):
        rowStart = i* chunkSize
        rowEnd = (i+1) * chunkSize if i != threadNumber -1 else height

        thread = threading.Thread(
            target=processNegative,
            args=(imageArray,rowStart,rowEnd),
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return imageArray

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Uzycie: py main.py <PLIK_OTWIERANY> <PLIK_DOCELOWY> <LICZBA_PROCESÓW>")
        sys.exit(1)

    fileInput = sys.argv[1] 
    fileOutput = sys.argv[2]
    processNumber = int(sys.argv[3])

    print(f"[Info] Wczytywanie obrazu z {fileInput}")
    image = Image.open(fileInput).convert("RGB")
    imageArray = np.array(image)

    print("[Info] Rozpoczynam przetwarzanie...")
    timeStart = time.time()

    
    negativeArray = processImage(imageArray, processNumber)
     
    timeEnd = time.time()
    timeDuration = timeEnd - timeStart
    print(f"[Sukces] Przetwarzanie zakończone w {timeDuration:.2f} sekundy")

    imageResult = Image.fromarray(negativeArray.astype(np.uint8))
    imageResult.save(fileOutput)
    print(f"[Info] Zapisano wynik do {fileOutput}")