from vpython import *
# JavaScript and CSS to make the canvas full screen
fullscreen_js = """
<style>
html, body { margin: 0; padding: 0; overflow: hidden; height: 100%; }
#glowscript-canvas { width: 100vw; height: 100vh; display: block; }
</style>
<script>
window.addEventListener("load", function() {
    var canvas = document.getElementById('glowscript-canvas');
    if (canvas.requestFullscreen) {
        canvas.requestFullscreen();
    } else if (canvas.mozRequestFullScreen) { // Firefox
        canvas.mozRequestFullScreen();
    } else if (canvas.webkitRequestFullscreen) { // Chrome, Safari and Opera
        canvas.webkitRequestFullscreen();
    } else if (canvas.msRequestFullscreen) { // IE/Edge
        canvas.msRequestFullscreen();
    }
});
</script>
"""

scene.append_to_caption(fullscreen_js)
scene.width = 1920
scene.height = 1080
scene.background = color.black

# Constants
G = 6.67430e-11  # Gravitational constant
m1 = 1.989e30    # Mass of Sun 1 (kg)
m2 = 1.989e30    # Mass of Sun 2 (kg)
m3 = 5.972e24    # Mass of Planet (kg)

# Initial positions (meters)
r1 = vector(-1e11, 0, 0)
r2 = vector(1e11, 0, 0)
r3 = vector(0, 0, 0)  # Center the planet on the screen initially

# Initial velocities (meters/second)
v1 = vector(0, -2e4, 0)
v2 = vector(0, 2e4, 0)
v3 = vector(2.5e4, 0, 0)

# Create visual objects with textures
sun1 = sphere(pos=r1, radius=7e9, texture="sun_texture.jpg", emissive=True)
sun2 = sphere(pos=r2, radius=7e9, texture="sun_texture.jpg", emissive=True)
planet = sphere(pos=r3, radius=3e9, texture="planet_texture.jpg", make_trail=True, trail_color=color.white)

# Add lighting to make it look realistic
distant_light(direction=vector(1, 0, 0), color=color.white)
local_light(pos=sun1.pos, color=color.yellow)
local_light(pos=sun2.pos, color=color.orange)

# Time step
dt = 1000

def gravitational_force(m1, m2, r1, r2):
    r = r2 - r1
    r_mag = mag(r)
    r_hat = r / r_mag
    force = G * m1 * m2 / r_mag**2 * r_hat
    return force

# Adjust the camera position and direction
scene.camera.pos = vector(0, -2e11, 2e11)
scene.camera.axis = vector(0, -1e11, -2e11)

# Variable to track the current object being followed
follow_index = 0
objects_to_follow = [planet,sun1, sun2]

def on_keydown(evt):
    global follow_index
    if evt.key == 'f':  # Press 'f' to switch follow target
        follow_index = (follow_index + 1) % len(objects_to_follow)
        scene.camera.follow(objects_to_follow[follow_index])

scene.bind("keydown", on_keydown)

# Simulation loop
while True:
    rate(100)  # Controls the speed of the simulation

    # Calculate forces
    F12 = gravitational_force(m1, m2, r1, r2)
    F13 = gravitational_force(m1, m3, r1, r3)
    F23 = gravitational_force(m2, m3, r2, r3)

    # Update velocities
    v1 += (F12 + F13) / m1 * dt
    v2 += (-F12 + F23) / m2 * dt
    v3 += (-F13 - F23) / m3 * dt

    # Update positions
    r1 += v1 * dt
    r2 += v2 * dt
    r3 += v3 * dt

    # Update visual objects
    sun1.pos = r1
    sun2.pos = r2
    planet.pos = r3

    # Make the camera follow the selected object
    scene.center = objects_to_follow[follow_index].pos
