#!/usr/bin/python3

"""
This module processes MuJoCo XML files to extract and sum mass values,
and saves the results to a CSV file.
"""

import os
import xml.etree.ElementTree as ET
import csv
import argparse
import json

EXTRACTED_FILE_NAME = "extracted.json"

def get_total_mass(xml_path):
    """Extract and sum all mass values from a MuJoCo XML file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Find all inertial elements and sum their mass attributes
    total_mass = 0.0
    for inertial in root.findall(".//inertial"):
        if 'mass' in inertial.attrib:
            total_mass += float(inertial.attrib['mass'])

    return total_mass

def process_directories(base_dir):
    """Process all XML files in subdirectories and collect mass data."""
    results = []

    for sub_directory in os.listdir(base_dir):

        object_name = sub_directory
        sub_dir_path = os.path.join(base_dir, sub_directory)
        total_mass = 0
        json_data = {}

        # Process all FBX files in directory
        for file in os.listdir(sub_dir_path):

            # Get the object name (subfolder name)

            if file.endswith(".xml"):
                # Full path to XML file
                xml_path = os.path.join(sub_dir_path, file)
                # Get total mass from the XML file
                total_mass = get_total_mass(xml_path)

            elif file == EXTRACTED_FILE_NAME:
                extracted_file_path = os.path.join(sub_dir_path, EXTRACTED_FILE_NAME)
                with open(extracted_file_path, "r") as extracted_file:
                    json_data = json.load(extracted_file)


        # Create object list as base for csv file
        results.append({
            'object_name': object_name,
            'mass': total_mass,
            'width' : json_data['width'],
            'depth' : json_data['depth'],
            'height' : json_data['height'],
        })

    return results

def save_to_csv(results, output_file):
    """Save results to CSV file."""
    if not results:
        print("No results to save.")
        return

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['object_name', 'mass', 'width', 'depth', 'height']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

def main():
    """Main function to process directories and save results to CSV."""
        # Set up argument parser
    parser = argparse.ArgumentParser(description='Process XML files to extract mass data.')
    parser.add_argument('--dir', '-d', default='objects/', help='Base directory containing object folders')
    parser.add_argument('--output', '-o', default='out.csv',
                        help='Output CSV file name (default: out.csv)')

    # Parse arguments
    args = parser.parse_args()

    # Check if directory exists
    if not os.path.isdir(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist.")
        return

    print(f"Processing directory: {args.dir}")
    results = process_directories(args.dir)

    print(f"Saving results to: {args.output}")
    save_to_csv(results, args.output)

    print(f"Processing complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()
