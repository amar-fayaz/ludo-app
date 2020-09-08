extends Node2D

var players = []
var safe_path_indexes = [0, 13, 26, 39, 8, 21, 34, 47]
signal game_finished

onready var dice
onready var player_bases = []

func _ready():
#	players = [$BluePlayer, $RedPlayer]#, $GreenPlayer, $YellowPlayer]
	dice = $Dice
#	player_bases = players
	dice.disable()
	dice.hide_dice()

func set_active_players(num_players):
	var player_configs = {
		2 : [$BluePlayer, $GreenPlayer],
		3 : [$BluePlayer, $RedPlayer, $GreenPlayer],
		4 : [$BluePlayer, $RedPlayer, $GreenPlayer, $YellowPlayer]
	}
	players = player_configs[num_players]
	
		
func enemies_in_same_pos(current_player_idx, path_index):
	if path_index == -1:
		return []
	else:
		var enemies = []
		for player in players:
			if player != players[current_player_idx]:
				var enemy_pins = player.get_pins_in_pos(path_index)
				if enemy_pins:
					enemies.append([player.index, enemy_pins])
		return enemies
	
func show_game_over():
	$GameStatus.text = "Game Over"
	$GameStatus.show()

func _on_exit_game_pressed():
	emit_signal("game_finished")
