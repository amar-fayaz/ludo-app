extends Control

const DEFAULT_PORT = 8910
const NETWORK_ADDRESS = "127.0.0.1"
var players = [1]
var player_info = {}
var joined_names = []
var config_class 
func _ready():
	config_class = get_node("/root/Config")
	var config = config_class.load_config()
	$Nickname.text = config["nickname"]
	$host_ip.text = config["ip_address"]
	get_tree().connect("network_peer_connected", self, "_player_connected")
	get_tree().connect("network_peer_disconnected", self, "_player_disconnected")
	

func _player_connected(_id):
	if get_tree().is_network_server():
		players.append(_id)
		$Status.text = ""
		if players.size() > 1:
			$StartGame.show()

func _connected_to_server():
	var local_player_id = get_tree().get_network_unique_id()
	var nickname = $Nickname.text
	$Status.text = ""
	rpc('_get_player_info', local_player_id, nickname)

func _send_server_info(client_id):
	if get_tree().is_network_server():
		var nickname = $Nickname.text
		rpc_id(client_id, '_get_player_info', 1, nickname)
	
remote func _get_player_info(player_id, nickname):
	if get_tree().is_network_server():
		player_info[player_id] = nickname
		$Status.text = nickname + ' joined.'
		joined_names.append(nickname)
		rpc('_show_joined_players', joined_names)
	else:
		$Status.text = 'Connected to server by ' + nickname + '.\n' + $Status.text

sync func _show_joined_players(nickname_list):
	joined_names = nickname_list
	$JoinedPlayers.text = "Players in the lobby:"
	for nickname in nickname_list:
		$JoinedPlayers.text += '\n' + nickname
	$JoinedPlayers.show()

sync func _begin_game(player_list, player_infos):
	if get_tree().is_network_server():
		config_class.save_config("", $Nickname.text)	
	else:
		config_class.save_config($host_ip.text, $Nickname.text)
	var ludo = load("res://GameScene.tscn").instance()
	get_tree().get_root().add_child(ludo)
	var game_manager = load("res://GameServer.tscn").instance()
	get_tree().get_root().add_child(game_manager)
#	ludo.connect("game_finished", self, "_end_game", [], CONNECT_DEFERRED)
	game_manager.start_game(ludo, player_list, player_infos)
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
	$Status.text = with_error
	get_tree().set_network_peer(null) # Remove peer.
	$Host.set_disabled(false)
	$Join.set_disabled(false)
	$Host/Label.modulate.a = 1.0
	$Join/Label.modulate.a = 1.0
	
func _on_Host_pressed():
	if $Nickname.text == "":
		$Status.text = "Enter Nickname"
	else:
		var host = NetworkedMultiplayerENet.new()
		get_tree().connect('network_peer_connected', self, '_send_server_info')
		host.set_compression_mode(NetworkedMultiplayerENet.COMPRESS_RANGE_CODER)
		var err = host.create_server(DEFAULT_PORT, 3)
		if err != OK:
			# Is another server running?
			$Status.text = "Can't host, address in use."
			return
		$host_ip.text = str(IP.get_local_addresses())
		get_tree().set_network_peer(host)
		$Host.set_disabled(true)
		$Join.set_disabled(true)
		player_info[1] = $Nickname.text
		joined_names = [$Nickname.text]
		$Host/Label.modulate.a = 0.6
		$Join/Label.modulate.a = 0.6
		$Status.text = "Waiting for players..."
	
func _on_Join_pressed():
	if $Nickname.text == "":
		$Status.text = "Enter Nickname"
	else:
		var ip = $host_ip.text
		if not ip.is_valid_ip_address():
			$Status.text = "IP address is invalid"
			return
		get_tree().connect('connected_to_server', self, '_connected_to_server')
		var host = NetworkedMultiplayerENet.new()
		host.set_compression_mode(NetworkedMultiplayerENet.COMPRESS_RANGE_CODER)
		host.create_client(ip, DEFAULT_PORT)
		get_tree().set_network_peer(host)
		$Status.text = "Connecting..."

func _on_Host_button_down():
	$Host/Label.modulate.a = 0.6

func _on_Host_button_up():
	$Host/Label.modulate.a = 1.0

func _on_Join_button_down():
	$Join/Label.modulate.a = 0.6

func _on_Join_button_up():
	$Host/Label.modulate.a = 1.0

func _on_StartGame_pressed():
	if get_tree().is_network_server():
		if players.size() > 1:
			rpc("_begin_game",  players, player_info)
