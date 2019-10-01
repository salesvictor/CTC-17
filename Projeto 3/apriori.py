import pandas as pd
from sklearn.metrics import cohen_kappa_score

y1 = [5,5,5,4,4,4,3,2,1,1]
y2 = [4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0]

# Hit Rate

y3 = pd.DataFrame({'A':y1,'B':y2})
print(len(y3[y3.A == y3.B].index)/len(y1))

# Confusion Matrix

y_actu = pd.Series(y1, name='Actual')
y_pred = pd.Series(y2, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)
print(df_confusion)

# RMSE
RMSE = 0
for i in range(len(y1)):
	RMSE += (y1[i] - y2[i]) ** 2
print((RMSE/len(y1)) ** .5)

# Cohen's Kappa

print(sklearn.metrics.cohen_kappa_score(y1, y2))