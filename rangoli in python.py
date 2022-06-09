import string
string.ascii_lowercase
alphabet=list(string.ascii_lowercase)
def print_rangoli(size):
    rangoli=[]
    lst=[]
    lst.append(alphabet[size-1])
    rangoli.append(lst.copy())
    for i in range(size-1):
        lst.clear()
        var=0
        for x in range(i+2):
            lst.append(alphabet[size-1-var])
            var=var+1
        var=var-1
        for x in range(i+1,0,-1):
            var=var-1
            lst.append(alphabet[size-1-var])
        rangoli.append(lst.copy())
    for i in range (size-1,0,-1):
        rangoli.append(rangoli[i-1])
    lst.clear()
    string='-'.join(rangoli[size-1])
    for i in range (2*size-1):
        lst.append('-'.join(rangoli[i]))
        print(lst[i].center(len(string),'-'))
number=int(input('size '))
print_rangoli(number)
