extends Sprite

onready var dice
onready var show_dice
onready var play_dice
onready var active_dice 
onready var inactive_dice

var roll_value = 1

signal dice_rolled
signal dice_roll_completed

func _ready():
	dice = $DiceView
	play_dice = dice 
	show_dice = get_parent().get_node("ShowDice/DiceView")
	show_dice.connect("animation_finished", self, "_on_Roll_animation_finished")

func _on_DiceButton_button_up():
	disable()
	emit_signal("dice_rolled")

func hide_dice():
	pass
#	self.hide()
#	show_dice.show()
	
func enable():
	$DiceButton.disabled = false
	
func disable():
	$DiceButton.disabled = true

func activate_dice(mode="play"):
	if mode == "play":
		active_dice = play_dice
		inactive_dice = show_dice
		show_dice.hide()
		self.show()
		enable()
		
	elif mode == "show":
		active_dice = show_dice
		inactive_dice = play_dice
		self.hide()
		show_dice.show()
		disable()

func display_active_dice():
#	pass
	active_dice.show()
	inactive_dice.hide()

func show_dice_roll(value):
	roll_value = value
	inactive_dice.animation = str(roll_value)
#	inactive_dice.set_frame(roll_value - 1)
	
	active_dice.animation = "DiceRoll"
	active_dice.play()
	print("animation start", roll_value)
#	if active_dice == show_dice:
#		var start_time = OS.get_ticks_msec()
#		while OS.get_ticks_msec() - start_time < 1000:
#			1 == 1
#	active_dice.stop()
#	active_dice.animation = "DiceFace"
#	active_dice.set_frame(roll_value - 1)
	
func _on_Roll_animation_finished():
	print("animation end ", roll_value)
	active_dice.stop()
	active_dice.animation = str(roll_value)
#	active_dice.set_frame(roll_value - 1)
	emit_signal("dice_roll_completed")
