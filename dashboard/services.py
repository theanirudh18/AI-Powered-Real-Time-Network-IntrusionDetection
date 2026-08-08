"""
==========================================================
Dashboard Services
==========================================================
"""

from pathlib import Path

from werkzeug.utils import secure_filename

import config

from dashboard.predictor import Predictor


class PredictionService:

    def __init__(self):

        self.predictor = Predictor()

    # ======================================================
    # CHECK CSV
    # ======================================================

    @staticmethod
    def allowed_file(filename):

        return filename.lower().endswith(".csv")

    # ======================================================
    # SAVE FILE
    # ======================================================

    def save_upload(self, file):

        filename = secure_filename(file.filename)

        save_path = config.UPLOAD_DIR / filename

        file.save(save_path)

        return save_path

    # ======================================================
    # PREDICT
    # ======================================================

    def predict(self, uploaded_file):

        if uploaded_file.filename == "":

            raise ValueError("No file selected.")

        if not self.allowed_file(uploaded_file.filename):

            raise ValueError("Only CSV files are allowed.")

        csv_path = self.save_upload(uploaded_file)

        summary, prediction_file = self.predictor.predict(

            csv_file=str(csv_path),

            output_folder=str(config.RESULT_DIR)

        )

        return {

            "filename": csv_path.name,

            "prediction_file": Path(prediction_file).name,

            "summary": summary

        }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    service = PredictionService()

    print("======================================")
    print(" Dashboard Service Loaded ")
    print("======================================")