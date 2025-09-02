import serial
import threading

def listen_serial(port="COM8", baudrate=9600):
    try:
        ser = serial.Serial(port=port,
                            baudrate=baudrate,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1)
        print(f"✅ Listening on {port} ({baudrate}, 8N1)...")

        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # read all available bytes
                print(f"📥 Received ({len(data)} bytes): {data}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Run serial listener in background thread
    t = threading.Thread(target=listen_serial, daemon=True)
    t.start()

    # Keep main thread alive
    while True:
        cmd = input("Type 'exit' to quit: ")
        if cmd.strip().lower() == "exit":
            break
