#!/usr/bin/env python3
from collections import Counter

from csv_combinator import Combinator
from data_extraction import *
from pepper_arcs.arcs import *
from data_extraction.clean_csv import cleancsv, WrapperGetPart

import pandas as pd

REGEX = r'(?<=P)[0-9]*'
NEW_RECORDINGS_FOLDER = r'/data/pepper/new_recordings/'
CLEANED_ROTATED_DATA = r'/data/pepper/cleaned_rotated_combined.csv'
SIDED_DATA = r'/data/pepper/sided_data.csv'
ARCS = r'/data/pepper/combined_arcs.csv'
FOLDER_PARAMETER = 'pNum'
FILE_PARAMETER = 'eNum'

def remove_multiple_bodies(path):
    df = pd.read_csv(path)
    per_pnum = [x for _, x in df.groupby(df.pNum)]
    df_list = []

    for pnum in per_pnum:
        per_enum = [x for _, x in pnum.groupby(pnum.eNum)]
        for enum in per_enum:
            trackings = [x for _, x in enum.groupby(enum.trackingId)]
            df_list.append(max(trackings, key=len))

    return pd.concat(df_list)
    
def run():
    c = Combinator(NEW_RECORDINGS_FOLDER, NEW_RECORDINGS_COMBINED)
    c.combine(REGEX, FOLDER_PARAMETER, FILE_PARAMETER)
    removed_bodies = remove_multiple_bodies(NEW_RECORDINGS_COMBINED)
    
    # removed_bodies = pd.read_csv(r'/data/pepper/combined_single_plus_zuiderpark.csv')

    per_pnum1 = [x for _, x in removed_bodies.groupby(removed_bodies.pNum)]
    rotated = None
    
    print("ROTATING")
    for person in per_pnum1:
        print(person.iloc[0].pNum)
        per_enum = [x for _, x in person.groupby(person['eNum'])]
        for exercise in per_enum:
            print(exercise.iloc[0].eNum)
            rotated_e = rotate_body(exercise)
            if type(rotated) == type(None):
                rotated = rotated_e
            else:
                rotated= rotated.append(rotated_e)
    
    try:
        old_rotated = pd.read_csv(CLEANED_ROTATED_DATA)
        new_rotated = old_rotated.append(rotated)
    except:
        new_rotated = rotated
    new_rotated.to_csv(CLEANED_ROTATED_DATA)



    # Do Thijs' stuff
    print("THJS SHIZZLE")
    per_pnum2 = [x for _, x in rotated.groupby(rotated.pNum)]
    combined_with_sides = None
    for person in per_pnum2:
        per_enum = [x for _, x in person.groupby(person['eNum'])]
        if len(per_enum) == 3:
            for exercise in per_enum:
                try:
                    enum_ = exercise.iloc[0].eNum
                    exercise = exercise.reset_index(drop=True)
                    cut_exercise = cleancsv(exercise, enum_)
                    cut_exercise = cut_exercise.reset_index(drop=True)
                    cut_exercise = WrapperGetPart(cut_exercise, enum_)
                    if not isinstance(combined_with_sides, type(pd.DataFrame())):
                        combined_with_sides = cut_exercise
                    else:
                        combined_with_sides = pd.concat([combined_with_sides,
                                                         cut_exercise])
                except:
                    print("EXCEPTION!")
                    continue
    try:
        old_sided = pd.read_csv(SIDED_DATA)
        new_sided = old_sided.append(combined_with_sides)
    except:
        new_sided = combined_with_sides
    new_sided.to_csv(SIDED_DATA)
    
    # Calculate arcs
    print("ARCING")
    per_pnum3 = [x for _, x in combined_with_sides.groupby(combined_with_sides.pNum)]
    all_arcs = None
    for person in per_pnum3:
        pnum = person['pNum'].iloc[0]
        print(pnum)
        per_enum = [x for _, x in person.groupby(person.eNum)]
        for exercise in per_enum:
            enum_ = exercise['eNum'].iloc[0]
            per_side = [x for _, x in exercise.groupby(exercise.Side)]
            for sided in per_side:
                Side = sided['Side'].iloc[0]
                arcs = get_arcs(sided, enum_, Side)
                if not Side == '':
                    arcs = get_arcs(sided, enum_, Side)
                    arcs['pNum'] = pnum
                    arcs['eNum'] = enum_
                    arcs['Side'] = Side
                    if type(all_arcs) == type(None):
                        all_arcs = arcs
                        print("all_arcs is None")
                    else:
                        all_arcs = all_arcs.append(arcs)
                        print("APPENDED")

    try:
        old_arcs = pd.read_csv(ARCS)
        new_arcs = old_arcs.append(all_arcs)
    except:
        new_arcs = all_arcs

    new_arcs.to_csv(r'/data/pepper/upto_92.csv')

    print("jwz")
