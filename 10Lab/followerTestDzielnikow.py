import random
import time


def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def processFollower(id, queueLeader, queueFromLeader, queueToLeader, eventStop):
    numberCurrent = 0
    numberMaxFound = 0
    print(f"[Follower {id} - Division test method] Starting with current number: {numberCurrent}")


    while not eventStop.is_set():
        try:
            msg = queueFromLeader.get(timeout=0.5)
            if msg[0] == "voteRequest":
                primeProposed = msg[1]
                if primeProposed >= numberMaxFound:
                    print(f"[Follower {id}] Voting YES for {primeProposed}")
                    queueToLeader.put("yes")
                    #numberMaxFound = primeProposed
                else:
                    print(f"[Follower {id}] Voting NO for {primeProposed} (my max: {numberMaxFound})")
                    queueToLeader.put("no")
        except:
            pass

        if isPrime(numberCurrent):
            if numberMaxFound < numberCurrent:
                numberMaxFound = numberCurrent
                print(f"[Follower {id}] Found new prime: {numberCurrent}")
                try:
                    queueLeader.put(("proposal", id, numberCurrent))
                except:
                    print(f"[Follower {id}] Failed to send proposal to leader")

        numberCurrent += random.randint(1, 10)
        time.sleep(0.1)
