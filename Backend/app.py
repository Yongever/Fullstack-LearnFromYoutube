from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Set OpenAI API key (replace with your key)
openai.api_key = "Your API"

@app.route("/")
def home():
    return "Welcome to the YouTube Transcript Q&A App! Use http://127.0.0.1:5000/transcript?video_url=YOUTUBE URL."

@app.route('/transcript', methods=['GET'])
def get_transcript():
    """
    Endpoint to fetch the transcript of a YouTube video.
    """
    video_url = request.args.get('video_url')
    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400

    try:
        # Extract video ID from URL
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({"transcript": transcript})
    except Exception as e:
        return jsonify({"error": f"Error fetching transcript: {str(e)}"}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Endpoint to answer a question based on the transcript.
    """
    data = request.json
    video_url = data.get('video_url')
    question = data.get('question')

    if not video_url or not question:
        return jsonify({"error": "Video URL and question are required"}), 400

    try:
        # Extract video ID from URL
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript])

        # Use OpenAI GPT to answer the question
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"The following is a transcript of a video:\n{transcript_text}\n\nAnswer the question: {question}",
            max_tokens=200
        )

        answer = response.choices[0].text.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"message": "Backend is connected!"})

if __name__ == '__main__':
    app.run(debug=True)
