## DSR Mini-Competition

This mini competition is adapted from the Kaggle "[Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales)" challenge. Additional information on the competition can be found on https://github.com/ADGEfficiency/minicomp-rossman.

The goal of this challenge is to predict future sales based on past sales and store information. As evaluation metric we use the root mean square percentage error (RMSPE), which provides a simple way of comparing the results of different groups in the competition.

The competition was limited to three days. This repository covers the group work completed within that time.

## Setting up

1. Clone the repository
```
git clone https://github.com/cverst/minicomp
```

2. Create an environment

Our code is tested for Python 3.8 but other Python 3 releases should also work.

**Using conda**

With Anaconda or miniconda installed, create an environment by running
```
conda create -n minicomp_env python=3.8
```
The environment can be enabled with
```
conda activate minicomp_env
```

**Using pip**

If virtualenv is not installed, start with
```
pip install virtualenv
```
Then, create a virtual environment by running
```
python3 -m venv minicomp_env
```
Enable the virtual environment with
```
source minicomp_env/bin/activate
```

3. Install Jupyter

Assuming your environment name is "minicomp_env" run:
```
pip install jupyter
python -m ipykernel install --user --name minicomp_env --display-name "minicomp_env"
```

4. Install requirements

Access the project folder
```
cd minicomp
```
and install the required python packages in your environment
```
pip install -r requirements.txt
```

5. Make sure store.csv, train.csv, and holdout.csv are present in the data folder.

## Running the code

1. Jupyter notebook

Start Jupyter notebook with
```
jupyter notebook
```
and open "Prediction of Rossmann sales using Random Forest Regressor.ipynb"

2. Contents of the notebook

This notebook gives a detailed explanation of the steps we take in our analysis.
First, three custom classes imported from preprocessing.py (Merger, Cleaner, Imputer) take care of all preprocessing and feature engineering for our model.

After preprocessing, we perform hyperparameter tuning. However, the corresponding code takes very long to run. It is best to skip the cell relating to hyperparameter tuning (indicated in the notebook) and use the hard-coded best hyperparameters provided after that part.

3. Predictions

The score RMSPE for our model is shown at the end of the notebook.


## Dataset

The dataset contains three csv files:

```
#  store.csv
['Store', 'StoreType', 'Assortment', 'CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

#  train.csv and holdout.csv
['Date', 'Store', 'DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo','StateHoliday', 'SchoolHoliday']
```

Below is additional information on the features of our data:

```
Id - an Id that represents a (Store, Date) duple within the test set

Store - a unique Id for each store

Sales - the turnover for any given day (this is what you are predicting)

Customers - the number of customers on a given day

Open - an indicator for whether the store was open: 0 = closed, 1 = open

StateHoliday - indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None

SchoolHoliday - indicates if the (Store, Date) was affected by the closure of public schools

StoreType - differentiates between 4 different store models: a, b, c, d

Assortment - describes an assortment level: a = basic, b = extra, c = extended

CompetitionDistance - distance in meters to the nearest competitor store

CompetitionOpenSince[Month/Year] - gives the approximate year and month of the time the nearest competitor was opened

Promo - indicates whether a store is running a promo on that day

Promo2 - Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating

Promo2Since[Year/Week] - describes the year and calendar week when the store started participating in Promo2

PromoInterval - describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store
```
