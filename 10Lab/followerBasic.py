import random
import time


def isPrime(n):
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

def processFollower(id, queueLeader, queueFromLeader, queueToLeader, eventStop):
    numberCurrent = 0
    numberMaxFound = 0
    print(f"[Follower {id} - basic method] Starting with current number: {numberCurrent}")


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
