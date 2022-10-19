import itertools


R = list()
G = list()
B = list()

#Create Red vector
for i in range(0,256):
    R.append(int(i))

for i in reversed(range(0,256)):
    R.append(int(i))

for i in range(0,256):
    R.append(0)

#for i in range(0,256):
#    R.append(int(i))



#Create Green vector

for i in range(0,256):
    G.append(0)

for i in range(0,256):
    G.append(int(i))

for i in reversed(range(0,256)):
    G.append(int(i))

#for i in range(0,256):
#    G.append(0)

print(G)

#Create Blue vector

for i in reversed(range(0,256)):
    B.append(int(i))

for i in range(0,256):
    B.append(0)

for i in range(0,256):
    B.append(int(i))

#for i in reversed(range(0,256)):
#    B.append(int(i))


#Create Blue vector

output = list()
f = open("rgb.txt", "w", encoding="utf-8")

for i in range(len(R)):
    red = str(hex(R[i]))
    red = red[2:]
    if len(red) < 2:
        red = "0"*(2-len(red)) + red

    red = red.upper()

    green = str(hex(G[i]))
    green = green[2:]
    if len(green) < 2:
        green = "0"*(2 - len(green)) + green

    green = green.upper()

    blue = str(hex(B[i]))
    blue = blue[2:]
    if len(blue) < 2:
        blue = "0"*(2 - len(blue)) + blue
    blue = blue.upper()

    tmp = red + green + blue

    f.write("#" + tmp + "\n")


print()