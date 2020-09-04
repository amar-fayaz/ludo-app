extends Sprite
class_name IndicatorPin

var start_pos :Vector2
var highlight_pos :Vector2
var tween :Tween
export var show_highlight = false

func _ready():
	tween = Tween.new()
	add_child(tween)

func highlight():
	start_pos = self.position
	highlight_pos = self.position - Vector2(0, self.texture.get_height()/2)
	show_highlight = true
	tween_indicator()

func stop_highlight():
	if show_highlight:
		show_highlight = false
		tween.stop_all()
		position = start_pos

func tween_indicator():
	if show_highlight:
		var bounce_up_duration = 0.25
		var bounce_down_duration = 0.5
		tween.interpolate_property(self, "position", start_pos, highlight_pos, bounce_up_duration,Tween.TRANS_LINEAR, Tween.EASE_IN)
		tween.interpolate_property(self, "position", highlight_pos, start_pos, bounce_down_duration, Tween.TRANS_ELASTIC, Tween.EASE_OUT, bounce_up_duration)
		tween.interpolate_callback(self, bounce_up_duration + bounce_down_duration, "tween_indicator")
		tween.start()
