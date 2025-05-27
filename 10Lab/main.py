import multiprocessing
import time
import random
import signal
import sys
import leader
import followerBasic
import followerMIillerRabin


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

    # Leader
    leaderProcess = multiprocessing.Process(
        target=leader.processLeader,
        args=(queueLeader,
              [queueToFollower1, queueToFollower2],
              [queueFromFollower1, queueFromFollower2],
              eventStop,
              3)
    )

    follower1 = multiprocessing.Process(
        target=followerBasic.processFollower,
        args=(1, queueLeader, queueToFollower1, queueFromFollower1, eventStop)
    )

    follower2 = multiprocessing.Process(
        target=followerMIillerRabin.processFollower,
        args=(2, queueLeader, queueToFollower2, queueFromFollower2, eventStop)
    )

    leaderProcess.start()
    follower1.start()
    follower2.start()

    leaderProcess.join()
    follower1.join()
    follower2.join()