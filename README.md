# NeditGD

 Lightweight Geometry Dash level scripting tool

## Installation

### Via Pip

 Nedit is now on [PyPi](https://pypi.org/project/NeditGD/)! After [downloading python](https://www.python.org/downloads/) and [installing Pip](https://pip.pypa.io/en/stable/installation/), run the following command in your terminal of choice:
`pip install NeditGD`
 Which will install Nedit as a package. After that, you can import the main features from Nedit at the start of your file:
`from NeditGD import Object, Editor`

### Manual via GitHub

 If you would like to interact with the source code directly, you can download it from the [GitHub page of Nedit](https://github.com/Boris-Filin/NeditGD).
 Note that Git will be updated more frequently with experimental changes.

## Main components

### Object

Object is a generic dictionary-like class that stores all properties for a given GD object. Properties can be addressed via dot syntax or  dictionary indexing.

```python
# Init spike
obj = Object(
    id = 'spike',
    x = 15,
    y = 15
)
# Add group 42 to spike
obj.groups = ['42']
# Move spike to editor layer 2
obj['layer'] = 2
```

Properties surrounded by underscores are discarded. They allow you to store information in objects during code execution that is not passed into the GD level

```python
objects = []
for i in range(10):
    obj = Object(
        id = 'spike',
        x = 15 + 30 * i,
        y = 15,
        # Record the object's index
        _i_ = i
    )
    objects.append(obj)

...

for obj in objects:
    # Move odd spikes half a block up
    if obj._i_ % 2:
        obj.y += 15
```

Objects have helper methods that allow you to change the most common properties more conveniently. They return the object so you can chain them.

```python
objects = []
obj = Object(...)
# Move object to given position
obj.move_to(15, 75)
# Move object relatively to its position
obj.move(15, 0)
# Add a group to an object and set its layer
objects.append(obj.add_group(42).to_layer(2))
```

### Editor

Editor object is defined by the collection of GD objects in the given level. It is used to interact with the level save. Saving and loading your changes is explained in the next section.

```python
# Create empty editor
editor = Editor()

obj = Object(...)

# Add an object
editor.add_object(obj)

# Print existing objects
print(editor.read_objects())
```

## Loading the level editor

### Live with Geode

NeditGD supports live editing via [WSLiveEditor](https://github.com/iAndyHD3/WSLiveEditor) by [iAndyHD3](https://github.com/iAndyHD3). This option requires Geode to function. If you don't want to use mods, see the next section

You will need to:

- [Install Geode](https://geode-sdk.org/install)
- [Install the mod](https://geode-sdk.org/faq#how-do-i-install-mods) named "WSLiveEditor"
- Open the editor of the file you want to edit

Then you can load the Editor object like so:

```python
# Load the editor currently opened
editor = Editor.load_live_editor()

# Make all the necessary changes (add/delete objects)
editor.add_object(
    Object(id='spike', x=75, y=-15, groups=[12, 42], scale=5))

# Make all the necessary changes (add/delete objects)
editor.save_changes()
```

### From savefile (vanilla)

 For now, Nedit can only read the level at the top of the created levels list ('current level'). If you want to edit a level, push it to the top of your levels list in Geometry Dash first.
 The Editor class handles loading and saving the data automatically. You only need to call the level loader, add your objects, and save the changes:

```python
# Load the most recent level using Editor.load_current_level()
editor = Editor.load_current_level()

# Make all the necessary changes (add/delete objects)
editor.add_object(
    Object(id='spike', x=75, y=-15, groups=[12, 42], scale=5))

# Make all the necessary changes (add/delete objects)
editor.save_changes()
```

## Special group 9999

 With Nedit you can add tens of thousands of objects to your level at a time. If your development process is iterative, they might need to be removed every time you re-run the script. To avoid doing that manually, Nedit uses group 9999 to mark objects as scripted. Upon a Nedit save, every previously existing object with group 9999 will be deleted and replaced with the new ones. Make sure you don't use this group to prevent your manual changes being deleted.
 If you prefer to disable that behaviour for any reason, you can do so by passing False as the second argument whenever loading the editor and adding new objects:

```python

 ...
editor = Editor.load_current_level(remove_scripted=False)
editor.add_objects(your_object_list, mark_as_scripted=False)
```

## Level Version Control

 Due to the way GD saves are structured, Nedit has to load all of the existing levels in a compressed format before extracting/writing data. Therefore a large amount of levels leads to multiple second load times.
 VersionControl.py is a script that allows you to extract data from a GD file and save it in plaintext format for long-term storage. Useful in case you need to test a change - you don't have to create duplicate levels, so the total weight of your GD save becomes significantly lower.
 Finally, you can use this script to store finished projects or ones you aren't planning to work on for a while longer. That further reduces loadtimes, both of Nedit and GD cloud backup itself.

## Credits

- Code written and hosted by Nemo2510
- Live editing introduced by Niche

### Property decoding and testing

Huge thanks to people who helped me dig for property ids and debug Nedit:

- [Incidius](https://github.com/Incidius)
- Toastium
