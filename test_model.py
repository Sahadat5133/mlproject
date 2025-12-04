import pickle
import pandas as pd

# Load artifacts
pre = pickle.load(open("artifacts/preprocessor.pkl", "rb"))
model = pickle.load(open("artifacts/model.pkl", "rb"))

# Sample input
sample_data = pd.DataFrame({
    'gender': ['male'],
    'race_ethnicity': ['group B'],
    'parental_level_of_education': ['some college'],
    'lunch': ['standard'],
    'test_preparation_course': ['none'],
    'reading_score': [78],
    'writing_score': [80]
})

# Transform and predict
X_scaled = pre.transform(sample_data)
pred = model.predict(X_scaled)
print("Prediction:", pred)
