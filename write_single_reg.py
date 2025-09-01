from pymodbus.client.sync import ModbusSerialClient
from pymodbus.register_write_message import WriteSingleRegisterRequest
from pymodbus.transaction import ModbusRtuFramer

def to_hex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)

def main():
    client = ModbusSerialClient(
        method='rtu',
        port='COM5',
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=2
    )

    if not client.connect():
        print("❌ Could not connect to Modbus device.")
        return

    framer = ModbusRtuFramer(client)

    try:
        while True:
            print("\n=== Power Meter SELECT MFM384 ===")
            print("Enter a number (0–4) to write into holding register 1")
            print("Enter q to quit")
            choice = input("Your choice: ").strip()

            if choice.lower() == "q":
                print("⏹️ Exiting program.")
                break

            if choice in ["0", "1", "2", "3", "4"]:
                value = int(choice)
                request = WriteSingleRegisterRequest(address=1, value=value, unit=1)

                # Build TX frame
                tx_frame = framer.buildPacket(request)
                print("📤 TX (RTU frame):", to_hex(tx_frame))

                response = client.execute(request)

                if response.isError():
                    print("❌ Error response:", response)
                else:
                    rx_frame = framer.buildPacket(response)
                    print("📥 RX (RTU frame):", to_hex(rx_frame))
                    print(f"✅ Wrote {value} to register 1")

            else:
                print("⚠️ Invalid input. Please enter 0–4 or q.")

    finally:
        client.close()

if __name__ == "__main__":
    main()
