<p align="center">
  <img src="docs/images/icon.webp" width="144" alt="CamCycler app icon">
</p>

# CamCycler

A small Blender add-on for cycling through the cameras in a scene and toggling
camera-view lock, without leaving the 3D viewport.

![CamCycler moves through the cameras surrounding a Blender scene with the Shift plus Numpad 0 shortcut](docs/images/camcycler.png)

*Step through every scene camera from the viewport, then toggle camera-to-view locking when you need to reframe a shot.*

Requires Blender 3.0 or newer.

## What it does

**Next Camera** (`camcycler.next_camera`) — steps to the next camera in the
scene, ordered by name, wrapping around at the end. If the viewport isn't
already looking through a camera, it switches to camera view. Reports the new
camera's name in the status bar, or warns if the scene has no cameras.

**Toggle Camera Lock** (`camcycler.toggle_lock`) — flips `Lock Camera to View`
on the active 3D viewport, so you can navigate freely while staying in the
camera.

## Default keymap

| Shortcut | Action |
| --- | --- |
| <kbd>Shift</kbd> + <kbd>Numpad 0</kbd> | Next Camera |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd> | Toggle Camera Lock |

Both are bound in the *3D View* keymap and can be rebound from the add-on's
preferences panel.

## Installation

1. Download `cam_cycler.py`.
2. In Blender, open **Edit → Preferences → Add-ons**.
3. Choose **Install from Disk** (the dropdown in the top-right corner; on
   Blender 3.x this is the **Install…** button) and pick `cam_cycler.py`.
4. Enable **CamCycler** in the add-on list.

## Test scene

`cam cycler test scene.blend` is a scratch scene kept in the repo for
exercising the cycling behaviour.
