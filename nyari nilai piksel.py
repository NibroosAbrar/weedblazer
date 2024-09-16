import cv2

# Fungsi untuk menangani peristiwa mouse
def ambil_nilai_piksel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Saat tombol kiri mouse ditekan
        nilai_piksel = frame[y, x]  # Baca nilai piksel di lokasi (x, y)
        print("Nilai piksel di lokasi ({}, {}): {}".format(x, y, nilai_piksel))

# Buka kamera laptop
kamera = cv2.VideoCapture(0)

# Cek apakah kamera terbuka
if not kamera.isOpened():
    print("Kamera tidak dapat dibuka.")
    exit()

# Buat jendela untuk menampilkan gambar dari kamera
cv2.namedWindow("Kamera Laptop")

# Mengaitkan fungsi ambil_nilai_piksel dengan peristiwa mouse
cv2.setMouseCallback("Kamera Laptop", ambil_nilai_piksel)

# Loop utama untuk membaca gambar dari kamera
while True:
    ret, frame = kamera.read()  # Baca frame dari kamera

    if not ret:
        print("Gagal membaca frame.")
        break

    cv2.imshow("Kamera Laptop", frame)  # Tampilkan frame di jendela

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'q' untuk keluar
        break

# Tutup kamera dan jendela
kamera.release()
cv2.destroyAllWindows()
