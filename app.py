# URL To YoutubeID
from urllib.parse import urlparse

def get_yt_video_id(url):

    from urllib.parse import urlparse, parse_qs

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError
        
# Transcription and text formatting
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def transcribe(youtubeId):
    transcription = YouTubeTranscriptApi.get_transcript(youtubeId)
    return transcription

formatter = TextFormatter()

def transcriptToText(transcript):
  text = formatter.format_transcript(transcript)
  text = text.replace("\n", " ")
  return text

# Summary using OpenAI API
import openai

def textToSummary(text,OpenAIkey):
  openai.api_key = OpenAIkey
  response = openai.Completion.create(
      model="text-davinci-003",
      prompt= "Summarize this in 200 words or less:\n\n" + text,
      temperature=0.7,
      max_tokens=400,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=1
      )
  return response["choices"][0]["text"].replace("\n", " ").strip()

def summarize(url,OpenAIkey):
  videoId = get_yt_video_id(url)
  transcript = transcribe(videoId)
  text = transcriptToText(transcript)
  summary = textToSummary(text,OpenAIkey)
  return summary

# Gradio Setup
import gradio as gr

description = "Enter a link for a YouTube video you want summarized"

gr.Interface(fn=summarize,
             inputs=["text", "text"],
             outputs=["textbox"], 
             description=description
            ).launch()
