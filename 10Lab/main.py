import multiprocessing
import time
import random
import signal
import sys
import leader

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

def processFollower(id, queueLeader, queueResponse, eventStop):
    numberCurrent = 0
    numberMaxFound = 0

    while not eventStop.is_set():
        if not queueResponse.empty():
            msg = queueResponse.get()
            if msg[0] == "voteRequest":
                primeProposed = msg[1]
                print(f"[Follower {id}] Voting YES for {primeProposed}")
                queueResponse.put("yes")

        if isPrime_Basic(numberCurrent):
            if numberMaxFound < numberCurrent:
                numberMaxFound = numberCurrent
                queueLeader.put(("proposal", id, numberCurrent))
                print(f"[Follower {id}] Found new prime: {numberCurrent}")
                time.sleep(0.5)

        numberCurrent += random.randint(1, 10)

eventStop = multiprocessing.Event()

def signalHandler(sig, frame):
    print("\n[Main] Ctrl+C received. Stopping...")
    eventStop.set()

signal.signal(signal.SIGINT, signalHandler)


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    queueLeader = manager.Queue()
    

    # Odpowiedzi Followerów do Leadera
    queueResponse1 = manager.Queue()
    queueResponse2 = manager.Queue()

    # Leader
    leader = multiprocessing.Process(
        target=leader.processLeader,
        args=(queueLeader, [queueResponse1, queueResponse2], eventStop)
    )

    follower1 = multiprocessing.Process(
        target=processFollower,
        args=(1, queueLeader, queueResponse1, eventStop)
    )

    follower2 = multiprocessing.Process(
        target=processFollower,
        args=(2, queueLeader, queueResponse2, eventStop)
    )

    leader.start()
    follower1.start()
    follower2.start()

    leader.join()
    follower1.join()
    follower2.join()