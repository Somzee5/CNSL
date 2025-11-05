import hashlib

# Take input from user
text = input("Enter any text: ")

# Encode and calculate SHA-1 hash
sha1_hash = hashlib.sha1(text.encode()).hexdigest()

# Display result
print("SHA-1 Message Digest:", sha1_hash)