extends Node

var pins
var path
var index

var won = false
var game_base setget game_base_set
var nickname setget player_name_set

func game_base_set(base):
	game_base = base
	pins = base.pins
	path = base.path
	index = base.index
	
func player_name_set(name):
	game_base.set_player_name(name)

func activate():
	if is_network_master():
		game_base.show_your_turn()
	game_base.highlight_player()

func deactivate():
	game_base.hide_your_turn()
	game_base.stop_highlighting()

func get_eligible_pins(roll):
	return game_base.get_eligible_pins(roll)

func activate_eligible_pins(pin_list):
	for pin in pin_list:
		pins[pin].enable()

func show_victory(standing):
	won = true
	game_base.show_victory(standing)
