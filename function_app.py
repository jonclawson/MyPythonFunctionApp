import azure.functions as func
import logging
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HelloWorldPyFunc")
def HelloWorldPyFunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        songs = generate_song_content('Can you return 20 songs I might like (formatted in the JSON pattern of ["song by artist", ...] with no other information before or after) by artists I might like if I like the artist of the song:  ', name)
        songs_json = json.loads(songs)
        logging.info("there are " + str(len(songs_json)) + " songs")
        return func.HttpResponse(f"Similar songs to, {name}. {songs}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# Function to generate song-related content using OpenAI's GPT-3
def generate_song_content(prompt, subject):
    openai_key = os.environ.get('OPENAI_API_KEY')

    prompt = f"{prompt}: {subject}."
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        # api_key=openai_key,
    )
    logging.info('running request to openai')
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    content = response.choices[0].message.content
    logging.info('response returned from openai ' + content)
    return content