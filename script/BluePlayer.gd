extends Player

func _ready():
	indicator_pin = $BluePin
	pins = [$BluePath/B1, $BluePath/B2, $BluePath/B3, $BluePath/B4]
	path = $BluePath
	for pin in pins:
		pin.connect("pin_selected", self, "process_pin_click")
		pin.common_path_seed = 0
		pin.path = path
