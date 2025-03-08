use std::collections::HashMap;

pub struct SerialTerminal {
    readonly: bool,
    chars: HashMap<u8, String>, // Use String instead of str
}

impl SerialTerminal {
    pub fn new(readonly: bool, serial_name: String) -> SerialTerminal {
        println!("Opened Serial Terminal");
        println!("Serial Connection to {}", serial_name);
        
        let chars_map = HashMap::from([
            (0x00, "0".to_string()),
            (0x01, "1".to_string()),
            (0x02, "2".to_string()),
            (0x03, "3".to_string()),
            (0x04, "4".to_string()),
            (0x05, "5".to_string()),
            (0x06, "6".to_string()),
            (0x07, "7".to_string()),
            (0x08, "8".to_string()),
            (0x09, "9".to_string()),
            (0x0a, "a".to_string()),
            (0x0b, "b".to_string()),
            (0x0c, "c".to_string()),
            (0x0d, "d".to_string()),
            (0x0e, "e".to_string()),
            (0x0f, "f".to_string()),
            (0x10, "g".to_string()),
            (0x11, "h".to_string()),
            (0x12, "i".to_string()),
            (0x13, "j".to_string()),
            (0x14, "k".to_string()),
            (0x15, "l".to_string()),
            (0x16, "m".to_string()),
            (0x17, "n".to_string()),
            (0x18, "o".to_string()),
            (0x19, "p".to_string()),
            (0x1a, "q".to_string()),
            (0x1b, "r".to_string()),
            (0x1c, "s".to_string()),
            (0x1d, "t".to_string()),
            (0x1e, "u".to_string()),
            (0x1f, "v".to_string()),
            (0x20, "w".to_string()),
            (0x21, "x".to_string()),
            (0x22, "y".to_string()),
            (0x23, "z".to_string()),
            (0x24, "A".to_string()),
            (0x25, "B".to_string()),
            (0x26, "C".to_string()),
            (0x27, "D".to_string()),
            (0x28, "E".to_string()),
            (0x29, "F".to_string()),
            (0x2a, "G".to_string()),
            (0x2b, "H".to_string()),
            (0x2c, "I".to_string()),
            (0x2d, "J".to_string()),
            (0x2e, "K".to_string()),
            (0x2f, "L".to_string()),
            (0x30, "M".to_string()),
            (0x31, "N".to_string()),
            (0x32, "O".to_string()),
            (0x33, "P".to_string()),
            (0x34, "Q".to_string()),
            (0x35, "R".to_string()),
            (0x36, "S".to_string()),
            (0x37, "T".to_string()),
            (0x38, "U".to_string()),
            (0x39, "V".to_string()),
            (0x3a, "W".to_string()),
            (0x3b, "X".to_string()),
            (0x3c, "Y".to_string()),
            (0x3d, "Z".to_string()),
            (0x3e, "!".to_string()),
            (0x3f, "\"".to_string()),
            (0x40, "§".to_string()),
            (0x41, "$".to_string()),
            (0x42, "%".to_string()),
            (0x43, "&".to_string()),
            (0x44, "/".to_string()),
            (0x45, "(".to_string()),
            (0x46, ")".to_string()),
            (0x47, "=".to_string()),
            (0x48, "?".to_string()),
            (0x49, ",".to_string()),
            (0x4a, ";".to_string()),
            (0x4b, ".".to_string()),
            (0x4c, ":".to_string()),
            (0x4e, "-".to_string()),
            (0x4f, "_".to_string()),
            (0x50, "\n".to_string()),
        ]);
        
        SerialTerminal {
            readonly,
            chars: chars_map,
        }
    }

    pub fn print(&self, char_to_output: u8) {
        if let Some(mapped_char) = self.chars.get(&char_to_output) {
                print!("{}", mapped_char);
        }
    }
 }
