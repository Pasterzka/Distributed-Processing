
import hashlib

tekst = "aaa"

password = hashlib.sha256(tekst.encode()).hexdigest()
print(password)