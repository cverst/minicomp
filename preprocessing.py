import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


class Merger():
    """Merges sales table with store table AFTER dropping unused sampels and features
    """
    
    def __init__(self):
        nondropped_data = None
        merged_data = None
        sales_data = None
        store_data = None
    
    
    def merge(self, sales_data, store_data):
        self.sales_data = sales_data
        self.store_data = store_data
        self._drop_data()
        self._merge_sales_stores()
        return self.merged_data
    
    
    def _drop_data(self):
        sales_data = self.sales_data
        
        # drop NaN in sales
        sales_data.dropna(subset=["Sales"], inplace=True)
        
        # remove rows where sales=0
        keep_mask = sales_data.loc[:, "Sales"] != 0
        sales_data = sales_data[keep_mask]
        
        # drop the cutomers feature
        sales_data.drop("Customers", axis=1, inplace=True)
        
        # store data
        self.nondropped_data = sales_data
    
    
    def _merge_sales_stores(self):
        
        nondropped_data = self.nondropped_data
        store_data = self.store_data
        
        # fill NaNs
        nondropped_data = nondropped_data.fillna({"Store": 0})
        
        # make dtype the same on merging key
        nondropped_data = nondropped_data.astype({"Store": int})
        
        # merging and storing
        self.merged_data = nondropped_data.merge(store_data, how="left", on="Store")
        



class Imputer():
    
    def __init__(self):
        self.zero_imputed = ["Open", "Promo", "SchoolHoliday"]
        self.mode_imputed = ["StateHoliday", "StoreType", "Assortment"]
        self.median_imputed = ["CompetitionDistance"]
        self.columns_ordered = self.zero_imputed + self.mode_imputed + self.median_imputed
        self.transformers = None


    def define_imputers(self):
        
        zero_imputer = SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=0)
        mode_imputer = SimpleImputer(missing_values=np.nan, strategy="most_frequent")
        median_imputer = SimpleImputer(missing_values=np.nan, strategy="median")
        
        self.transformers = ColumnTransformer(
            transformers=[
                ("zero_imputer", zero_imputer, self.zero_imputed),
                ("mode_imputer", mode_imputer, self.mode_imputed),
                ("median_imputer", median_imputer, self.median_imputed),
            ]
        )

    
    def fit(self, X):
        self.transformers.fit(X)

        
    def transform(self, X):
        transformed = self.transformers.transform(X)
        return transformed


    def fit_transform(self, X):
        transformed = self.transformers.fit_transform(X)
        return transformed
    
    
    def transform_reconstruct(self, X):
        X_out = X.copy()
        X_out.loc[:, self.columns_ordered] = self.transform(X)
        return X_out


class Cleaner():
    """Clean data and set data types
    """
    
    def __init__(self):
        self.data = None
    
    
    def clean(self, data):
        self.data = data
        self._correct_stateholiday()
        self._convert_competition_date()
        self._set_dtypes()
        return self.data
    
    
    def _correct_stateholiday(self):

        def zerofun(row):
            if row["StateHoliday"] == "0.0":
                out = "0"
            else:
                out = row["StateHoliday"]
            return out

        self.data = self.data.astype({"StateHoliday": str})
        self.data.loc[:, "StateHoliday"] = self.data.apply(func=zerofun, axis=1)

        
    def _set_dtypes(self):
        self.data = self.data.astype({
            "StateHoliday": "category",
            "StoreType": "category",
            "Assortment": "category"
        })
    

    def _convert_competition_date(self):
        # change CompetitionOpenSinceMonth CompetitionOpenSinceYear to days from sales
        self.data.loc[:, 'CompetitionOpenDate'] = pd.to_datetime(dict(
            year=self.data.CompetitionOpenSinceYear,
            month=self.data.CompetitionOpenSinceMonth,
            day=1
            ))
        self.data.loc[:, 'DateObj'] = pd.DatetimeIndex(self.data.Date)
        self.data.loc[:, 'SalesCompetitionLag'] = (self.data.loc[:, 'DateObj'] - self.data.loc[:, 'CompetitionOpenDate'])


    # change Promo2SinceYear Promo2SinceWeek to days from sales
    # run _convert_competition_date first, need data['DateObj'] column
    def _promo2_date(self):
        dates = self.data.Promo2SinceYear * 100 + (self.data.Promo2SinceWeek - 1)
        dates.fillna(0, inplace=True)
        dates = dates.astype(int)
        dates = dates.astype(str) + '0'
        dates.replace('00', np.nan, inplace=True)
        self.data['Promo2Date'] = pd.to_datetime(dates, format='%Y%W%w')
        # self.data['DateObj'] = pd.DatetimeIndex(self.data.Date)
        self.data['Promo2Lag'] = (self.data['DateObj'] - self.data['Promo2Date'])

        # return data