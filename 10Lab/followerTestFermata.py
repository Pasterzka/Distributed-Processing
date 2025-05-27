import random
import time


def isPrime(n, k=5):  # k = liczba iteracji
    if n <= 1:
        return False
    if n == 2:
        return True
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

def processFollower(id, queueLeader, queueFromLeader, queueToLeader, eventStop):
    numberCurrent = 0
    numberMaxFound = 0
    print(f"[Follower {id} - Test Fermata method] Starting with current number: {numberCurrent}")


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
