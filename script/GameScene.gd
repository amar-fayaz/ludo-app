extends Node2D

var players = []
onready var winners
var current_player :Player = null
var current_roll :int = 0
var safe_path_indexes = [0, 13, 26, 39, 8, 21, 34, 47]
var connected_players setget set_connected_players
var peerID 
signal game_finished
signal pin_moved 


func _ready():
	peerID = get_tree().get_network_unique_id()
	players = [$BluePlayer, $RedPlayer]#, $GreenPlayer, $YellowPlayer]
	for player in players:
		player.connect("end_player_turn", self, "_on_player_turn_ended")
	$Dice.disable()
	current_player = players[0]

func get_current_player_index():
	return players.find(current_player)

func set_connected_players(conn_players):
	connected_players = conn_players
	var idx = 0
	for player in players:
		player.set_network_master(connected_players[idx])
		idx += 1
	if connected_players[get_current_player_index()] == peerID:
		$Dice.enable()
		$Dice.hide_dice()
	current_player = players[0]
	rpc("change_player", 0)

sync func change_player(player_idx):
	if connected_players[get_current_player_index()] == peerID:
			$Dice.disable()
			$Dice.hide_dice()
	current_player.stop_highlighting()
	current_player = players[player_idx]
	current_player.highlight_player()
	$Dice.set_network_master(connected_players[player_idx])
	if connected_players[get_current_player_index()] == peerID:
			$Dice.enable()
			$Dice.display_dice()
	print("Player Changed ->", current_player.name)

func _on_Dice_rolled(roll):
	if connected_players[get_current_player_index()] == peerID:
		current_roll = roll
		$Dice.disable()
		var eligible_pins = current_player.get_eligible_pins(current_roll)
		if eligible_pins.empty():
			change_turn()
		elif eligible_pins.size() > 1:
			current_player.enable_pins(eligible_pins)
		elif eligible_pins.size() == 1:
			current_player.process_pin_click(eligible_pins[0])
		
func _on_player_turn_ended(player_idx, pin_idx, pin_status):
	if connected_players[get_current_player_index()] == peerID:
		var extra_turn = false
		var new_path_index = -1
		assert(players[player_idx] == current_player)
	
		if pin_status == -1 and current_roll == 6:
			new_path_index = current_player.move_pin(pin_idx, 0)
		else:
			new_path_index = current_player.move_pin(pin_idx, pin_status + current_roll)

	
		var enemies = enemies_in_same_pos(new_path_index)
		if enemies and not(new_path_index in safe_path_indexes):
			for enemy in enemies:
				for enemy_pin in enemy[1]:
					rpc("_kill_pin", enemy[0], enemy_pin)
			extra_turn = true
		if current_roll == 6 or pin_status + current_roll == 56:
			extra_turn = true
		
		if current_player.has_won():
			rpc("_show_player_victory", get_current_player_index())
			extra_turn = false
			
		if extra_turn:
			continue_playing()
		else:
			change_turn()

sync func _show_player_victory(player_idx):
	winners.append(players[player_idx])
	players[player_idx].show_victory()
#	players.remove(player_idx)

func enemies_in_same_pos(path_index):
	if path_index == -1:
		return []
	else:
		var enemies = []
		for player in players:
			if player != current_player:
				var enemy_pins = player.get_pins_in_pos(path_index)
				if enemy_pins:
					enemies.append([player.index, enemy_pins])
		return enemies

sync func _kill_pin(player_idx, pin_idx):
	players[player_idx].pins[pin_idx].kill_pin()

func continue_playing():
	$Dice.enable()

func change_turn():
	if connected_players[get_current_player_index()] == peerID:
#		var start_time = OS.get_ticks_msec()
#		while OS.get_ticks_msec() - start_time < 1000:
#			1 == 1
		rpc("change_player", (get_current_player_index() + 1) % players.size())
	

func _on_exit_game_pressed():
	emit_signal("game_finished")
