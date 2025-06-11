from datetime import datetime

class Pelabuhan:
    def __init__(self, nama_pelabuhan, image, description, location, rating, facilities, article):
        self.nama_pelabuhan = nama_pelabuhan
        self.image = image
        self.description = description
        self.location = location
        self.rating = rating
        self.facilities = facilities
        self.article = article
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "nama_pelabuhan": self.nama_pelabuhan,
            "image": self.image,
            "description": self.description,
            "location": self.location,
            "rating": self.rating,
            "facilities": self.facilities,
            "article": self.article,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
