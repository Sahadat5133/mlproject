import sys
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:

    def get_data_transformer_object(self):
        try:
            # Only numerical input features
            numerical_columns = ["reading_score", "writing_score"]

            # Categorical input features
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            # Numerical pipeline
            num_pipeline = Pipeline(
                steps=[("scaler", StandardScaler())]
            )

            # Categorical pipeline
            cat_pipeline = Pipeline(
                steps=[("one_hot_encoder", OneHotEncoder(handle_unknown='ignore'))]
            )

            logging.info(f"Numerical columns: {numerical_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")

            # ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Load train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info(f"Train columns: {train_df.columns.tolist()}")
            logging.info(f"Test columns: {test_df.columns.tolist()}")

            target_column_name = "math_score"

            # Split input features and target
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            # Get preprocessing object
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Applying preprocessing to training and testing data")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine features with target
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Save preprocessor
            save_object(
                file_path=DataTransformationConfig.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info(f"Preprocessor saved at {DataTransformationConfig.preprocessor_obj_file_path}")

            return train_arr, test_arr, DataTransformationConfig.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)
