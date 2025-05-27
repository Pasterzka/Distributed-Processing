import multiprocessing
import time
import random
import signal
import sys
import leader
import followerBasic
import followerMIillerRabin
import followerTestFermata
import followerTestDzielnikow


eventStop = multiprocessing.Event()

def signalHandler(sig, frame):
    print("\n[Main] Ctrl+C received. Stopping...")
    eventStop.set()

signal.signal(signal.SIGINT, signalHandler)


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    queueLeader = manager.Queue()
    

    queueToFollower1 = manager.Queue()  # Leader -> Follower 1
    queueFromFollower1 = manager.Queue()  # Follower 1 -> Leader

    queueToFollower2 = manager.Queue()  # Leader -> Follower 2
    queueFromFollower2 = manager.Queue()  # Follower 2 -> Leader
    
    queueToFollower3 = manager.Queue()  # Leader -> Follower 3
    queueFromFollower3 = manager.Queue()  # Follower 3 -> Leader

    queueToFollower4 = manager.Queue()  # Leader -> Follower 4
    queueFromFollower4 = manager.Queue()  # Follower 4 -> Leader

    # Leader
    leaderProcess = multiprocessing.Process(
        target=leader.processLeader,
        args=(queueLeader,
              [queueToFollower1, queueToFollower2, queueToFollower3, queueToFollower4],
              [queueFromFollower1, queueFromFollower2, queueFromFollower3, queueFromFollower4],
              eventStop,
              4)
    )

    follower1 = multiprocessing.Process(
        target=followerBasic.processFollower,
        args=(1, queueLeader, queueToFollower1, queueFromFollower1, eventStop)
    )

    follower2 = multiprocessing.Process(
        target=followerMIillerRabin.processFollower,
        args=(2, queueLeader, queueToFollower2, queueFromFollower2, eventStop)
    )

    follower3 = multiprocessing.Process(
        target=followerTestFermata.processFollower,
        args=(3, queueLeader, queueToFollower3, queueFromFollower3, eventStop)
    )

    follower4 = multiprocessing.Process(
        target=followerTestDzielnikow.processFollower,
        args=(4, queueLeader, queueToFollower4, queueFromFollower4, eventStop)
    )

    leaderProcess.start()
    follower1.start()
    follower2.start()
    follower3.start()
    follower4.start()

    leaderProcess.join()
    follower1.join()
    follower2.join()
    follower3.join()
    follower4.join()