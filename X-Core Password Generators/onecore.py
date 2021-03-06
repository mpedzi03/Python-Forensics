# Single Core Password Table Generator
# import standard libraries

import hashlib  #hashing the results
import time      #timing the operation
import itertools #creating controlled combinations

#
# Create a list of lower case, upper case, numbers
# and special characters to include in the password table
#
lowerCase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
upperCase = ['G', 'H', 'I', 'J', 'K', 'L']
numbers = ['0', '1', '2', '3']
special = ['!', '@', '#', '$']

# combine to create a final list
allCharacters = []
allCharacters = lowerCase + upperCase + numbers + special

#Define Directory Path for the password file
DIR = 'C:\\PW\\'

#Define a hypothetical SALT value
SALT = "&45Bvx9"

#Define the allowable range of password length
PW_LOW = 2
PW_HIGH = 6

# Mark the start time
startTime = time.time()

# Create an empty list to hold the final passwords
pwList = []

# Create a loop to include all passwords
# within the allowable range

for r in range(PW_LOW, PW_HIGH):
    # Apply the standard libary interator
    # The product interator will generate the cartesian product
    # for allCharacters repeating for the range of
    # PW_LOW to PW_HIGH
    for s in itertools.product(allCharacters, repeat = r):
        # append each generated password to the
        # final list
        pwList.append(''.join(s))
    # For each password in the list generate
    # generate a file containing the
    # hash, password pairs
    # one per line
try:
    # Open the output file
    fp = open(DIR+'all','w')

    # process each generated password

    for pw in pwList:
        # Perform hashing of the password
        md5Hash =hashlib.md5()
        md5Hash.update(SALT+pw)
        md5Digest = md5Hash.hexdigest()
        # Write the hash, password pair to the file
        fp.write(md5Digest+' '+pw + '\n')
        del md5Hash
except:
    print 'File Processing Error'
    fp.close()

# Now create a dictionary to hold the
# Hash, password pairs for easy lookup

pwDict = {}

try:
    # Open each of the output file
    fp = open(DIR+'all', 'r')
    # Process each line in the file which
    # contains key, value pairs
    for line in fp:
        # extract the key value pairs
        # and update the dictionary
        pairs = line.split( )
        pwDict.update({pairs[0]: pairs[1]})
    fp.close()
except:
    print 'File Handling Error'
    fp.close()

# When complete caculate the elapsed time
elapsedTime = time.time() - startTime
print 'Elapsed Time: ', elapsedTime
print 'Passwords Generated: ', len(pwDict)
print

# print out a few of the dictionary entries
# as an example

cnt = 0
for key, value in (pwDict.items()):
    print key, value
    cnt += 1
    if cnt >10:
        break;
print

# Demonstrate the use of the Dictionary to Lookup a password using a known hash
# Lookup a Hash Value
pw = pwDict.get('c6f1d6b1d33bcc787c2385c19c29c208')
print 'Hash Value Tested = c6f1d6b1d33bcc787c2385c19c29c208'
print 'Associated Password = ' + pw
