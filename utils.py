from config import OPENAI_ORGANIZATION, OPENAI_API_KEY
from database import add_record
from datetime import datetime
from config import ALLOWED_EXTENSIONS
import openai
import re

openai.organization = OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY


def extract_number(text):
    match = re.search('\d+', text)
    if match:
        return int(match.group())
    return 0


def extract_datetime_microseconds(filename):
    pattern = r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{6})"
    match = re.match(pattern, filename)

    if not match:
        raise ValueError("Invalid filename format")

    year, month, day, hour, minute, second, microseconds = [
        int(x) for x in match.groups()]
    dt = datetime(year, month, day, hour, minute, second, microseconds)

    return dt


def transcribe_and_extract_agreement_price(input_file):
    with open(input_file, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    query_price = f"""
    transcript of a phone call with a client:

    '{transcript["text"]}'

    what is the agreement price mentioned in this conversation?
    Please just say an integer, don't explain.
    if this conversation doesn't mention the total price, write 0
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query_price}
        ]
    )

    response = completion.choices[0].message['content']
    aggreement_price = extract_number(response)

    date = extract_datetime_microseconds(input_file.split('/')[1])

    record_id = add_record(
        date, input_file, transcript["text"], aggreement_price)

    print(f"Record added with ID {record_id}")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
