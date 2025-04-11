import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@postgres:5432/fintech')
df = pd.read_sql('SELECT * FROM stocks', engine)

# Preprocesamiento
df['Target'] = df.groupby('Ticker')['Price'].shift(-5)  # Precio en 5 días
df.dropna(inplace=True)

X = df[['Price', 'Daily_Return']]
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)
print(f"Precisión: {model.score(X_test, y_test):.2%}")