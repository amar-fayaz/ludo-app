extends Player

func _ready():
	pins = [$RedPath/R1, $RedPath/R2, $RedPath/R3, $RedPath/R4]
	path = $RedPath
	indicator_pin = $RedPin
	for pin in pins:
		pin.connect("pin_selected", self, "process_pin_click")
		pin.common_path_seed = 13
		pin.path = path
