import numpy as np
import pandas as pandu
from PIL import Image
import copy

# Probabilities of all the settings
TUNDRA_P = 0.03
FOREST_P = 0.1
DESERT_P = 0.11
OCEAN_P = 0.76
# Array of all the settings' probabilities
SETTING_P = [TUNDRA_P, FOREST_P, DESERT_P, OCEAN_P]


def naive_bayes_classifier(input_filepath):
    im = Image.open(input_filepath, 'r')
    pixel_values = list(im.getdata())

    df = pandu.DataFrame(pixel_values)
    df.rename(columns={0: 'R', 1: 'G', 2: 'B'}, inplace=True)
    rows_count = len(df.index)
    
    #Mapped out list of probabilities for P(rgbVal > 128|placeName)
    rMean = [{"tundra": 0.85, "forest":0.53, "desert":0.94, "ocean":0.18}, (df['R'].sum())/rows_count]
    gMean = [{"tundra": 0.71, "forest":0.88, "desert":0.06, "ocean":0.27}, (df['G'].sum())/rows_count]
    bMean = [{"tundra": 0.89, "forest":0.12, "desert":0.03, "ocean":0.98}, (df['B'].sum())/rows_count]
    settingsList = {"tundra": 0, "forest": 0, "desert": 0, "ocean": 0}

    count = 0
    for key, value in settingsList.items():
        for mean in [rMean, gMean, bMean]:
            if mean[1] > 128 and settingsList[key] == 0:
                settingsList[key] = mean[0][key]
            elif mean[1] > 128 and settingsList[key] != 0:
                settingsList[key] = settingsList[key] * mean[0][key]
            elif mean[1] < 128 and settingsList[key] == 0:
                settingsList[key] = 1 - mean[0][key]
            elif mean[1] < 128 and settingsList[key] != 0:
                settingsList[key] = settingsList[key] * (1 - mean[0][key])
        settingsList[key] = settingsList[key] * SETTING_P[count]
        count += 1

    class_probabilities = {}
    for key, value in settingsList.items():
        class_probabilities[key] = value / (settingsList["tundra"] + settingsList["forest"] + settingsList["desert"] + settingsList["ocean"])
    
    most_likely_class = max(class_probabilities, key=class_probabilities.get)
    util_print(most_likely_class, class_probabilities)
    return most_likely_class, class_probabilities


def fuzzy_classifier(input_filepath):

    # keeping track of a,b,c,d values for each color and each intensity
    red_trapezium_values = {"low": [0, 0, 85, 125], "medium": [85, 125, 130, 190], "high": [130, 190, 255, 255]}
    green_trapezium_values = {"low": [0, 0, 60, 120], "medium": [60, 120, 125, 185], "high": [125, 185, 255, 255]}
    blue_trapezium_values = {"low": [0, 0, 55, 130], "medium": [55, 130, 140, 190], "high": [140, 190, 255, 255]}

    #The truth values of each intensity for each color
    red_truth = {"low": 0, "medium": 0, "high": 0}
    green_truth = {"low": 0, "medium": 0, "high": 0}
    blue_truth = {"low": 0, "medium": 0, "high": 0}

    im = Image.open(input_filepath, 'r')
    pixel_values = list(im.getdata())

    df = pandu.DataFrame(pixel_values)
    df.rename(columns={0: 'R', 1: 'G', 2: 'B'}, inplace=True)
    rows_count = len(df.index)

    # calculate the mean of each color
    rMean = (df['R'].sum())/rows_count
    gMean = (df['G'].sum())/rows_count
    bMean = (df['B'].sum())/rows_count

    # calculate the truth value of each intensity for each color
    for key, value in red_trapezium_values.items():
        red_truth[key] = FuzzyCalc(rMean, value[0], value[1], value[2], value[3])
    for key, value in green_trapezium_values.items():
        green_truth[key] = FuzzyCalc(gMean, value[0], value[1], value[2], value[3])
    for key, value in blue_trapezium_values.items():
        blue_truth[key] = FuzzyCalc(bMean, value[0], value[1], value[2], value[3])
    
    allTruths = calcRulesStrength(red_truth, green_truth, blue_truth)
    highest_membership_class = max(allTruths, key=allTruths.get)
    class_memberships = allTruths

    util_print(highest_membership_class, class_memberships)
    return highest_membership_class, class_memberships

# This function is used to calculate the truth value of a pixel in a trapezium.
def FuzzyCalc(Mean, a, b, c, d):
        if (Mean <= a):
            return 0
        elif (Mean > a and Mean < b):
            return (Mean - a)/(b - a)
        elif (Mean >= b and Mean <= c):
            return 1
        elif (Mean > c and Mean < d):
            return (d - Mean)/(d - c)
        elif (Mean >= d):
            return 0

#Calculates the rule strength of each rules and returns a dictionary of the class and its rule strength
def calcRulesStrength(red_truth, green_truth, blue_truth):
    tundra = red_truth["high"] * green_truth["high"] * blue_truth["high"]
    forest = ((red_truth["low"] + red_truth["medium"]) - (red_truth["low"] * red_truth["medium"])) * green_truth["high"] * ((blue_truth["low"] + blue_truth["medium"]) - (blue_truth["low"] * blue_truth["medium"]))
    desert = red_truth["high"] * green_truth["low"] * blue_truth["low"]
    ocean = red_truth["low"] * blue_truth["high"]
    return {"tundra": tundra, "forest": forest, "desert":desert, "ocean":ocean}


# This function is used to print the results of the classification.
def util_print(name, dic):
    str = list(dic.values()).__str__()
    final = "'"+ name + "', "+ str
    print(final)


# Main function, prints the results of the classification for all the examples.
def main():
    for i in range (0,4):
        input_filepath = "./Examples/Example" + str(i) + "/image.jpg"
        print("Example", i)
        print("\nPrinting NAIVE CLASSIFIER")
        naive_bayes_classifier(input_filepath)
        print()
        print("Printing FUZZY CLASSIFIER")
        fuzzy_classifier(input_filepath)
        print("\n")
    print()


main()