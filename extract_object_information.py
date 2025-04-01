#!/usr/bin/python3

"""
This module processes MuJoCo XML files to extract and sum mass values,
and saves the results to a CSV file.
"""

import os
import xml.etree.ElementTree as ET
import csv
import argparse


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

    # Walk through all subdirectories
    for dirpath, dirnames, filenames in os.walk(base_dir):

        dirnames.sort()  # Sort directories for consistency
        filenames.sort()  # Sort files within each directory

        # Get the object name (subfolder name)
        object_name = os.path.basename(dirpath)

        xml_files = [f for f in filenames if f.endswith('.xml')]

        if len(xml_files) == 0:
            raise Exception('No XML files found')
        elif len(xml_files) > 1:
            raise Exception('Multiple XML files found')

        xml_file = xml_files[0]
        # Full path to XML file
        xml_path = os.path.join(dirpath, xml_file)
        # Get total mass from the XML file
        total_mass = get_total_mass(xml_path)



        # Create object list as base for csv file
        results.append({
            'object_name': object_name,
            'mass': total_mass
        })

    return results

def save_to_csv(results, output_file):
    """Save results to CSV file."""
    if not results:
        print("No results to save.")
        return

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['object_name', 'mass']
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
