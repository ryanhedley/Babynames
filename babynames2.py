import sys
import pandas as pd
import jellyfish as jf


def names_import(SEX='F', YEAR_OF_BIRTH=2020):

    # Resolve the Path of the Names subdirectory, and the year of birth file within it
    from pathlib import Path
    NAME_FOLDER = Path().resolve() / 'Names'
    NAME_2020 = NAME_FOLDER / f'yob{YEAR_OF_BIRTH}.txt'

    # Column names for data txt file
    COLUMN_NAMES = ['Name', 'Sex', 'Popularity']

    # Read txt file (in csv format) and create names dataframe
    names_df = pd.read_csv(NAME_2020, names=COLUMN_NAMES)

    # Filter names dataframe by sex
    sex_filt = (names_df['Sex'] == SEX)
    names_df = names_df[sex_filt]

    return names_df


def name_distance_jw(names_df, start_name_list):

    """
    Calculates similarity between the start_name and each of the names in names_df, using these algorithms (in jellyfish):

    Jaro-Winkler is a modification/improvement to Jaro distance, like Jaro it gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.
    """

    for start_name in start_name_list:

        # print(start_name)
        jaro_winkler_column = []

        for test_name in names_df.Name:
            
            jaro_winkler_column.append(round(jf.jaro_winkler_similarity(test_name, start_name),3))
        
        column_name = f"{start_name}"
        names_df[column_name] = jaro_winkler_column

    names_df["Jaro-Winkler"] = round(names_df[start_name_list].mean(axis=1),3)


if __name__ == '__main__':

    try:
        
        SEX = sys.argv[1]
        start_name_list = sys.argv[2:]
        

    except:
        print('Usage: babynames.py [SEX(F or M)] [NAME(S)] ')
        quit()

    YEAR_OF_BIRTH = 2020 #Year of Birth for names list
    NUMBER_SIMILAR = 30 # Number of similar names to be displayed

    names_df = names_import(SEX, YEAR_OF_BIRTH)

    name_distance_jw(names_df, start_name_list)

    jaro_df = names_df.filter(['Name', 'Popularity', 'Jaro-Winkler']).nlargest(NUMBER_SIMILAR, 'Jaro-Winkler')
    jaro_table = jaro_df.to_string(index=0)

    with open(f'{start_name_list}_Top-{NUMBER_SIMILAR}_{SEX}_{YEAR_OF_BIRTH}_Jaro-Winkler.txt','w') as f:
        f.write(f"Starting Names: {start_name_list} \n")
        f.write("\n")
        f.write(jaro_table)






