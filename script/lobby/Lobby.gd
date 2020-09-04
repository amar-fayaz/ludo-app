extends Control

const DEFAULT_PORT = 8910
const NETWORK_ADDRESS = "127.0.0.1"
var players = [1]

func _ready():
	get_tree().connect("network_peer_connected", self, "_player_connected")
	get_tree().connect("network_peer_disconnected", self, "_player_disconnected")


func _player_connected(_id):
	print("success")
	if get_tree().is_network_server():
		print(players)
		players.append(_id)
		if players.size() == 2:
			rpc("_begin_game",  players)

sync func _begin_game(player_list):
	var ludo = load("res://GameScene.tscn").instance()
	get_tree().get_root().add_child(ludo)
	ludo.connect("game_finished", self, "_end_game", [], CONNECT_DEFERRED)
	ludo.connected_players = player_list
	print(player_list)
	hide()
	
func _player_disconnected(_id):
	if get_tree().is_network_server():
		_end_game("Client disconnected")
	else:
		_end_game("Server disconnected")
		
func _end_game(with_error = ""):
	if has_node("/root/GameScene"):
		# Erase immediately, otherwise network might show errors (this is why we connected deferred above).
		get_node("/root/GameScene").free()
		show()
	
	get_tree().set_network_peer(null) # Remove peer.
	$Host.set_disabled(false)
	$Join.set_disabled(false)
	
func _on_Host_pressed():
	var host = NetworkedMultiplayerENet.new()
	host.set_compression_mode(NetworkedMultiplayerENet.COMPRESS_RANGE_CODER)
	var err = host.create_server(DEFAULT_PORT, 1) # Maximum of 1 peer, since it's a 2-player game.
	if err != OK:
		# Is another server running?
		print("Can't host, address in use.")
		return
	
	get_tree().set_network_peer(host)
	$Host.set_disabled(true)
	$Join.set_disabled(true)
	print("Waiting for player...")
	
func _on_Join_pressed():
	var ip = $home_ip.text
	if not ip.is_valid_ip_address():
		print("IP address is invalid")
		return
	
	var host = NetworkedMultiplayerENet.new()
	host.set_compression_mode(NetworkedMultiplayerENet.COMPRESS_RANGE_CODER)
	host.create_client(ip, DEFAULT_PORT)
	get_tree().set_network_peer(host)
	
	print("Connecting...")
