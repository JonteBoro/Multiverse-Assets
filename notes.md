# Object dimensions
Object dimensions are handled in two steps:
1. Use a python script for blender, to load all .fbx files and extract their dimensions to a .json file
2. Read those values into one combined .csv

## Running the script
The script only needs to be run, if we decide to add more objects. 
Otherwise, running the script is not necessary, as the ``extraced.json`` files contain the results of the script.

In order to run the script, do the following:

Add Blender to path: 
``C:\Program Files\Blender Foundation\Blender 4.0``

```bash
blender --background --python .\blender_extractor.py
```