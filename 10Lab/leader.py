import time

def processLeader(queueLeader, queuesToFollowers, queuesFromFollowers, eventStop, processNumber=3):
    primeMax = 0

    print("[Leader] Starting as leader")

    while not eventStop.is_set():
        try:
            msg = queueLeader.get(timeout=1)
            if msg[0] == "proposal":
                _, idFrom, primeProposed = msg

                
                print(f"[Leader] Received proposal {primeProposed} from Follower {idFrom}")
                votes = 1
                for q in queuesToFollowers:
                    try:
                        q.put(("voteRequest", primeProposed), timeout=1)
                    except:
                        continue 
                for q in queuesFromFollowers:
                    try:
                        response = q.get(timeout=1)
                        if response == "yes":
                            votes += 1
                    except:
                        continue 
                print(f"[Leader] Vote result: {votes}/{processNumber//2 + 1}")
                if votes > (processNumber // 2):
                    primeMax = primeProposed
                    print(f"[Leader] Prime {primeProposed} accepted by majority")
                    try:
                        with open("10Lab/primes.txt", "a") as f:
                            f.write(f"{primeProposed} - by Follower {idFrom}\n")
                            f.flush()
                    except Exception as e:
                        print(f"[Leader] Error writing to file: {e}")

        except:
            continue
        
        time.sleep(0.1)