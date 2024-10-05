import time

class emulator():
    def __init__(self, script):
        print("AX10 emu \nv0l-bootup\n")
        print("MasterBIOS Boot-Output-Input-System v0.1")
        print("Init Stack")
        self.stack = []
        print("Init Registers")
        self.ah = 0
        self.al = 0
        self.bh = 0
        self.bl = 0
        self.ch = 0
        self.cl = 0
        self.dh = 0
        self.dl = 0
        self.rh = 0
        self.rl = 0
        print("Init Pointer")
        self.pointer = 0
        print("Init Ram")
        self.ram = []
        for _ in range(254):
            for _ in range(254):
                self.ram.append(0)
        print("Installed Ram: " + str(len(self.ram)) + " bytes")
        #print(self.ram)
        print("Init Cache")
        with open(script, "rb") as file:
            cache = file.read()
        print("Cache entry;")
        if len(cache) <= 255:
            for i in range(len(cache)):
                print(hex(cache[i]), end=" ")
                self.ram[i] = cache[i]
            print("\n")
        else:
            for i in range(254):
                print(hex(cache[i]), end=" ")
                self.ram[i] = cache[i]
            print("\n")
    def run(self):
        try:
            while True:
                command = hex(self.ram[self.pointer])
                print("Command: " + str(command))
                print("AH: " + str(self.ah))
                print("AL: " + str(self.al))
                print("BH: " + str(self.bh))
                print("BL: " + str(self.bl))
                print("CH: " + str(self.ch))
                print("CL: " + str(self.cl))
                print("DH: " + str(self.dh))
                print("DL: " + str(self.dl))
                print("RH: " + str(self.rh))
                print("RL: " + str(self.rl))
                match command:
                    case "0x0":
                        raise Exception("Socket Panick\nHalted emu")
                    case "0x1":
                        self.pointer += 1
                        self.mov()
                    case "0x2":
                        self.pointer += 1
                        self.add()
                    case "0x3":
                        self.pointer += 1
                        self.sub()
                    case "0x4":
                        self.pointer += 1
                        self.div()
                    case "0x5":
                        self.pointer += 1
                        self.mul()
                    case "0x6":
                        self.pointer += 1
                        self.jmp()
                    case "0x7":
                        self.pointer += 1
                        self.wait()
                    case "0x8":
                        self.pointer += 1
                        self.writeram()
                    case "0x9":
                        self.pointer += 1
                        self.cmp()
                    case "0xa":
                        self.pointer += 1
                        self.jie()
                    case "0xb":
                        self.pointer += 1
                        self.jin()
                self.pointer += 1
                self.Registers = [
                    self.ah,
                    self.al,
                    self.bh,
                    self.bl,
                    self.ch,
                    self.cl,
                    self.dh,
                    self.dl,
                    self.rh,
                    self.rl
                ]
                for i in range(self.pointer,254):
                    print(self.ram[i], end = " ")
                self.check8bit()
        except Exception as error:
            print("Emulator Panicked, error:\n" + str(error))
    def check8bit(self):
        for i in range(len(self.Registers)):
            while self.Registers[i] > 255:
                self.Registers[i] -= 255
                match i:
                    case 0 :
                        self.ah -= 128
                    case 1 :
                        self.al -= 128
                    case 2 :
                        self.bh -= 128
                    case 3 :
                        self.bl -= 128
                    case 4 :
                        self.ch -= 128
                    case 5 :
                        self.cl -= 128
                    case 6 :
                        self.dh -= 128
                    case 7 :
                        self.dl -= 128
                    case 8 :
                        self.rh -= 128
                    case 9 :
                        self.rl -= 128
            while self.Registers[i] < 0:
                self.Registers[i] -= self.Registers[i]*2
                match i:
                    case 0 :
                        self.ah -= self.ah*2
                    case 1 :
                        self.al -= self.al*2
                    case 2 :
                        self.bh -= self.bh*2
                    case 3 :
                        self.bl -= self.bl*2
                    case 4 :
                        self.ch -= self.ch*2
                    case 5 :
                        self.cl -= self.cl*2
                    case 6 :
                        self.dh -= self.dh*2
                    case 7 :
                        self.dl -= self.dl*2
                    case 8 :
                        self.rh -= self.rh*2
                    case 9 :
                        self.rl -= self.rl*2
    def wait(self):
        time.sleep(self.ram[self.pointer])
    def jmp(self):
        byte_num = self.ram[self.pointer]
        self.pointer += 1
        new_pointer = 0
        for i in range(byte_num):
            new_pointer = (new_pointer << 8) | self.ram[self.pointer]
            self.pointer += 1
        self.pointer = new_pointer - 1 
        print(f"Jumping to address: {hex(new_pointer)}")
    def mov(self):
        self.register = self.ram[self.pointer]
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = self.ram[self.pointer]
        elif typ == "0x1":
            pass # Charakter Map
        elif typ == "0x2":
            self.res = self.getregister()
        elif typ == "0x3":
            self.res = self.getramentry()
        self.setregister()
    def add(self):
        self.register = self.ram[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = registerentey + self.ram[self.pointer]
        elif typ == "0x1":
            self.res = registerentey + self.getregister()
        elif typ == "0x2":
            self.res = registerentey + self.getramentry()
        self.setregister()
    def sub(self):
        self.register = self.ram[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = registerentey - self.ram[self.pointer]
        elif typ == "0x1":
            self.res = registerentey - self.getregister()
        elif typ == "0x2":
            self.res = registerentey - self.getramentry()
        self.setregister()
    def div(self):
        self.register = self.ram[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = round(registerentey / self.ram[self.pointer])
        elif typ == "0x1":
            self.res = round(registerentey / self.getregister())
        elif typ == "0x2":
            self.res = round(registerentey / self.getramentry())
        self.setregister()
    def mul(self):
        self.register = self.ram[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = registerentey * self.ram[self.pointer]
        elif typ == "0x1":
            self.res = registerentey * self.getregister()
        elif typ == "0x2":
            self.res = registerentey * self.getramentry()
        self.setregister()
    def writeram(self):
        address = self.ram[self.pointer]
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = self.ram[self.pointer]
        elif typ == "0x1":
            self.res = self.getregister()
        elif typ == "0x2":
            self.res = self.getramentry()
        self.ram[address] = self.res
    def cmp(self):
        entry = self.getregister()
        self.pointer += 1
        typ = hex(self.ram[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = self.ram[self.pointer]
        elif typ == "0x1":
            self.res = self.getregister()
        elif typ == "0x2":
            self.res = self.getramentry()
        if entry == self.res:
            self.rh = 1
        else:
            self.rh = 0
    def jie(self):
        # JIE -> Jump if equal
        if self.rh == 1:
            self.jmp()
        else:
            self.pointer += 1
    def jin(self):
        # JIN -> Jump if not equal
        if self.rh == 0:
            self.jmp() 
        else:
            self.pointer += 1
    def setregister(self):
        if self.register == 0:
            self.ah = self.res
        elif self.register == 1:
            self.al = self.res
        elif self.register == 2:
            self.bh = self.res
        elif self.register == 3:
            self.bl = self.res
        elif self.register == 4:
            self.ch = self.res
        elif self.register == 5:
            self.cl = self.res
        elif self.register == 6:
            self.dh = self.res
        elif self.register == 7:
            self.dl = self.res
        elif self.register == 8:
            self.rh = self.res
        elif self.register == 9:
            self.rl = self.res
    def getregister(self):
        register = self.ram[self.pointer]
        if register == 0:
            return self.ah
        elif register == 1:
            return self.al
        elif register == 2:
            return self.bh
        elif register == 3:
            return self.bl
        elif register == 4:
            return self.ch
        elif register == 5:
            return self.cl
        elif register == 6:
            return self.dh 
        elif register == 7:
            return self.dl 
        elif register == 8:
            return self.rh 
        elif register == 9:
            return self.rl 
    def getramentry(self):
        return self.ram[self.ram[self.pointer]]
    def close(self):
        exit()
emu = emulator("test")
emu.run()