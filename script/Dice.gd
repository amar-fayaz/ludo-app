extends Sprite

var roll_value = -1
var dice = null
var show_dice
var show_dice_val
signal rolled(val)

func _ready():
	dice = $DiceView 
	show_dice = get_parent().get_node("ShowDice/DiceView")
	show_dice.connect("animation_finished", self, "_show_animation_finished")

func _on_DiceButton_button_up():
	randomize()
	roll_value = randi() % 6 + 1
	dice.play("DiceRoll")
#	var roll = randi() % 2
#	if roll == 1:
#		roll_value = 1
#	else: 
#		roll_value = 6

func display_dice():
	self.show()
	show_dice.hide()

func hide_dice():
	self.hide()
	show_dice.show()
	
func enable():
	$DiceButton.disabled = false
	
func disable():
	$DiceButton.disabled = true

func _show_animation_finished():
	show_dice.stop()
	show_dice.animation = "DiceFace"
	show_dice.set_frame(show_dice_val - 1)
	
sync func _show_roll_dice(val):
	show_dice.play("DiceRoll")
	show_dice_val = val

func _on_Roll_animation_finished():
	dice.stop()
	$DiceButton.text = str(roll_value)
	dice.animation = "DiceFace"
	dice.set_frame(roll_value - 1)
	rpc("_show_roll_dice", roll_value)
	emit_signal("rolled", roll_value)
