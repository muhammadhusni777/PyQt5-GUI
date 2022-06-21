
class siswa():
    def __init__(self, nama, usia, alamat):
        self.nama = nama
        self.usia = usia
        self.alamat = alamat

identitas = siswa('husni', 24,"parongpong")

print(identitas.nama)
print(identitas.usia)
print(identitas.alamat)