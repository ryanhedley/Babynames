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


def name_distance(names_df, start_name):

    """
    Calculates similarity between the start_name and each of the names in names_df, using these algorithms (in jellyfish):

    Hamming distance is the measure of the number of characters that differ between two strings.
    Levenshtein distance represents the number of insertions, deletions, and substitutions required to change one word to another.
    A modification of Levenshtein distance, Damerau-Levenshtein distance counts transpositions (such as ifsh for fish) as a single edit.
    Jaro distance is a string-edit distance that gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.
    Jaro-Winkler is a modification/improvement to Jaro distance, like Jaro it gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.
    """

    # Blank lists to temporarily store the respective scores, before adding back to dataframe
    hamming_column = []
    levenshtein_column = []
    damerau_column = []
    jaro_column = []
    jaro_winkler_column = []

    # For each name, compare the start_name using the hamming, levenshtein, damerau, jaro and jaro_winkler algorithms
    for test_name in names_df.Name:

        hamming_column.append(jf.hamming_distance(test_name, start_name))
        levenshtein_column.append(jf.levenshtein_distance(test_name, start_name))
        damerau_column.append(jf.damerau_levenshtein_distance(test_name, start_name))
        jaro_column.append(round(jf.jaro_similarity(test_name, start_name),3))
        jaro_winkler_column.append(round(jf.jaro_winkler_similarity(test_name, start_name),3))

    # Add the calculations back to the dataframe as unique columns
    names_df['Hamming'] = hamming_column
    names_df['Levenshtein'] = levenshtein_column
    names_df['Damerau-Levenshtein'] = damerau_column
    names_df['Jaro'] = jaro_column
    names_df['Jaro-Winkler'] = jaro_winkler_column


if __name__ == '__main__':

    try:
        start_name = sys.argv[1]
        SEX = sys.argv[2]

    except:
        print('Usage: babynames.py BABYNAME SEX(F or M) ')
        quit()

    YEAR_OF_BIRTH = 2020 #Year of Birth for names list
    NUMBER_SIMILAR = 30 # Number of similar names to be displayed

    names_df = names_import(SEX, YEAR_OF_BIRTH)

    name_distance(names_df, start_name)

    # damerau_df = names_df.filter(['Name', 'Popularity', 'Damerau-Levenshtein']).nsmallest(NUMBER_SIMILAR, 'Damerau-Levenshtein')
    # damerau_df.to_string(f'{start_name}_Top-{NUMBER_SIMILAR}_{SEX}_{YEAR_OF_BIRTH}_Damerau-Levenshtein.txt', index=0)

    jaro_df = names_df.filter(['Name', 'Popularity', 'Jaro-Winkler']).nlargest(NUMBER_SIMILAR, 'Jaro-Winkler')
    jaro_df.to_string(f'{start_name}_Top-{NUMBER_SIMILAR}_{SEX}_{YEAR_OF_BIRTH}_Jaro-Winkler.txt', index=0)






