import time

class emulator():
    def __init__(self, script):
        print("AX10 emu \nv0l-bootup\n")
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
        print("Init Drive")
        with open(script, "rb") as file:
            drive = file.read()
        self.drive = []
        print("Drive entry;")
        for byte in drive:
            print(hex(byte), end=" ")
            self.drive.append(byte)
        print("\n")
    def run(self):
        try:
            while True:
                command = hex(self.drive[self.pointer])
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
                if command == "0x0":
                    raise Exception("Socket Panick\nHalted emu")
                elif command == "0x1":
                    self.pointer += 1
                    self.mov()
                elif command == "0x2":
                    self.pointer += 1
                    self.add()
                elif command == "0x3":
                    self.pointer += 1
                    self.sub()
                elif command == "0x4":
                    self.pointer += 1
                    self.div()
                elif command == "0x5":
                    self.pointer += 1
                    self.mul()
                elif command == "0x6":
                    self.pointer += 1
                    self.jmp()
                elif command == "0x7":
                    self.pointer += 1
                    self.wait()
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
                for i in range(self.pointer,len(self.drive)):
                    print(self.drive[i], end = " ")
                #self.check8bit()
        except Exception as error:
            print("Emulator Panicked, error:\n" + str(error))
    def check8bit(self):
        for i in self.Registers:
            if i > 255:
                raise Exception("Register to big")
    def wait(self):
        time.sleep(self.drive[self.pointer])
    def jmp(self):
        byte_num = self.drive[self.pointer]
        self.pointer += 1
        new_pointer = 0
        for i in range(byte_num):
            new_pointer = (new_pointer << 8) | self.drive[self.pointer]
            self.pointer += 1
        self.pointer = new_pointer - 1 
        print(f"Jumping to address: {hex(new_pointer)}")
    def mov(self):
        self.register = self.drive[self.pointer]
        self.pointer += 1
        typ = hex(self.drive[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = self.drive[self.pointer]
        elif typ == "0x1":
            pass # Charakter Map
        elif typ == "0x2":
            self.res = self.getregister()
        elif typ == "0x3":
            pass # drive address
        self.setregister()
    def add(self):
        self.register = self.drive[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.drive[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = registerentey + self.drive[self.pointer]
        elif typ == "0x1":
            self.res = registerentey + self.getregister()
        elif typ == "0x2":
            pass # drive address
        self.setregister()
    def sub(self):
        self.register = self.drive[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.drive[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = registerentey - self.drive[self.pointer]
        elif typ == "0x1":
            self.res = registerentey - self.getregister()
        elif typ == "0x2":
            pass # drive address
        self.setregister()
    def div(self):
        self.register = self.drive[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.drive[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = round(registerentey / self.drive[self.pointer])
        elif typ == "0x1":
            self.res = round(registerentey / self.getregister())
        elif typ == "0x2":
            pass # drive address
        self.setregister()
    def mul(self):
        self.register = self.drive[self.pointer]
        registerentey = self.getregister()
        self.pointer += 1
        typ = hex(self.drive[self.pointer])
        self.pointer += 1
        if typ == "0x0":
            self.res = registerentey * self.drive[self.pointer]
        elif typ == "0x1":
            self.res = registerentey * self.getregister()
        elif typ == "0x2":
            pass # drive address
        self.setregister()
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
        register = self.drive[self.pointer]
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
    def close(self):
        exit()
emu = emulator("test")
emu.run()