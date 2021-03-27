import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

dataset = pd.read_csv('phishing_url.csv')
features = dataset.iloc[:,0:9].values
label = dataset.iloc[:,[9]].values
X_train, X_test, y_train, y_test = train_test_split(features, label, test_size = 0.25,  random_state = 67)
classifier=RandomForestClassifier(n_estimators=100)
classifier.fit(X_train,y_train.ravel())
y_pred=classifier.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
# feature_imp = pd.Series(classifier.feature_importances_, index = dataset.columns[0:21]).sort_values(ascending=False)
# print(feature_imp)