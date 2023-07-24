from id3_datasets import *
import sys

dataset = sys.argv[1] # dataset a usar
example = sys.argv[2].upper() # exemplo a prever (y/n)

if dataset == "restaurant":
    Restaurant = read_csv('restaurant.csv')
    TargetAttribute = 'Class'
    Attributes = {'Fri','Hun','Pat','Type'}
    Attributes2 = ['Alt','Bar','Fri','Hun','Pat','Price','Rain','Res','Type','Est']
    Root = id3(Restaurant, TargetAttribute, Attributes)
    print_tree(Root)
    print('\n')
    if example == "Y": # exemplo a prever
        prediction_ex = {}
        print('\nInsert the values for the following attributes: ') 
        for i in range(0,len(Attributes2)):
            value = input(f"{Attributes2[i]}: ")
            prediction_ex[Attributes2[i]] = value
        
        prediction = predict_example(prediction_ex, Root)
        print('\nPrediction:', prediction)


if dataset == "weather":
    Weather = read_csv('weather.csv')
    TargetAttribute = 'Play'
    Attributes = {'Weather', 'Temp', 'Humidity', 'Windy'}
    Attributes2 = ['Weather', 'Temp', 'Humidity', 'Windy']
    Root = id3(Weather, TargetAttribute, Attributes)
    print_tree(Root)
    print('\n')
    
    if example == "Y": # exemplo a prever
        prediction_ex = {}
        print('\nInsert the values for the following attributes: ') 
        for i in range(0,len(Attributes2)):
            value = input(f"{Attributes2[i]}: ")
            prediction_ex[Attributes2[i]] = value
        
        prediction = predict_example(prediction_ex, Root)
        print('\nPrediction:', prediction)



if dataset == "iris":
    Iris = read_csv('iris.csv')
    TargetAttribute = 'class'
    Attributes = {'sepallength', 'sepalwidth', 'petallength', 'petalwidth'}
    Attributes2 = ['sepallength', 'sepalwidth', 'petallength', 'petalwidth']
    RoundFloat(Iris, 'sepallength')
    RoundFloat(Iris, 'sepalwidth')
    RoundFloat(Iris, 'petallength')
    RoundFloat(Iris, 'petalwidth')
    Root = id3(Iris, TargetAttribute, Attributes)
    print_tree(Root)
    print('\n')
    
    if example == "Y": # exemplo a prever
        prediction_ex = {}
        print('\n\nInsert the values for the following attributes') 
        for i in range(0,len(Attributes2)):
            value = input(f"{Attributes2[i]}: ")
            prediction_ex[Attributes2[i]] = value
        
        prediction = predict_example(prediction_ex, Root)
        print('\nPrediction:', prediction)
