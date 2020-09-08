extends IndicatorPin
class_name Pin

export var status = -1 setget status_set
export var index = 0

var common_path_index = -1 setget ,common_path_index_get
var common_path_seed = 0
var home_position = null
var path = null

signal pin_selected(idx)

func _ready():
	home_position = self.position

func common_path_index_get() -> int:
	return get_common_path_index(status)

func get_common_path_index(status_val):
	if -1 <status_val and status < 50:
		return (common_path_seed + status) % 52
	else:
		return -1

func kill_pin():
	var old_pos = self.position
	var new_pos :Vector2
	var tween_delay = 0.08
	for idx in range(0, self.status):
		new_pos = path.get_curve().get_point_position(self.status - 1 - idx)
		tween.interpolate_property(self, "position", old_pos, new_pos, tween_delay, Tween.TRANS_QUINT, Tween.EASE_OUT, (idx * tween_delay))
		old_pos=new_pos
	tween.interpolate_property(self, "position", old_pos, home_position, tween_delay,Tween.TRANS_LINEAR, Tween.EASE_IN_OUT, self.status * tween_delay)
	tween.start()
	self.status = -1
	#self.position = home_position
	yield(tween, "tween_all_completed")

func enable():
	highlight()
	self.z_index = 1
	$Button.disabled=false

func disable():
	stop_highlight()
	self.z_index = 0
	$Button.disabled=true
	
func move(initial_status: int, new_pin_status:int):
	var idx = 0
	var tween_delay = 0.2
	var pin_target
	var old_pos = self.position
	if new_pin_status != -1:
		for new_stat in range(initial_status + 1, new_pin_status + 1):
			var target_in_curve = path.get_curve().get_point_position(new_stat)
			pin_target = target_in_curve + Vector2(0, - self.texture.get_height() * self.scale.y /2)
			tween.interpolate_property(self, "position", old_pos, pin_target, tween_delay, Tween.TRANS_QUINT, Tween.EASE_OUT, idx * tween_delay)
			idx +=  1
			old_pos = pin_target
		tween.start()	


func status_set(value):
	status = min(value, 56)

func _on_Button_pressed():
	emit_signal("pin_selected", index)
