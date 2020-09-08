extends Node

const SAVE_PATH = "user://config.cfg"


var _settings = {
	"ip_address" : "127.0.0.1",
	"nickname"   : ""
}


func load_config():
	var config_file = File.new()
	if not config_file.file_exists(SAVE_PATH):
		return _settings

	config_file.open(SAVE_PATH, File.READ)
	var current_line = parse_json(config_file.get_line())
	_settings = current_line
	config_file.close()
	
	return _settings

func save_config(ip_address, nickname):
	var config_file = File.new()
	config_file.open(SAVE_PATH, File.WRITE)
	_settings["ip_address"] = ip_address
	_settings["nickname"] = nickname
	config_file.store_line(to_json(_settings))
	config_file.close()
