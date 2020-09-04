extends Player

func _ready():
	pins = [$YellowPath/Y1, $YellowPath/Y2, $YellowPath/Y3, $YellowPath/Y4]
	path = $YellowPath
	indicator_pin = $YellowPin
	for pin in pins:
		pin.connect("pin_selected", self, "process_pin_click")
		pin.common_path_seed = 39
		pin.path = path
