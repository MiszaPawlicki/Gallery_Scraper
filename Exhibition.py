class Exhibition:
    def __init__(self, name, date, location, description, price):
        self.name = name
        self.date = date
        self.location = location
        self.description = description
        self.price = price

    def __str__(self):
        return f"Exhibition: {self.name}\nDate: {self.date}\nLocation: {self.location}\nDescription: {self.description}\nPrice: {self.price}"

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "description": self.description,
            "price": self.price
        }
