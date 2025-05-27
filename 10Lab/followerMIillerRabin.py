import random
import time


def isPrime(n, k=5):
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def processFollower(id, queueLeader, queueFromLeader, queueToLeader, eventStop):
    numberCurrent = 0
    numberMaxFound = 0
    print(f"[Follower {id} - Miller Rabin method] Starting with current number: {numberCurrent}")


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
