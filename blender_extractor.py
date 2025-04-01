import bpy
import sys
import os
import json

# Get command line arguments after "--"
argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []

# Default path if none provided
base_directory_path = argv[0] if len(argv) > 0 else r"C:\Users\Jonte\PycharmProjects\Multiverse-Assets\objects"
output_file = argv[1] if len(argv) > 1 else "extracted.json"

for sub_directory in os.listdir(base_directory_path):

    sub_directory_path = os.path.join(base_directory_path, sub_directory)

    # Process all FBX files in directory
    for file in os.listdir(sub_directory_path):
        if file.endswith(".fbx"):

            # Clear existing objects
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

            # Get full file path
            filepath = os.path.join(sub_directory_path, file)

            # Import FBX
            bpy.ops.import_scene.fbx(filepath=filepath)

            # Select all objects
            bpy.ops.object.select_all(action='SELECT')

            dimensions_data = {}
            # Make one object active (required for join)
            if bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

                # Join selected objects
                bpy.ops.object.join()

                # Get dimensions
                obj = bpy.context.active_object
                width = obj.dimensions.x
                depth = obj.dimensions.y
                height = obj.dimensions.z

                # Store dimensions
                dimensions_data = {
                    "width": width,
                    "depth": depth,
                    "height": height
                }

            # Save dimensions to JSON file
            with open(os.path.join(sub_directory_path, output_file), 'w') as f:
                json.dump(dimensions_data, f, indent=4)