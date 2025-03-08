import os
import pandas as pd
import json

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = self.detect_file_type()
    
    
    def detect_file_type(self):
        _, ext = os.path.splitext(self.file_path)
        return ext.lower()
    
    
    def process(self):
        """Main method to preocess diffrent file types with error handling."""
        if not os.path.exists(self.file_path):
            return "Error: File not found. Please check the path."
        
        
        try:
            if self.file_type == ".text":
                return self.process_text()
            elif self.file_type == ".csv":
                return self.process_csv()
            elif self.file_type == ".json":
                return self.process_json()
            else:
                return "Error: Unsupported file format. Use .text, .csv, .json."
        except Exception as e:
            return f"Error while processing file: {str(e)}"
        
        
    def process_csv(self):
        """Reads a CSV file and return summary statistics."""
        try:
            df = pd.read_csv(self.file_path)
            return df.describe(include='all').to_string()
        except pd.error.EmptyDataError:
            return "Error: CSV file is empty."
        except pd.errors.ParserError:
            return "Error: CSV file is malinformed (check formatting.)"
        except Exception as e:
            return f"Error processing CSV file: {str(e)}"
        
        
    def process_json(self):
        """Read a JSON file and extracts key statistics or convert it to a DataFrame."""
        try:
            with open(self.file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                
            if isinstance(data, list):
                df = pd.DataFrame(data)
                return df.describe(include="all").to_string()
            else:
                return f"JSON keys: {list(data.keys())}"
        except json.JSONDecodeError:
            return "Error: JSON file is malformed (check syntax)."
        except Exception as e:
            return f'Error processing JSON file: {str(e)}'
        
        
# Example usage:
file_path = input('Enter file path: ')
processor = DataProcessor(file_path)
result = processor.process()
print(result)

#Optional: save output to a new file
output_file = "output.txt"
try:
    with open(output_file, "w", encoding='utf-8') as file:
        file.write(result)
    print(f"Processing data saved to {output_file}")
except Exception as e:
    print(f"Error saving output file: {str(e)}")