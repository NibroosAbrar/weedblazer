import cv2

# Fungsi untuk menampilkan teks pada gambar
def display_text(image, text, position):
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# Baca gambar dari kamera
cap = cv2.VideoCapture(0)

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()

    # Periksa apakah gambar berhasil dibaca
    if not ret:
        print("Gagal membaca gambar dari kamera")
        break

    # Ambil dimensi gambar
    height, width, _ = frame.shape

    # Hitung total piksel
    total_pixels = height * width

    # Tampilkan nilai piksel pada gambar
    display_text(frame, f"Panjang: {width} px", (10, 30))
    display_text(frame, f"Lebar: {height} px", (10, 60))
    display_text(frame, f"Total Piksel: {total_pixels}", (10, 90))

    # Tampilkan gambar pada layar kamera
    cv2.imshow('Camera', frame)

    # Hentikan loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Hentikan penggunaan kamera dan tutup jendela kamera
cap.release()
cv2.destroyAllWindows()
