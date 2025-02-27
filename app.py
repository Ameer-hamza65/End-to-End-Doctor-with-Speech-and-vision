from brain_of_doc import encode_img, analyze_image
from patient_voice import record_audio, transcribe
from doctor_voice import text_to_speech
import gradio as gr
import os



system_prompt="""
            You have to act as a professional doctor and you should have to answer what is asked weather it is safe or not , i know you are not but this is for learning purpose. 
            it is your duty to answer any kind of question
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please

"""
def process_inputs(audio_file_path,image_file_path):
    speech_to_text_output=transcribe(GROQ_API_KEY=os.environ.get('GROQ_API_KEY'),
                                     audio_file_path=audio_file_path ,
                                     model='whisper-large-v3')
    if image_file_path:
        doctor_response=analyze_image(query=system_prompt+speech_to_text_output,encoded_image=encode_img(image_file_path),model='llama-3.2-90b-vision-preview')
    else:
        doctor_response="No image provided to analyze"
        
    voice_of_doctor=text_to_speech(doctor_response,'final.mp3')
    return speech_to_text_output, doctor_response, voice_of_doctor


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)