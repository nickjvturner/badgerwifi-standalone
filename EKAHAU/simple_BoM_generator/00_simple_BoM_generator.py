#!/usr/bin/env python3

"""
Created by Nick Turner (@nickjvturner)

Super Ugly work in progress

Intended for Simulation project files

"""

import zipfile
import json
import time
import shutil
from pathlib import Path
from collections import Counter
from pprint import pprint


def main():
    nl = '\n'

    # Get filename and current working directory
    print(f'{nl}{Path(__file__).name}')
    print(f'working_directory: {Path.cwd()}{nl}')

    # Get local file(s) with extension .esx
    for file in sorted(Path.cwd().iterdir()):
        # ignore files in directory containing _re-zip
        if (file.suffix == '.esx') and (not('re-zip' in file.stem)):
            proceed = input(f'Proceed with file: {str(file.name)}? (YES/no)')
            if proceed == 'no':
                exit()

            print('filename:', file.name)

            # Define the project name
            project_name = file.stem
            print('project_name:', project_name)

            # Unzip the .esx project file into folder named {project_name}
            with zipfile.ZipFile(file.name, 'r') as zip_ref:
                zip_ref.extractall(project_name)
            print('project successfully unzipped')

            # Load the floorPlans.json file into the floorPlansJSON Dictionary
            with open(Path(project_name) / 'floorPlans.json') as json_file:
                floorPlansJSON = json.load(json_file)
                json_file.close()
            # pprint(floorPlansJSON)

            # Create an intermediary dictionary to lookup floor names
            floorPlansDict = {}

            # Populate the intermediary dictionary
            for floor in floorPlansJSON['floorPlans']:
                floorPlansDict[floor['id']] = floor['name']
            # pprint(floorPlansDict)

            # Load the accessPoints.json file into the accessPointsJSON dictionary
            with open(Path(project_name) / 'accessPoints.json') as json_file:
                accessPointsJSON = json.load(json_file)
                json_file.close()
            # pprint(accessPointsJSON)

            try:
                # Remove temporary directory containing unzipped project file
                shutil.rmtree(project_name)
            except Exception as e:
                print(e)

            # Convert accessPointsJSON from dictionary to list
            accessPointsLIST = []
            for ap in accessPointsJSON['accessPoints']:
                accessPointsLIST.append(ap)

            # Create a list to store AP models and external antennas
            ap_model_list = []

            for ap in accessPointsLIST:
                if 'model' in ap:
                    if ' +  ' in ap['model']:
                        apmodel_split_antenna = (ap['model']).split(' +  ')
                        for entry in apmodel_split_antenna:
                            ap_model_list.append(entry)

                    elif ap['model'] == '':
                        ap_model_list.append('measured AP, model unavailable, vendor: ' + ap['vendor'])

                    else:
                        ap_model_list.append(ap['model'])

                else:
                    # print(ap)
                    ap_model_list.append(f"measured AP, model & vendor information available")


            simple_BoM = Counter(ap_model_list)

            # print(simple_BoM)
            print(f'{nl}')
            print(f'{file.stem}')
            print('-' * len(file.stem))

            for key, value in sorted(simple_BoM.items()):
                print(f'{key}, {value}')
            print(f'{nl}')


if __name__ == "__main__":
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print(f'** Time to run: {round(run_time, 2)} seconds **')
