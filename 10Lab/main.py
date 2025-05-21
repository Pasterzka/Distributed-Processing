import multiprocessing
import time
import random
import signal
import sys

def isPrime_Basic(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def processLeader(queueLeader, queueResponse, eventStop, processNumber):
    prmieMax = 0

    # Program działa do momentu CTRL+C
    while eventStop.is_set():

        # Czekanie na wiadomość
        try:
            msg = queueLeader.get(timeout=1)
        except:
            continue
        
        # Follower znalazł liczbę pierwszą
        if msg[0] == "propsal":
            _, idFrom, primeProposed = msg

        # Sprawdzenie czy nowa liczba pierwsza jest największa
        if primeProposed > prmieMax:
             print(f"[Leader] Received proposal {primeProposed} from Follower {idFrom}")

        # Wysłanie oraz czekanie na odpowiedzi od Followerów
        votes = 1
        for q in queueResponse:
            q.put(("voteRequest", primeProposed))

        for q in queueResponse:
            try:
                respone = q.get(timeout=1)
                if respone == "yes":
                    vote += 1
            except: 
                continue
        

        if votes > (int(processNumber/2)+1):
            prmieMax = primeProposed
            print(f"[Leader] Prime {primeProposed} accepted by majority. Writing to file.")

            with open("primes.txt", "a") as f:
                f.write(str(primeProposed) + f" - by Follower {idFrom}\n")
