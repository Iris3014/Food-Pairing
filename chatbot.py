from flask import Flask, render_template, request, jsonify
import requests
import re  

app = Flask(__name__)

OPENROUTER_API_KEY = "your_api_key"
YOUTUBE_API_KEY = "your_api_key"

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
@app.route("/index2")
def index2():
    return render_template("index2.html")


@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"].lower()

        if not OPENROUTER_API_KEY:
            return jsonify({"reply": "⚠️ OpenRouter API key is missing or incorrect!"})

        openrouter_reply = get_openrouter_response(user_message)

        food_keywords = ["recipe", "cooking", "food video", "how to cook", "dish", "baking"]
        youtube_links = ""
        if any(keyword in user_message for keyword in food_keywords):
            youtube_links = fetch_youtube_videos(user_message)
            final_reply = f"{openrouter_reply}\n\n🍽️ <b>Related Videos:</b><br>{youtube_links}"
        else:
            final_reply = openrouter_reply

        return jsonify({"reply": final_reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

def get_openrouter_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot. Answer user questions. If they ask for food recipes, provide them."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
    response_data = response.json()

    if "choices" in response_data and response_data["choices"]:
        return response_data["choices"][0]["message"]["content"]
    else:
        return "⚠️ No valid response from OpenRouter API."

def fetch_youtube_videos(query):
    params = {
        "part": "snippet",
        "q": query + " recipe",
        "key": YOUTUBE_API_KEY,
        "maxResults": 3,
        "type": "video"
    }
    
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = response.json()

    video_links = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_links.append(f"📌 {video_title}: <a href='{video_url}' target='_blank'>Watch Here</a>")

    return "<br>".join(video_links) if video_links else "⚠️ No videos found."

if __name__ == "__main__":
    app.run(debug=True, port=5002)

