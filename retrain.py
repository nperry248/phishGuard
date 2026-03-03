"""Retrain the phishing URL classifier and save to webserver/KtpCapstoneModel.pkl"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import joblib
import os

r = pd.read_csv('dataset.csv')

y = r['Type']
X = r.drop(['Type'], axis=1)

categorical_cols = [c for c in X.columns if X[c].nunique() < 10 and X[c].dtype == 'object']
numerical_cols = [c for c in X.columns if X[c].dtype in ['int64', 'float64']]
my_cols = categorical_cols + numerical_cols

X = X[my_cols]

X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

preprocessor = ColumnTransformer(transformers=[
    ('num', SimpleImputer(strategy='constant'), numerical_cols),
    ('cat', Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ]), categorical_cols)
])

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', XGBClassifier(eval_metric='logloss'))
])

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_valid)
print(f"Validation accuracy: {accuracy_score(y_valid, preds):.4f}")

out_path = os.path.join('webserver', 'KtpCapstoneModel.pkl')
joblib.dump(pipeline, out_path)
print(f"Model saved to {out_path}")
print(f"Expected columns: {my_cols}")
