import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

class Cleaner():
    
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