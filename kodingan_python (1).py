import serial
import time

# Define serial port and baud rate
ser = serial.Serial('COM6', 9600)  # Sesuaikan dengan port serial yang digunakan

# Buat fungsi untuk mengirim data ke Arduino
def send_to_arduino(data):
    ser.write(data.encode())
    time.sleep(2)  # Tunggu 2 detik untuk memastikan Arduino menerima dan memproses data

# Program utama
if __name__ == "__main__":
    try:
        while True:
            panjangsumbux = input("Masukkan panjang sumbu X: ")
            panjangsumbuy = input("Masukkan panjang sumbu Y: ")
            inputX = input("Masukkan nilai input X (1 untuk on, 0 untuk off): ")
            inputY = input("Masukkan nilai input Y (1 untuk on, 0 untuk off): ")

            # Kirim data ke Arduino
            send_to_arduino(f"{panjangsumbux} {panjangsumbuy} {inputX} {inputY}\n")

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    finally:
        ser.close()
