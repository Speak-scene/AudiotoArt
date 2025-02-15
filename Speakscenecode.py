import gradio 
import openai
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Set OpenAI API key
openai.api_key = "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"

def chatgpt_api(input_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    if input_text:
        messages.append(
            {"role": "user", "content": 'Summarize this text "{}" into a short and concise Dall-e2 prompt'.format(input_text)},
        )
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    
    reply = chat_completion.choices[0].message.content
    return reply

def dall_e_api(dalle_prompt):
    dalle_response = openai.Image.create(
        prompt=dalle_prompt,
        size="512x512"
    )
    image_url = dalle_response['data'][0]['url']
    return image_url

def whisper_transcribe(audio):
    new_audio_path = audio + '.wav'
    os.rename(audio, new_audio_path)
    with open(new_audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    dalle_prompt = chatgpt_api(transcript["text"])
    image_url = dall_e_api(dalle_prompt)
    return transcript["text"], image_url

# Define the Gradio interface
output_1 = gradio.Textbox(label="Speech to Text")
output_2 = gradio.Image(label="DALL-E Image")
speech_interface = gradio.Interface(fn=whisper_transcribe, inputs=gradio.Audio(type="filepath"), 
    outputs=[output_1, output_2], 
    title="Generate Images using Voice")
speech_interface.launch(debug=True)