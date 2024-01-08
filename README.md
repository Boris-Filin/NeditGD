# NeditGD

 Lightweight Geometry Dash level scripting tool

## Installation

 While Nedit is in early stages of development, you will need to download the code and import the modules manually. The main ones are Editor and Object. For more advanced save file interaction, import SaveLoad.

## Loading the level editor

 For now, Nedit can only read the level at the top of the created levels list ('current level'). If you want to edit a level, push it to the top of your levels list in Geometry Dash first.
 The Editor class handles loading and saving the data automatically. You only need to call the level loader, add your objects, and save the changes:

```python

# Load the most recent level using Editor.load_current_level()
editor = Editor.load_current_level()

# Make all the necessary changes (add/delete objects)
editor.add_object(
    Object(id=1, x=75, y=-15, groups=[12, 42], scale=5))

# Make all the necessary changes (add/delete objects)
editor.save_changes()
```

## New level bug

 Before you use Nedit on a level, make sure you have saved it from within Geometry Dash editor at least once. New levels are not initialised upon creation, so Nedit won't be able to read them.

## Credits

* Code written and hosted by Nemo2510
* [Incidius](https://github.com/Incidius) aided in cataloguing
