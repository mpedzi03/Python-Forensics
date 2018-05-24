import hashlib

# define the alphabet as a list of strings
# separate list for each character class
lowercase = ['a','b','c','d']
uppercase = ['A','B','C','D']

numbers = ['0','1,','2','3']
special = ['!','@','#','$']

alphabet = lowercase + uppercase + numbers + special
print "length of alphabet:", len(alphabet)

# empty list of passwords
pwdsTwo = []
pwdsThree = []
pwdsFour = []

# triple-nested loop
for i in alphabet:
    for j in alphabet:
        pwdsTwo.append(i+j)
        for k in alphabet:
            pwdsThree.append(i+j+k)
            for l in alphabet:
                pwdsFour.append(i+j+k+l)

print "Generated: ", len(pwdsTwo), "passwords."
print "Generated: ", len(pwdsThree), "passwords."
print "Generated: ", len(pwdsFour), "passwords."

