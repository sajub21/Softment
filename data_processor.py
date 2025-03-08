import os 
import pandas as pd
import json 

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = self.detect_file_type()
    
    
    def detect_file_type(self):
        _, ext = os.path.splitext(self.file_path)  # ✅ Correct: self.file_path
        return ext.lower()
    
    
    def process(self):
        if self.file_type == ".text":
            return self.process_text()
        elif self.file_type == ".csv":
            return self.process_csv()
        elif self.file_type == ".json":
            return self.process_json()
        else:
            return "Unsupported file format"
    
    
    def process_text(self):
        with open(self.file_path, 'r', encoding="utf-8") as file:
            text = file.read()
        word_count = len(text.split())
        line_count = text.count('\n') + 1
        return f"Text file: {word_count} words, {line_count} lines"
    
    
    def process_csv(self):
        df = pd.read_csv(self.file_path)
        return df.describe(include="all").to_string()
    
    
    def process_json(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list): #If Json is a list of records
            df = pd.DataFrame(data)
            return df.describe(include="all").to_string()
        else:
            return f"JSON keys: {list(data.keys())}"
        
#Example usage
file_path = input("Enter file path:  ")
processor = DataProcessor(file_path)
result = processor.process()
print(result)

#Optional: Save output to a new file
with open("output.txt", "w", encoding="utf-8") as output_file:
    output_file.write(result)