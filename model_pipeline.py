
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.combine import SMOTEENN
from imblearn.pipeline import Pipeline as ImbPipeline

def prepare_data(train_path=None, test_path=None):
    if train_path and test_path:
        data_train = pd.read_csv(train_path)
        data_test = pd.read_csv(test_path)
        data = pd.concat([data_train, data_test], ignore_index=True)
    else:
        raise ValueError("Please provide train and test file paths")

    label_encoder = LabelEncoder()
    data['International plan'] = label_encoder.fit_transform(data['International plan'])
    data['Voice mail plan'] = label_encoder.fit_transform(data['Voice mail plan'])
    data['Churn'] = label_encoder.fit_transform(data['Churn'])

    X = data.drop('Churn', axis=1)
    y = data['Churn']
    X = pd.get_dummies(X, columns=['State'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    smote_enn = SMOTEENN(random_state=42)
    model = RandomForestClassifier(random_state=42)
    pipeline = ImbPipeline(steps=[
        ('smote_enn', smote_enn),
        ('classifier', model)
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print(f"Classification Report:\n{classification_report(y_test, y_pred)}")
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

def save_model(model, filename="model.pkl"):
    joblib.dump(model, filename)

def load_model(filename="model.pkl"):
    return joblib.load(filename)

