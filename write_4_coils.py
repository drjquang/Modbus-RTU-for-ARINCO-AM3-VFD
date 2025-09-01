try:
    # pymodbus >= 3.0
    from pymodbus.client import ModbusSerialClient
except ImportError:
    # pymodbus 2.x
    from pymodbus.client.sync import ModbusSerialClient


def write_coil(client, coil_address, value):
    """Write a single coil and report result"""
    result = client.write_coil(address=coil_address, value=value, unit=1)  # slave id = 1
    if result.isError():
        print(f"⚠️ Error writing coil {coil_address}")
    else:
        state = "ON" if value else "OFF"
        print(f"✔ Coil {coil_address} set to {state}")


def main():
    client = ModbusSerialClient(
        method="rtu",
        port="COM5",
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=1
    )

    if not client.connect():
        print("❌ Failed to connect to Modbus device on COM5")
        return

    print("✅ Connected to Modbus device on COM5")

    menu = """
=== Coil Control Menu ===
1. Coil 0 ON     | 2. Coil 0 OFF
3. Coil 1 ON     | 4. Coil 1 OFF
5. Coil 2 ON     | 6. Coil 2 OFF
7. Coil 3 ON     | 8. Coil 3 OFF
q. Quit
"""
    while True:
        print(menu)
        choice = input("Your choice: ").strip().lower()

        if choice == "q":
            print("Exiting...")
            break
        elif choice == "1":
            write_coil(client, 0, True)
        elif choice == "2":
            write_coil(client, 0, False)
        elif choice == "3":
            write_coil(client, 1, True)
        elif choice == "4":
            write_coil(client, 1, False)
        elif choice == "5":
            write_coil(client, 2, True)
        elif choice == "6":
            write_coil(client, 2, False)
        elif choice == "7":
            write_coil(client, 3, True)
        elif choice == "8":
            write_coil(client, 3, False)
        else:
            print("Invalid choice. Please select from the menu.")

    client.close()


if __name__ == "__main__":
    main()
