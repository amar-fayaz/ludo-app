extends Player

func _ready():
	pins = [$GreenPath/G1, $GreenPath/G2, $GreenPath/G3, $GreenPath/G4]
	path = $GreenPath
	indicator_pin = $GreenPin
	for pin in pins:
		pin.connect("pin_selected", self, "process_pin_click")
		pin.common_path_seed = 26
		pin.path = path
