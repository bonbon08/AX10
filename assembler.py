file = input("File: ")
lines = []
def getregister(reg):
    numreg = b"\x00"
    match reg:
        case "al":
            numreg = b"\x01"
        case "bh":
            numreg = b"\x02"
        case "bl":
            numreg = b"\x03"
        case "ch":
            numreg = b"\x04"
        case "cl":
            numreg = b"\x05"
        case "dh":
            numreg = b"\x06"
        case "dl":
            numreg = b"\x07"
        case "rh":
            numreg = b"\x08"
        case "rl":
            numreg = b"\x09"
    return numreg
def sp_gettypeandcontent(typ, content):
    typnum = b"\x00"
    connum = b"\x00"
    match typ:
        case "int":
            connum = int(content).to_bytes(1, byteorder="big")
        case "reg":
            typnum = b"\x02"
            connum = getregister(content)
        case "ram":
            typnum = b"\x03"
            connum = int(content).to_bytes(1, byteorder="big")
    return typnum, connum
def gettypeandcontent(typ, content):
    typnum = b"\x00"
    connum = b"\x00"
    match typ:
        case "int":
            connum = int(content).to_bytes(1, byteorder="big")
        case "reg":
            typnum = b"\x01"
            connum = getregister(content)
        case "ram":
            typnum = b"\x02"
            connum = int(content).to_bytes(1, byteorder="big")
    return typnum, connum
with open(file, "r") as data:
    cache = data.read()
tempcache = ""
for i in cache:
    if i == "\n":
        lines.append(tempcache)
        tempcache = ""
    else:
        tempcache += i
print(lines)
outfile = open("out.bin", "wb")
for line in lines:
    entrys = line.split(" ")
    match entrys[0]:
        case "stp":
            outfile.write(b"\x00")
        case "mov":
            outfile.write(b"\x01")
            outfile.write(getregister(entrys[1]))
            t1, t2 = sp_gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "add":
            outfile.write(b"\x02")
            outfile.write(getregister(entrys[1]))
            t1, t2 = gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "sub":
            outfile.write(b"\x03")
            outfile.write(getregister(entrys[1]))
            t1, t2 = gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "div":
            outfile.write(b"\x04")
            outfile.write(getregister(entrys[1]))
            t1, t2 = gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "mul":
            outfile.write(b"\x05")
            outfile.write(getregister(entrys[1]))
            t1, t2 = gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "jmp":
            outfile.write(b"\x06")
            for i in range(1, len(entrys)):
                outfile.write(int(entrys[i]).to_bytes(1, byteorder="big"))
        case "sle":
            outfile.write(b"\x07")
            outfile.write(int(entrys[1]).to_bytes(1, byteorder="big"))
        case "wtr":
            outfile.write(b"\x08")
            outfile.write(int(entrys[1]).to_bytes(1, byteorder="big"))
            t1, t2 = gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "cmp":
            outfile.write(b"\x09")
            outfile.write(getregister(entrys[1]))
            t1, t2 = gettypeandcontent(entrys[2], entrys[3])
            outfile.write(t1)
            outfile.write(t2)
        case "jie":
            outfile.write(b"\x0a")
            for i in range(1, len(entrys)):
                outfile.write(int(entrys[i]).to_bytes(1, byteorder="big"))
        case "jin":
            outfile.write(b"\x0b")
            for i in range(1, len(entrys)):
                outfile.write(int(entrys[i]).to_bytes(1, byteorder="big"))
