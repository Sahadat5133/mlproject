import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "raw.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    preprocessor_obj_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion process")

        try:
            # READ RAW DATA
            df = pd.read_csv(r"K:\mlproject\notebook\stud.csv")
            logging.info("Raw dataset loaded successfully")

            # Create artifacts directory if it doesn't exist
            os.makedirs("artifacts", exist_ok=True)

            # Save raw CSV
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info(f"Raw data saved at {self.ingestion_config.raw_data_path}")

            # TRAIN/TEST SPLIT
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save train/test CSVs
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Train-test split completed and saved.")

            # ===============================
            # Apply Data Transformation
            # ===============================
            logging.info("Starting data transformation (preprocessing)...")
            data_transformation = DataTransformation()
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

            logging.info(f"Preprocessing completed. Preprocessor saved at {preprocessor_path}")

            return train_arr, test_arr, preprocessor_path

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_arr, test_arr, preprocessor_path = obj.initiate_data_ingestion()
    print(f"Data ingestion and transformation completed successfully.\nPreprocessor path: {preprocessor_path}")
