pub struct SerialTerminal {
    readonly: bool
}

impl SerialTerminal {
    pub fn new(readonly: bool, serial_name: String) -> SerialTerminal{
        println!("Opened Serial Terminal");
        println!("Serial Connection to {}", serial_name);
        return SerialTerminal{
            readonly: readonly
        };
    }
}