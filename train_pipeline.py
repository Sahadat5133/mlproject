import os
import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor

# Load data
data = pd.read_csv(r"K:\mlproject\notebook\stud.csv")
X = data.drop("math_score", axis=1)
y = data["math_score"]

# Define categorical and numerical columns
categorical_cols = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
numerical_cols = ['reading_score','writing_score']

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
        ('num', StandardScaler(), numerical_cols)
    ]
)

# Fit preprocessor and transform data
X_preprocessed = preprocessor.fit_transform(X)

# Train model
model = RandomForestRegressor()
model.fit(X_preprocessed, y)

# Save artifacts
os.makedirs("artifacts", exist_ok=True)
with open("artifacts/preprocessor.pkl", "wb") as f:
    pickle.dump(preprocessor, f)
with open("artifacts/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Training complete. Model and preprocessor saved in artifacts/")
