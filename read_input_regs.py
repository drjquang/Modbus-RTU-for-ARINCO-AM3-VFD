import struct
import time
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.register_read_message import ReadInputRegistersRequest
from pymodbus.transaction import ModbusRtuFramer

def to_hex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)

def decode_ieee754_cdab(registers):
    """Decode 2 registers (CDAB order) into float rounded to 2 decimals."""
    raw = registers[0].to_bytes(2, "big") + registers[1].to_bytes(2, "big")
    raw = raw[2:4] + raw[0:2]   # CDAB word swap
    value = struct.unpack(">f", raw)[0]
    return round(value, 2)

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
        print("❌ Could not connect")
        return

    try:
        while True:
            request = ReadInputRegistersRequest(address=0, count=2, unit=1)

            # Build RTU TX frame (with CRC)
            framer = ModbusRtuFramer(client)
            tx_frame = framer.buildPacket(request)
            print("📤 TX (RTU frame):", to_hex(tx_frame))

            # Send and receive
            response = client.execute(request)

            if response.isError():
                print("❌ Error response:", response)
            else:
                rx_frame = framer.buildPacket(response)
                print("📥 RX (RTU frame):", to_hex(rx_frame))
                print("✅ Raw Registers:", response.registers)

                value = decode_ieee754_cdab(response.registers)
                print(f"📊 Float Value (CDAB): {value}")

            print("-" * 50)
            time.sleep(1)

    except KeyboardInterrupt:
        print("⏹️ Stopped by user.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
