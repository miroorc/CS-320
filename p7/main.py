# project: p7
# submitter: mchoi82
# partner: none
# hours: 5

# #predict whether those users will be interested in our product
# #fit method fitting the pipeline
# #predict method using the pipeline for prediction
# #it's easier to start with just the ???_users.csv file (ignoring the logs data)
# #build pipelines based on LogisticRegression,
# #do cross validation in your fit method and prints some stats. Avoid high standard deviation



# '''
# past_purchase_amt --> 60%
# past_purchase_amt + seconds --> ???

# '''

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import cross_val_score
import pandas as pd


class UserPredictor:
    
    def __init__(self):
        self.model = Pipeline([('pf', PolynomialFeatures()),
              ('ss', StandardScaler()),
              ('lr', LogisticRegression()),])
    
    
    def transform(self, user, log, y=None):
        user['badge'] = user['badge'].replace(['bronze', 'silver', 'gold'], [1, 2, 3]) 
        log = pd.DataFrame(log.groupby(by='user_id')['seconds'].sum())
        data = user.merge(log, how = "left", on = "user_id")
        data['seconds'] = data['seconds'].fillna(0)
        
        if not y.empty:
            y['y'] = y['y'].astype(int)
            data = pd.merge(data, y, on = ["user_id"]) 
        return data
    
    
    def fit(self,train_users, train_logs, train_y):
        #(no need to output or return anything), but you'll probably want to fit an underlying sklearn model 
        #(for example, a LogisticRegression) to the data for purposes of later prediction
        data = self.transform(train_users, train_logs, train_y)
        self.x_columns = ['age','badge', 'past_purchase_amt','seconds']
        self.model.fit(data[self.x_columns], data['y'])
        scores = cross_val_score(self.model, data[self.x_columns], data['y'])

    
    def predict(self,test_users, test_logs):
        test_data_transformed = self.transform(test_users, test_logs, pd.DataFrame([]))
        return self.model.predict(test_data_transformed[self.x_columns])