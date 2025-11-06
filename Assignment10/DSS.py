# DSS using DSA

from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import utils

# Step 1: Generate DSA keys
private_key = dsa.generate_private_key(key_size=2048)
public_key = private_key.public_key()

# Step 2: Message to sign
message = b"Digital Signature Standard Demo"

# Step 3: Sign the message using SHA-256
signature = private_key.sign(
    message,
    hashes.SHA256()
)

print("Message:", message.decode())
print("Signature (hex):", signature.hex())

# Step 4: Verify the signature
try:
    public_key.verify(
        signature,
        message,
        hashes.SHA256()
    )
    print("✅ Signature is valid and verified!")
except:
    print("❌ Signature verification failed.")
