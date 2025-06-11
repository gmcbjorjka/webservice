from datetime import datetime

class Artikel:
    def __init__(self, judul, isi, gambar, penulis):
        self.judul = judul
        self.isi = isi
        self.gambar = gambar
        self.penulis = penulis
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "judul": self.judul,
            "isi": self.isi,
            "gambar": self.gambar,
            "penulis": self.penulis,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
