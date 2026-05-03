import csv
from config import PREDICTIONS_CSV

class CSVWriter:
    def __init__(self):
        self.csv_file = PREDICTIONS_CSV
        self.headers = ["Issue", "Subject", "Company", "Response", "Product Area", "Status", "Request Type", "Justification"]
        
        # Initialize the CSV with headers if it doesn't exist
        if not self.csv_file.exists():
            with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    def write_prediction(self, issue, subject, company, response, status, request_type, product_area, justification):
        # Remove newlines from response to keep CSV clean
        safe_response = response.replace("\n", " ").replace("\r", " ")
        
        with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([issue, subject, company, safe_response, product_area, status, request_type, justification])

csv_writer = CSVWriter()
