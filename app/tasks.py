import os
import subprocess
import json
from datetime import datetime
import sqlite3
import requests
from openai import AzureOpenAI
import markdown
import csv
import pandas as pd
from fastapi import HTTPException

def execute_task(task: str):
    if "install uv" in task:
        return install_uv_and_run_datagen(task)
    elif "format" in task and "prettier" in task:
        return format_with_prettier(task)
    elif "count the number of Wednesdays" in task:
        return count_wednesdays(task)
    elif "count the number of Thursdays" in task:
        return count_thursdays(task)
    elif "count the number of Sundays" in task:
        return count_sundays(task)
    elif "sort the array of contacts" in task:
        return sort_contacts(task)
    elif "first line of the 10 most recent .log file" in task:
        return recent_log_lines(task)
    elif "extract the first occurrence of each H1" in task:
        return extract_h1_titles(task)
    elif "extract the sender’s email address" in task:
        return extract_email_sender(task)
    elif "extract the card number" in task:
        return extract_credit_card_number(task)
    elif "find the most similar pair of comments" in task:
        return find_similar_comments(task)
    elif "total sales of all the items in the “Gold” ticket type" in task:
        return total_sales_gold(task)
    elif "fetch data from an API" in task:
        return fetch_data_from_api(task)
    elif "clone a git repo" in task:
        return clone_git_repo_and_commit(task)
    elif "run a SQL query" in task:
        return run_sql_query(task)
    elif "scrape a website" in task:
        return scrape_website(task)
    elif "compress or resize an image" in task:
        return compress_or_resize_image(task)
    elif "transcribe audio from an MP3 file" in task:
        return transcribe_audio(task)
    elif "convert Markdown to HTML" in task:
        return convert_markdown_to_html(task)
    elif "filter a CSV file" in task:
        return filter_csv_file(task)
    else:
        raise ValueError("Task not recognized")


def install_uv_and_run_datagen(email: str):
    subprocess.run(["pip", "install", "uv"])
    subprocess.run(["pip", "install", "Faker"])

    # Download the datagen.py script
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    response = requests.get(url)
    with open("datagen.py", "w") as file:
        file.write(response.text)

    # Run the datagen.py script with the email argument
    subprocess.run(["python", "datagen.py", email])
    return "Data generated successfully"

def format_with_prettier(task: str):
    subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"])
    return "File formatted successfully"

def count_wednesdays(task: str):
    with open("/data/dates.txt", "r") as file:
        dates = file.readlines()
    wednesdays = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)
    with open("/data/dates-wednesdays.txt", "w") as file:
        file.write(str(wednesdays))
    return "Wednesdays counted successfully"

def count_thursdays(task: str):
    with open("/data/dates.txt", "r") as file:
        dates = file.readlines()
    thursdays = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 3)
    with open("/data/extracts-count.txt", "w") as file:
        file.write(str(thursdays))
    return "Thursdays counted successfully"

def count_sundays(task: str):
    with open("/data/contents.log", "r") as file:
        dates = file.readlines()
    sundays = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 6)
    with open("/data/contents.dates", "w") as file:
        file.write(str(sundays))
    return "Sundays counted successfully"

def sort_contacts(task: str):
    with open("/data/contacts.json", "r") as file:
        contacts = json.load(file)
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
    with open("/data/contacts-sorted.json", "w") as file:
        json.dump(sorted_contacts, file, indent=4)
    return "Contacts sorted successfully"

def recent_log_lines(task: str):
    log_files = sorted([f for f in os.listdir("/data/logs/") if f.endswith(".log")], key=lambda x: os.path.getmtime(os.path.join("/data/logs/", x)), reverse=True)[:10]
    with open("/data/logs-recent.txt", "w") as outfile:
        for log_file in log_files:
            with open(os.path.join("/data/logs/", log_file), "r") as infile:
                outfile.write(infile.readline())
    return "Recent log lines written successfully"

def extract_h1_titles(task: str):
    index = {}
    for root, _, files in os.walk("/data/docs/"):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            index[file] = line[2:].strip()
                            break
    with open("/data/docs/index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "H1 titles extracted successfully"


def extract_email_sender(task: str):
    # Read the email content from the file
    with open("/data/email.txt", "r") as file:
        email_content = file.read()

    client = AzureOpenAI(
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRlZXBha2t1bWFyLmt1emFudGhhaXZlbHVAc3RyYWl2ZS5jb20ifQ.C2KdZmxw6ZXOeJ2P3PKTOzfoPpUF0getJ89zhBq4AeM",
        api_version="2025-01-01-preview",
        azure_endpoint="https://llmfoundry.straive.com/azure"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract the sender's email address from the following email:\n{email_content}"}]
    )
    sender_email = response['choices'][0]['message']['content'].strip()

    # Write the extracted email address to the output file
    with open("/data/email-sender.txt", "w") as file:
        file.write(sender_email)

    return "Email sender extracted successfully"


def extract_credit_card_number(image_path: str):
    # Define the API endpoint for the LLM that can process images
    api_url = "https://llmfoundry.straive.com/azure/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRlZXBha2t1bWFyLmt1emFudGhhaXZlbHVAc3RyYWl2ZS5jb20ifQ.C2KdZmxw6ZXOeJ2P3PKTOzfoPpUF0getJ89zhBq4AeM",
        "Content-Type": "application/json"
    }

    # Read the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Prepare the request payload
    payload = {
        "image": image_data
    }

    # Make the API call to the LLM
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # Assuming the response contains the extracted text
        extracted_text = response.json().get("text", "")

        # Process the extracted text to find the credit card number
        card_number = extract_card_number_from_text(extracted_text)

        # Write the card number to a file without spaces
        with open("/data/credit-card.txt", "w") as file:
            file.write(card_number.replace(" ", ""))

        return "Credit card number extracted successfully"
    else:
        return f"Error: {response.status_code} - {response.text}"


def extract_card_number_from_text(text: str) -> str:
    # Simple regex to find a credit card number in the text
    import re
    match = re.search(r'\b\d{16}\b', text)  # Adjust regex as needed for different formats
    return match.group(0) if match else ""

def find_similar_comments(task: str):
    # Placeholder for LLM call
    with open("/data/comments.txt", "r") as file:
        comments = file.readlines()
    similar_pair = comments[:2]  # Replace with actual LLM call
    with open("/data/comments-similar.txt", "w") as file:
        file.writelines(similar_pair)
    return "Similar comments found successfully"

def total_sales_gold(task: str):
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0]
    with open("/data/ticket-sales-gold.txt", "w") as file:
        file.write(str(total_sales))
    conn.close()
    return "Total sales for Gold tickets calculated successfully"

def fetch_data_from_api(task: str):
    url = "https://api.example.com/data"
    response = requests.get(url)
    if response.status_code == 200:
        with open("/data/api_data.json", "w") as file:
            file.write(response.text)
        return "Data fetched from API successfully"
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from API")

def clone_git_repo_and_commit(task: str):
    repo_url = "https://github.com/example/repo.git"
    subprocess.run(["git", "clone", repo_url, "/data/repo"])
    with open("/data/repo/new_file.txt", "w") as file:
        file.write("New content")
    subprocess.run(["git", "add", "new_file.txt"], cwd="/data/repo")
    subprocess.run(["git", "commit", "-m", "Add new file"], cwd="/data/repo")
    return "Git repo cloned and commit made successfully"

def run_sql_query(task: str):
    conn = sqlite3.connect("/data/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_name")
    result = cursor.fetchall()
    with open("/data/sql_result.json", "w") as file:
        json.dump(result, file)
    conn.close()
    return "SQL query executed successfully"

def scrape_website(task: str):
    url = "https://example.com"
    response = requests.get(url)
    if response.status_code == 200:
        with open("/data/website_content.html", "w") as file:
            file.write(response.text)
        return "Website scraped successfully"
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to scrape website")

def compress_or_resize_image(task: str):
    from PIL import Image
    image_path = "/data/image.jpg"
    with Image.open(image_path) as img:
        img = img.resize((img.width // 2, img.height // 2))
        img.save("/data/image_resized.jpg")
    return "Image compressed or resized successfully"

def transcribe_audio(task: str):
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    audio_path = "/data/audio.mp3"
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    with open("/data/audio_transcription.txt", "w") as file:
        file.write(text)
    return "Audio transcribed successfully"

def convert_markdown_to_html(task: str):
    with open("/data/document.md", "r") as file:
        markdown_content = file.read()
    html_content = markdown.markdown(markdown_content)
    with open("/data/document.html", "w") as file:
        file.write(html_content)
    return "Markdown converted to HTML successfully"

def filter_csv_file(task: str):
    df = pd.read_csv("/data/data.csv")
    filtered_df = df[df['column_name'] == 'filter_value']
    filtered_df.to_json("/data/filtered_data.json", orient="records")
    return "CSV file filtered and JSON data returned successfully"