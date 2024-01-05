import os
import json
import PyPDF2
import traceback
import pandas as pd
from dotenv import load_dotenv

import streamlit as st
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.MCQGenerator import generate_evaluate_chain


#loading json file
with open("E:/Programming Files/DataScience/ineuron-mcq-generator/mcq-generator/response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQ Generator Application with Langchain ")

#create a form using st.form
with st.form('user_inputs'):
    #File upload
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    #input fields
    mcq_count = st.number_input('No of MCQs : ', min_value=3, max_value=50)

    #Subject
    subject = st.text_input('Insert Subject', max_chars= 25)

    #Quiz Tone
    quiz_tone = st.text_input('Insert Complexity',max_chars= 25)

    #Submit button
    button = st.form_submit_button(label='Create MCQs')

#check if the button is clicked and all fields are filled
if button and uploaded_file and mcq_count and subject and quiz_tone:
    
    with st.spinner("Generating MCQs..."):
        try:
            #read the file
            text = read_file(uploaded_file)

            #generate the MCQs
            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": quiz_tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                }
                )

            

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error generating MCQs. Please try again.")

        else:
            st.success("MCQs generated successfully!")
            
            if isinstance(response, dict):
                #extract the questions from the generated MCQs
                quiz = response.get("quiz")
                # Find the index of the opening curly brace
                start_index = quiz.find('{')

                # Find the index of the closing curly brace
                end_index = quiz.rfind('}')

                # Extract the JSON string from the original string
                quiz_json = quiz[start_index:end_index + 1]
                
                

                if quiz is not None:
                    #convert the questions to a dataframe
                    quiz_table_data = get_table_data(quiz)
                    if quiz_table_data:
                        df = pd.DataFrame(quiz_table_data)
                        df.index = df.index + 1
                        st.table(df)
                        st.text_area(label='Review',value=response['review'],height=200)
                    else:
                        st.error("Error parsing MCQs. Please try again.")

            else:
                st.write(response)




    
