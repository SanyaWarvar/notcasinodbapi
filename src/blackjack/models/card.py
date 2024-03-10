class Card:
    name: str
    value: int

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def get_from_str(cls, string: str):
        nominal, suit = string[:-1], string[-1]
        amount: int = 10
        try:
            amount = int(nominal)
        except ValueError:
            if nominal == "A":
                amount = 11

        return cls(name=string, value=amount)
