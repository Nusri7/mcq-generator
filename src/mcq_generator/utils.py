import os
import json
import PyPDF2
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdfReader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdfReader.pages:
                text += page.extractText()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8") 
    
    else:
        raise Exception("File type not supported. Please upload a .txt or .pdf file.")
    
def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key,value in quiz_dict.items():
            mcq = value["mcq"]
            options = " | ".join([f"{option}: {option_value}" for option, option_value in value["options"].items()])
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

            
        
