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


if __name__ == "__main__":
    from client import Address, Client, Contract
    from env import Env

    ENV = Env()

    database_id = ENV.NOTION.CLIENTS_DATABASE_ID
    token = ENV.NOTION.INTEGRATION_SECRET

    response = query_database(database_id, token)
    for result in response["results"]:
        props = result["properties"]

        client_data = dict()
        for key, value in props.items():
            if value["type"] == "select":
                client_data[key] = parse_select_value(value)
            elif value["type"] == "multi_select":
                client_data[key] = parse_multi_select_value(value)
            elif value["type"] == "title":
                client_data[key] = parse_title_value(value)
            elif value["type"] == "email":
                client_data[key] = parse_email_value(value)
            elif value["type"] == "date":
                client_data[key] = parse_date_value(value)
            elif value["type"] == "rich_text":
                client_data[key] = parse_rich_text_value(value)
            elif value["type"] == "url":
                client_data[key] = parse_url_value(value)
            elif value["type"] == "unique_id":
                client_data[key] = parse_unique_id_value(value)

        client = Client(
            id_=result["id"],
            name=client_data["Name"],
            website=client_data["Website"],
            google_drive_folder_id=client_data["Google Drive - Folder ID"],
            gov_id=client_data["Gov ID (CNPJ)"],
            type_=client_data["Type"],
            contract=Contract(
                start=client_data["Contract Date"]["start"],
                end=client_data["Contract Date"]["end"],
            ),
            address=Address(
                city=client_data["City"],
                country=client_data["Country"],
                state=client_data["State"],
                postal_code=client_data["Postal Code"],
                address=client_data["Address"],
                district=client_data["District"],
            ),
        )
