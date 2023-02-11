def parseWheel(inpt):
    n = inpt.split(" ")
    g = [12, 14, 14, 12]
    b = []

    outputString = ""

    i = 0
    i2 = 0
    j = 0
    for word in n: #Split words into appropriately sized bits
        outputString += word + " "
        i += len(word) + 1
        if j < len(n) - 1:
            if g[i2] < i + len(n[j + 1]):
                i2 += 1
                if i2 == 4:
                    break
                i = 0
                b.append(outputString[:-1])
                outputString = ""
        j += 1

    b.append(outputString[:-1])

    if len(b) == 1 or len(b) == 2: #Adjust bits to be centered vertically
        b.insert(0, "")

    largestInd = -1
    largest = -1

    for string in b: #Yes I know this is really lazy code but it works
        if len(string) > largest:
            largest = len(string)
            largestInd = b.index(string)

    offsets = {14:0, 13:0, 12:1, 11:1, 10:2, 9:2, 8:3, 7:3, 6:4, 5:4, 4:5, 3:5, 2:6, 1:6, 0:0}

    if len(b) > 0:
        b[0] = (" " * (offsets[largest] - 1)) + b[0]
    if len(b) > 1:
        b[1] = (" " * offsets[largest]) + b[1]
    if len(b) > 2:
        b[2] = (" " * offsets[largest]) + b[2]
    if len(b) > 3:
        b[3] = (" " * (offsets[largest] - 1)) + b[3]

    #print(b)

    outputString = ""
    for string in b:
        outputString += string + "/"

    return outputString
