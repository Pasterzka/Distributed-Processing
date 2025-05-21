import asyncio
import hashlib
import itertools
import sys
from datetime import datetime

# Zbiór znaków do generowania haseł
CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

async def crack_password(start_idx, end_idx, target_hash, length):
    """Asynchroniczna funkcja do łamania hasła w określonym zakresie znaków."""
    chars_range = CHARACTERS[start_idx:end_idx]
    
    print(f"Sprawdzanie zakresu: '{chars_range}'")
    
    for prefix in chars_range:
        for combo in itertools.product(CHARACTERS, repeat=length - len(prefix)):
            candidate = prefix + ''.join(combo)
            h = hashlib.sha256(candidate.encode()).hexdigest()
            if h == target_hash:

                print(f'Password found: {candidate}')
                return candidate
    
    return None

async def main():
    if len(sys.argv) != 3:
        print("Użycie: python3 cpu_crack.py <HASŁO_SHA256> <DLUGOŚĆ_HASŁA>")
        return

    target_hash = sys.argv[1]
    length = int(sys.argv[2])
    
    print(f"Rozpoczynanie łamania hasła SHA256: {target_hash}")
    print(f"Długość hasła: {length}")
    print(f"Używany zestaw znaków: {CHARACTERS}")
    
    start_time = datetime.now()
    
    # Podział pracy na 8 wątków (zakresy znaków)
    chunk_size = len(CHARACTERS) // 8
    tasks = []
    
    for i in range(8):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < 7 else len(CHARACTERS)
        
        print(f"Wątek {i+1}: generowanie kombinacji od indeksu {start_idx} do {end_idx-1}")
        task = asyncio.create_task(crack_password(start_idx, end_idx, target_hash, length))
        tasks.append(task)
    
    # Czekaj na pierwszy wynik
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    # Anuluj pozostałe zadania jeśli znaleziono hasło
    for task in pending:
        task.cancel()
    
    result = None
    for task in done:
        result = task.result()
        if result:
            break
    
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    
    if result:
        print(f"\nZnaleziono hasło: {result}")
    else:
        print("\nNie znaleziono pasującego hasła.")
    
    print(f"Czas łamania: {elapsed_time.total_seconds():.2f} sekund")

if __name__ == "__main__":
    asyncio.run(main())
