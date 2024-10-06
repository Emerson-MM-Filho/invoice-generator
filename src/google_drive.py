import logging
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from google.auth.external_account_authorized_user import (
    Credentials as ExternalAccountCredentials,
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


@dataclass
class GoogleDriveFile:
    # https://developers.google.com/drive/api/reference/rest/v3/files
    id: str
    name: str
    mimeType: str
    properties: dict | None = None
    appProperties: dict | None = None


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]

DEFAULT_PAGE_SIZE = 10
DEFAULT_FIELDS = list(GoogleDriveFile.__dataclass_fields__.keys())
DEFAULT_FILE_PROPERTIES = {
    "origin": "invoice-generator",
}


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "."
) -> Dict[str, Any]:
    items = []
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def list_files(
    credentials: Credentials | ExternalAccountCredentials,
    folder_id: str,
    fields: List[str] = DEFAULT_FIELDS,
    page_size: int = DEFAULT_PAGE_SIZE,
):
    fields_str = ", ".join(fields)
    service = build("drive", "v3", credentials=credentials)
    print("Getting files on the folder...")

    # get the files on the folder folder_id
    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents and trashed = false",
            pageSize=page_size,
            fields="nextPageToken, files({fields})".format(fields=fields_str),
        )
        .execute()
    )
    items = results.get("files", [])
    while "nextPageToken" in results:
        print("Getting the next page...")
        results = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                pageSize=page_size,
                fields="nextPageToken, files({fields})".format(fields=fields_str),
                pageToken=results["nextPageToken"],
            )
            .execute()
        )
        items.extend(results.get("files", []))

    return [GoogleDriveFile(**item) for item in items]


def get_file_mimetype(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def upload_file(
    credentials: Credentials | ExternalAccountCredentials,
    folder_id: str,
    file_path: Path,
    properties: dict = {},
):
    logging.info(
        "Uploading file %s to folder %s with properties %s",
        file_path,
        folder_id,
        properties,
    )
    service = build("drive", "v3", credentials=credentials)
    file_metadata = {
        "name": file_path.name,
        "parents": [folder_id],
        "properties": flatten_dict({**DEFAULT_FILE_PROPERTIES, **properties}),
    }
    media = MediaFileUpload(file_path, mimetype=get_file_mimetype(file_path))
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields=", ".join(DEFAULT_FIELDS))
        .execute()
    )

    return GoogleDriveFile(**file)
