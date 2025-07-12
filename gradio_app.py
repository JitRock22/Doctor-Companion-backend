from brain import encode_img,analyze_img_with_query
from voice_patient import record_audio,transcribe_with_groq
from voice_doctor import text_to_speech_with_gtts

import os
import gradio as gr

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(
    stt_model="whisper-large-v3",
    audio_file_path=audio_filepath,
    GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
)

    # Handle the image input
    if image_filepath:
        # doctor_response = analyze_img_with_query(query=system_prompt+speech_to_text_output, encoded_img=encode_img(image_filepath), model="meta-llama/llama-4-maverick-17b-128e-instruct") #model="meta-llama/llama-4-maverick-17b-128e-instruct") 
        doctor_response = analyze_img_with_query(
        query=system_prompt + speech_to_text_output,
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        encoded_img=encode_img(image_filepath)
)

    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath_mp3="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


custom_css = """
body { background-color: #0f0f0f; font-family: 'Segoe UI', sans-serif; }
h1, .gr-textbox label, .gr-audio label { color: #f5f5f5 !important; }
.gradio-container { max-width: 1000px; margin: auto; padding: 20px; border-radius: 15px; }
.gr-box { background-color: #1f1f1f !important; border-radius: 12px !important; }
.gr-button { background: #6a5acd !important; color: white !important; border: none !important; }
"""


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath",label="🎤 Speak your Symptoms"),
        gr.Image(type="filepath",label="🖼️ Upload Your Image")
    ],
    outputs=[
        gr.Textbox(label="📝 Speech Transcription"),
        gr.Textbox(label="👨‍⚕️ Doctor's Response"),
        # gr.Audio("Temp.mp3")
        gr.Audio(type="filepath", label="🎧 Doctor's Voice (Click ▶️ to replay)")
    ],
    title="🩺 AI Doctor Assistant",
    theme="soft",
    css=custom_css

)

# iface.launch(debug=True)

port = int(os.environ.get("PORT", 7860))  # Render sets PORT env variable
iface.launch(
    server_name="0.0.0.0", 
    server_port=port,
    show_error=True, 
    debug=True
)



#http://127.0.0.1:7860


