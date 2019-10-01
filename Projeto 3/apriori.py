import pandas as pd
from sklearn.metrics import cohen_kappa_score

#movies = pd.read_table("ml-1m/movies.dat", sep="::", names=['MovieID', 'Title', 'Genres'], engine='python')
#users = pd.read_table("ml-1m/users.dat", sep="::", names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], engine='python')
ratings = pd.read_table("ml-1m/ratings.dat", sep="::", names=['UserID', 'MovieID', 'Rating', 'Timestamp'], engine='python')

movie_ratings = ratings[ratings.MovieID == 1193].iloc[:,2]

# Movie Truncated Mean

print(int(movie_ratings.mean()))

# Movie Mode

#print(movie_ratings.value_counts())
print(movie_ratings.mode()[0])

# Hit Rate

y3 = pd.DataFrame({'A':y1,'B':y2})
len(y3[y3.A == y3.B].index)

# Confusion Matrix

y_actu = pd.Series(y1, name='Actual')
y_pred = pd.Series(y2, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)

# RMSE

((y1 - y2) ** 2).mean() ** .5

# Cohen's Kappa

sklearn.metrics.cohen_kappa_score(y1, y2)