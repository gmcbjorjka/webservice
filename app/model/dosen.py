class Dosen:
    def __init__(self, nidn, nama, phone, alamat):
        self.nidn = nidn
        self.nama = nama
        self.phone = phone
        self.alamat = alamat

    def to_dict(self):
        return {
            "nidn": self.nidn,
            "nama": self.nama,
            "phone": self.phone,
            "alamat": self.alamat
        }
