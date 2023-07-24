# Decision Trees

## Description

This project is a implementation of the ID3 algorithm for decision trees. The algorithm is implemented in the file id3.py. The algorithm is tested with the restaurant dataset, the weather dataset and the iris dataset. The connect4 game is in the file connect4.py. The connect4 game uses the decision tree to make the moves. The connect4 game uses the MCTS algorithm to make the moves.

## Requirements Lib

Python 3.9.1 installed.
All of the requirements are in the default python library.

## Run the decision trees code

```
python3 main.py <dataset> <predict?>

```

* [dataset](): The dataset to be used.
* [predict?](): Whether to predict the class of the last column or not. Y or N.


For insert the values of the atributtes, you need to use the following format:

In restaurant dataset:

* [Alt](): Yes/No
* [Bar](): Yes/No
* [Fri](): Yes/No
* [Hun](): Yes/No
* [Pat](): Full/Some/None
* [Price](): $/$$/$$$
* [Rain](): Yes/No
* [Res](): Yes/No
* [Type](): French/Italian/Thai/Burger
* [Est](): 0-10/10-30/30-60/>60


In weather dataset:

* [Weather]() : sunny/overcast/rainy
* [Temp]() : any int number
* [Humidity]() : any int number
* [Wind]() : TRUE/FALSE

In iris dataset:

* [sepal_length]() : any float number
* [sepal_width]() : any float number
* [petal_length]() : any float number
* [petal_width]() : any float number


## Run the connect4 game

To run the connect4 game with the decision tree, you need to run the following command:

```
python3 connect4.py <time>

```
* [time](): The time limit for MCTS in seconds.
