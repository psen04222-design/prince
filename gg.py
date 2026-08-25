from ursina import *
import random

app =Ursina()

# Window Setup
window.title = "3D Endless Runner"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False

# Game Variables
LANES = [-2, 0, 2]       # Left, Center, Right positions
current_lane_idx = 1     # Shuru me Center lane
player_y = 1
is_jumping = False
jump_speed = 8
gravity = 20
vertical_velocity = 0
game_speed = 12
score = 0
game_over = False

# Environment & Track
ground = Entity(
    model='plane',
    scale=(8, 1, 100),
    color=color.rgb(40, 40, 40),
    texture='white_cube',
    texture_scale=(4, 50)
)

# Visual Lane Dividers
for x in [-1, 1]:
    Entity(model='cube', scale=(0.1, 0.05, 100), position=(x, 0.05, 0), color=color.yellow)

# Player Setup
player = Entity(
    model='quad',
texture='prince.jpg',
    color=color.white,
    scale=(0.8, 1.4, 0.8),
    position=(LANES[current_lane_idx], player_y, -2),
    collider='box'
)

# Camera Setup (Third-person view)
camera.position = (0, 6, -18)
camera.rotation_x = 18

# UI Elements
score_text = Text(text=f"Score: {score}", position=(-0.85, 0.45), scale=2, color=color.white)
game_over_text = Text(text="", position=(-0.3, 0), scale=3, color=color.red)

# Obstacle Management
obstacles = []

def spawn_obstacle():
    if game_over:
        return
    lane = random.choice(LANES)
    obs = Entity(
        model='cube',
        color=color.red,
        scale=(1, 1.2, 1),
        position=(lane, 0.6, 40),
        collider='box'
    )
    obstacles.append(obs)
    # Next obstacle spawn interval (randomized)
    invoke(spawn_obstacle, delay=random.uniform(0.8, 1.6))

# Input Handler (Lane Change & Jump)
def input(key):
    global current_lane_idx, is_jumping, vertical_velocity, game_over

    if game_over:
        if key == 'r':
            restart_game()
        return

    # Lane Switching (Left/Right)
    if key in ('a', 'left arrow') and current_lane_idx > 0:
        current_lane_idx -= 1
        player.x = LANES[current_lane_idx]
    elif key in ('d', 'right arrow') and current_lane_idx < 2:
        current_lane_idx += 1
        player.x = LANES[current_lane_idx]

    # Jumping
    if key == 'space' and not is_jumping:
        is_jumping = True
        vertical_velocity = jump_speed

# Game Loop
def update():
    global player_y, is_jumping, vertical_velocity, score, game_over

    if game_over:
        return

    # Score update
    score += time.dt * 10
    score_text.text = f"Score: {int(score)}"

    # Jump physics
    if is_jumping:
        player.y += vertical_velocity * time.dt
        vertical_velocity -= gravity * time.dt
        if player.y <= 1:
            player.y = 1
            is_jumping = False
            vertical_velocity = 0

    # Move obstacles towards player
    for obs in obstacles[:]:
        obs.z -= game_speed * time.dt

        # Collision Check
        if player.intersects(obs).hit:
            trigger_game_over()
            break

        # Remove past obstacles
        if obs.z < -15:
            obstacles.remove(obs)
            destroy(obs)

def trigger_game_over():
    global game_over
    game_over = True
    game_over_text.text = "GAME OVER!\nPress 'R' to Restart"

def restart_game():
    global game_over, score, current_lane_idx, is_jumping, vertical_velocity
    for obs in obstacles:
        destroy(obs)
    obstacles.clear()
    
    current_lane_idx = 1
    player.x = LANES[current_lane_idx]
    player.y = 1
    is_jumping = False
    vertical_velocity = 0
    score = 0
    game_over = False
    game_over_text.text = ""
    spawn_obstacle()

# Start spawning
spawn_obstacle()

# Directional Light for 3D depth
DirectionalLight(y=2, z=-3, shadows=True)

app.run()