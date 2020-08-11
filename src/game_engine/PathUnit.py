class PathUnit():
    def __init__(self, model):
        self.PathSquareModel = None
        self.safe_zone = False
        self.pins = []

    def add_pin(self, pin):
        self.pins.append(pin)
        if self.multiple_pins_in_unit():
            return self.pins_of_different_color(pin.color)

    def multiple_pins_in_unit(self):
        return len(self.pins) > 1

    def pins_of_different_color(self, color):
        return [pin for pin in self.pins if pin.color != color]

    def is_not_safe(self):
        return not self.safe_zone