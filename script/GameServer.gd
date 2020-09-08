extends Node

var active_players = []
var winners = []

var myID
var current_player_idx = -1
var scene 
var dice
var roll_value

func start_game(game_scene, players, player_info):
	scene = game_scene
	scene.set_active_players(players.size())
	var idx = 0
	myID = get_tree().get_network_unique_id()
	for player in players:
		var new_player = load("res://NetworkPlayer.tscn").instance()
		new_player.game_base = game_scene.players[idx]
		new_player.nickname = player_info[player]
		new_player.set_network_master(player)
		scene.players[idx].connect("pin_chosen", self, "_request_move_pin")
		active_players.append(new_player)
		add_child(new_player)
		idx += 1

	dice = scene.dice
	dice.connect("dice_rolled", self, "_on_dice_rolled")
	dice.connect("dice_roll_completed", self, "_post_roll_actions")


	if get_tree().is_network_server():
		rpc("_activate_player", 0)

sync func _activate_player(player_idx):
	if current_player_idx != -1:
		active_players[current_player_idx].deactivate()
	current_player_idx = player_idx
	var current_player = active_players[player_idx]
	if current_player.is_network_master():
		dice.activate_dice("play")
	else:
		dice.activate_dice("show")
	active_players[current_player_idx].activate()
		
#	dice.display_active_dice()
#	dice.display_active_dice()

sync func _game_over():
	scene.show_game_over()
	
remote func _update_statuses(new_statuses):
	var pl_i = 0
	for player in active_players:
		var pi_i = 0
		for pin in player.pins:
			pin.status = new_statuses[pl_i][pi_i]
			pi_i += 1
		pl_i += 1

remote func _change_player(extra_turn):
	if get_tree().is_network_server():
		print("Changing Player")
		var all_statuses = []
		for player in active_players:
			var player_status  = []
			for pin in player.pins:
				player_status.append(pin.status)
			all_statuses.append((player_status))
		rpc("_update_statuses", all_statuses)
		if winners.size() == active_players.size() - 1:
			rpc("_game_over")
			return
		var new_current_player_idx
		if not extra_turn:
			var new_idx = (current_player_idx + 1) % active_players.size()
			while active_players[new_idx].won:
				new_idx = (new_idx + 1) % active_players.size()
			new_current_player_idx = new_idx
		else:
			new_current_player_idx = current_player_idx
		rpc("_activate_player", new_current_player_idx)
	
sync func _show_dice_roll(value):
	roll_value = value
	dice.show_dice_roll(value)

sync func _move_pin_to_status(player_idx, pin_idx, current_status, new_status):
	active_players[player_idx].pins[pin_idx].move(current_status, new_status)	

sync func _kill_pin(player_idx, pin_idx):
	active_players[player_idx].pins[pin_idx].kill_pin()
	
sync func _player_victory(player_idx, standing):
	active_players[player_idx].show_victory(standing)

func _on_dice_rolled():
	randomize()
	roll_value = randi() % 6 + 1
#	var x = randi() % 2
#	if x == 1:
#		roll_value = 6
#	else:
#		roll_value = 1
	print("rolling_dice")
	rpc("_show_dice_roll", roll_value)
	
func _post_roll_actions():
	var current_player = active_players[current_player_idx]
	print(current_player_idx)
	if current_player.is_network_master():
		var eligible_pins = current_player.get_eligible_pins(roll_value)
		if eligible_pins.size() > 1:
			current_player.activate_eligible_pins(eligible_pins)
		elif eligible_pins.size() == 1:
			_request_move_pin(eligible_pins[0])
		else:
			_request_changing_player()
			
remote func _start_move_pin(idx):
	if get_tree().is_network_server():
		var extra_turn = false
		var current_player = active_players[current_player_idx]
		var pin_to_move = current_player.pins[idx]
		var current_pin_status = pin_to_move.status
		var new_pin_status
		if current_pin_status == -1 and roll_value == 6:
			 new_pin_status = 0
		else:
#			new_pin_status = 56
			new_pin_status = current_pin_status + roll_value
		rpc("_move_pin_to_status", current_player_idx, idx, current_pin_status, new_pin_status)
		pin_to_move.status = new_pin_status
		var new_path_index = pin_to_move.get_common_path_index(new_pin_status)

		var enemies = scene.enemies_in_same_pos(current_player_idx, new_path_index)
		if enemies and not(new_path_index in scene.safe_path_indexes):
			for enemy in enemies:
				for enemy_pin in enemy[1]:
					rpc("_kill_pin", enemy[0], enemy_pin)
			extra_turn = true
		if roll_value == 6 or new_pin_status == 56:
			extra_turn = true
		if current_player.game_base.has_won():
			winners.append(current_player_idx)
			rpc("_player_victory", current_player_idx, winners.size())
			extra_turn = false
		_change_player(extra_turn)

func _request_move_pin(idx):
	if active_players[current_player_idx].is_network_master() and not get_tree().is_network_server():
		rpc_id(1, "_start_move_pin", idx)
	else:
		_start_move_pin(idx)
		
func _request_changing_player(extra_turn=false):
	if active_players[current_player_idx].is_network_master() and not get_tree().is_network_server():
		rpc_id(1, "_change_player", extra_turn)
	else:
		_change_player(extra_turn)
