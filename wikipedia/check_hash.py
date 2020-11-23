# https://dumps.wikimedia.org/mkwiki/20201101/mkwiki-20201101-sha1sums.txt

# importing the hashlib module
import hashlib
import os

def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    if not os.path.isabs(filename):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, filename)

    if not os.path.exists(filename):
        print("File doesn't exist.")
        return

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()

def checkAgainst(hash1, hash2):
    if hash1 == hash2:
        print("The hash checks out!")
    else:
        print("Something is wrong, the hashes are NOT the same!")

def checkTwoHashes(file1, file2):
    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    print("Hash 1: ", hash1)
    print("Hash 2: ", hash2)
    checkAgainst(hash1, hash2)

hash = hash_file("./RAW/mkwiki-20201101-pages-meta-current.xml.bz2")
print("Hash: ", hash)
checkAgainst("6b52c17b2fb069fbd4bced7db8cc09a3b8fcdf66", hash)