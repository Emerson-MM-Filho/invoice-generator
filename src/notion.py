import requests


def query_database(database_id, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    payload = {"page_size": 100}

    response = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        json=payload,
        headers=headers,
    )

    response.raise_for_status()
    return response.json()


def parse_select_value(prop):
    return prop["select"]["name"]


def parse_multi_select_value(prop):
    return [item["name"] for item in prop["multi_select"]]


def parse_title_value(prop):
    return prop["title"][0]["text"]["content"]


def parse_email_value(prop):
    return prop["email"]


def parse_date_value(prop):
    return prop["date"]


def parse_rich_text_value(prop):
    return prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else None


def parse_url_value(prop):
    return prop["url"]


def parse_unique_id_value(prop):
    prefix = prop["unique_id"]["prefix"]
    number = prop["unique_id"]["number"]
    return f"{prefix or ''}{number}"
