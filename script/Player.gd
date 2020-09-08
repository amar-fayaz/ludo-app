extends Sprite
class_name Player

export var index = 0

var pins = []
var path:Path2D = null
var indicator_pin = null

signal pin_chosen(pin_idx)

func set_player_name(name):
	get_node("PlayerName").text = name

func highlight_player():
	indicator_pin.highlight()
	
func stop_highlighting():
	indicator_pin.stop_highlight()

func get_eligible_pins(roll_value:int):
	var eligible_idx = []
	for idx in range(pins.size()):
		var pin := pins[idx] as Pin
		if pin.status == -1: 
			if roll_value == 6:
				eligible_idx.append(idx)
		elif pin.status + roll_value <= 56:
			eligible_idx.append(idx)
	return eligible_idx
	
func enable_eligible_pins(roll_value:int):
	var eligible_pins = get_eligible_pins(roll_value)
	if not eligible_pins.empty():
		for idx in eligible_pins:
			pins[idx].enable()

func get_pins_in_pos(path_index):
	var pins_in_pos = []
	for pin in pins:
		if pin.common_path_index == path_index:
			pins_in_pos.append(pin.index)
	return pins_in_pos

func enable_pins(pin_idx):
	for idx in pin_idx:
		pins[idx].enable()

func disable_all_pins():
	for pin in pins:
		pin.disable()

func process_pin_click(idx):
	disable_all_pins()
	emit_signal("pin_chosen", idx)

#func move_pin(pin_idx, new_pin_status):
#	var pin: Pin = pins[pin_idx]
#	return pin.move(new_pin_status)
	
func has_won():
	var won = true
	for pin in pins:
		if pin.status != 56:
			won = false
			break 
	return won

func show_your_turn():
	var status_text = get_parent().find_node("GameStatus")
	status_text.text = "Your Turn"
	status_text.show()

func hide_your_turn():
	var status_text = get_parent().find_node("GameStatus")
	status_text.text = ""
	status_text.hide()

func show_victory(standing):
#	for pin in pins:
#		pin.hide()
	$VictoryPanel/Position.text = str(standing)
	$VictoryPanel.show()

