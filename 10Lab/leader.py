import time

def processLeader(queueLeader, queueResponse, eventStop, processNumber=3):
    primeMax = 0

    print("[Leader] Starting as leader")

    while not eventStop.is_set():
        try:
            msg = queueLeader.get(timeout=1)
        except:
            continue
        
        if msg[0] == "proposal":
            _, idFrom, primeProposed = msg

            if primeProposed > primeMax:
                print(f"[Leader] Received proposal {primeProposed} from Follower {idFrom}")

                votes = 1
                for q in queueResponse:
                    q.put(("voteRequest", primeProposed))

                for q in queueResponse:
                    try:
                        response = q.get(timeout=1)
                        if response == "yes":
                            votes += 1
                    except:
                        continue

                if votes > (processNumber // 2):
                    primeMax = primeProposed
                    print(f"[Leader] Prime {primeProposed} accepted by majority. Writing to file.")
                    with open("10Lab/primes.txt", "a") as f:
                        f.write(f"{primeProposed} - by Follower {idFrom}\n")

        time.sleep(0.1) 
