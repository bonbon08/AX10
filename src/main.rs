use std::fs::File;
use std::io::Read;
use std::{thread, time::Duration};

struct Emulator {
    stack: Vec<u8>,
    registers: [u8; 10],
    ram: Vec<u8>,
    pointer: usize,
    rh: u8,
}

impl Emulator {
    fn new(script: &str) -> Emulator {
        println!("AX10 emu \nv0l-bootup\n");
        println!("MasterBIOS Boot-Output-Input-System v0.1");
        println!("Init Stack");

        let mut stack = Vec::new();

        println!("Init Registers");

        let registers = [0; 10];

        println!("Init Pointer");
        let pointer = 0;

        println!("Init Ram");
        let mut ram = vec![0; 254 * 254];

        println!("Installed Ram: {} bytes", ram.len());

        println!("Init Cache");
        let mut file = File::open(script).expect("File not found");
        let mut cache = Vec::new();
        file.read_to_end(&mut cache).expect("Error reading file");

        println!("Cache entry;");
        if cache.len() <= 255 {
            for i in 0..cache.len() {
                print!("{:x} ", cache[i]);
                ram[i] = cache[i];
            }
        } else {
            for i in 0..254 {
                print!("{:x} ", cache[i]);
                ram[i] = cache[i];
            }
        }
        println!("\n");

        Emulator {
            stack,
            registers,
            ram,
            pointer,
            rh: 0,
        }
    }

    fn run(&mut self) {
        loop {
            let command = self.ram[self.pointer];
            println!("Command: 0x{:x}", command);
            println!("AH: {}", self.registers[0]);
            println!("AL: {}", self.registers[1]);
            println!("BH: {}", self.registers[2]);
            println!("BL: {}", self.registers[3]);
            println!("CH: {}", self.registers[4]);
            println!("CL: {}", self.registers[5]);
            println!("DH: {}", self.registers[6]);
            println!("DL: {}", self.registers[7]);
            println!("RH: {}", self.registers[8]);
            println!("RL: {}", self.registers[9]);

            match command {
                0x0 => {
                    println!("Socket Panick\nHalted emu");
                    break;
                }
                0x1 => {
                    self.pointer += 1;
                    self.mov();
                }
                0x2 => {
                    self.pointer += 1;
                    self.add();
                }
                0x3 => {
                    self.pointer += 1;
                    self.sub();
                }
                0x4 => {
                    self.pointer += 1;
                    self.div();
                }
                0x5 => {
                    self.pointer += 1;
                    self.mul();
                }
                0x6 => {
                    self.pointer += 1;
                    self.jmp();
                }
                0x7 => {
                    self.pointer += 1;
                    self.wait();
                }
                0x8 => {
                    self.pointer += 1;
                    self.writeram();
                }
                0x9 => {
                    self.pointer += 1;
                    self.cmp();
                }
                0xA => {
                    self.pointer += 1;
                    self.jie();
                }
                0xB => {
                    self.pointer += 1;
                    self.jin();
                }
                0xC => {
                    self.pointer += 1;
                    self.pushreg();
                }
                0xD => {
                    self.pointer += 1;
                    self.pullreg();
                }
                _ => {
                    println!("Unknown command");
                }
            }
            self.pointer += 1;
        }
    }

    fn wait(&self) {
        thread::sleep(Duration::from_secs(self.ram[self.pointer] as u64));
    }

    fn jmp(&mut self) {
        let byte_num = self.ram[self.pointer] as usize;
        self.pointer += 1;
        let mut new_pointer = 0;
        for _ in 0..byte_num {
            new_pointer = (new_pointer << 8) | self.ram[self.pointer] as usize;
            self.pointer += 1;
        }
        self.pointer = new_pointer - 1;
        println!("Jumping to address: 0x{:x}", new_pointer);
    }

    fn pushreg(&mut self) {
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => self.ram[self.pointer],        
            0x1 => self.get_register(),    
            0x2 => self.get_ram_entry(),     
            _ => 0,               
        };
        println!("{}", res);
        self.stack.push(res);
    }
    fn pullreg(&mut self) {
        let register = self.ram[self.pointer] as usize;
        let res: u8  = self.stack.pop().expect("");
        println!("{}", res);
        self.set_register(register, res);
    } 

    fn mov(&mut self) {
        let register = self.ram[self.pointer] as usize;
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => self.ram[self.pointer],        
            0x2 => self.get_register(),    
            0x3 => self.get_ram_entry(),     
            _ => 0,               
        };
        self.set_register(register, res);
    }

    fn add(&mut self) {
        let register = self.ram[self.pointer] as usize;
        let register_entry = self.get_register();
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => register_entry.wrapping_add(self.ram[self.pointer]), 
            0x1 => register_entry.wrapping_add(self.get_register()),  
            0x2 => register_entry.wrapping_add(self.get_ram_entry()), 
            _ => 0,
        };

        self.set_register(register, res);
    }

    fn sub(&mut self) {
        let register = self.ram[self.pointer] as usize;
        let register_entry = self.get_register();
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => register_entry.wrapping_sub(self.ram[self.pointer]),
            0x1 => register_entry.wrapping_sub(self.get_register()),   
            0x2 => register_entry.wrapping_sub(self.get_ram_entry()),   
            _ => 0,
        };

        self.set_register(register, res);
    }

    fn div(&mut self) {
        let register = self.ram[self.pointer] as usize;
        let register_entry = self.get_register();
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => register_entry / self.ram[self.pointer], 
            0x1 => register_entry / self.get_register(),  
            0x2 => register_entry / self.get_ram_entry(),  
            _ => 0,
        };

        self.set_register(register, res);
    }
    fn get_register(&self) -> u8 {
        let register = self.ram[self.pointer] as usize;
        self.registers[register]
    }
    fn set_register(&mut self, register: usize, value: u8) {
        if register < self.registers.len() {
            self.registers[register] = value;
        }
    }
    fn get_ram_entry(&self) -> u8 {
        let address = self.ram[self.pointer] as usize;
        self.ram[address]
    }

    fn mul(&mut self) {
        let register = self.ram[self.pointer] as usize;
        let register_entry = self.get_register();
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => register_entry.wrapping_mul(self.ram[self.pointer]),
            0x1 => register_entry.wrapping_mul(self.get_register()),  
            0x2 => register_entry.wrapping_mul(self.get_ram_entry()),  
            _ => 0,
        };

        self.set_register(register, res);
    }

    fn writeram(&mut self) {
        let address = self.ram[self.pointer] as usize;
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => self.ram[self.pointer],    
            0x1 => self.get_register(),      
            0x2 => self.get_ram_entry(),       
            _ => 0,
        };
        self.ram[address] = res;
    }

    fn cmp(&mut self) {
        let entry = self.get_register();
        self.pointer += 1;
        let typ = self.ram[self.pointer];
        self.pointer += 1;
        let res = match typ {
            0x0 => self.ram[self.pointer],  
            0x1 => self.get_register(),     
            0x2 => self.get_ram_entry(),        
            _ => 0,
        };

        if entry == res {
            self.rh = 1; 
        } else {
            self.rh = 0; 
        }
    }

    fn jie(&mut self) {
        if self.rh == 1 {
            self.jmp();
        } else {
            self.pointer += 1;
        }
    }

    fn jin(&mut self) {
        if self.rh == 0 {
            self.jmp();
        } else {
            self.pointer += 1;
        }
    }
}

fn main() {
    let mut emu = Emulator::new("out.bin");
    emu.run();
}
