#!/usr/bin/env python
# coding: utf-8

# In[2]:


import base64
import email
import json
import pickle
from apiclient import errors
from datetime import datetime, date
from pathlib import Path
import mailparser

from google.oauth2 import service_account
from googleapiclient.discovery import build


# ## Setup service account
#
# Service account setup is a bit convoluted.
#
# Here's some guidance from Stackoverflow: https://stackoverflow.com/questions/24779138/can-we-access-gmail-api-using-service-account
#
# Google's own description: https://developers.google.com/api-client-library/python/auth/service-accounts Don't forget to activate site wide permissions.
#
# Final step is to turn on scopes for the client: https://admin.google.com/mybusinessautomated.com/AdminHome?chromeless=1#OGX:ManageOauthClients

# In[3]:


# ## Instructions

# Follow the instructions on this page to create a credentials.json file:

# https://developers.google.com/gmail/api/quickstart/python

# Remember to put it into the right project on https://console.developers.google.com


# In[4]:


# If modifying these scopes, delete the file token.pickle.
# def establish_desktop_service():
#     SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
#     folder = Path.cwd()
#     pf = folder / 'token.pickle'
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if pf.exists():
#         token = pf.read_bytes()
#         creds = pickle.loads(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'desktop_credentials.json', SCOPES)
#             creds = flow.run_local_server()
#         # Save the credentials for the next run
#         pf.write_bytes(pickle.dumps(creds))

#     service = build('gmail', 'v1', credentials=creds)
#     return service


# In[6]:


def establish_server_credentials(credentials_json, user_email):
    secrets = credentials_json
    scopes = ["https://www.googleapis.com/auth/gmail.modify"]
    credentials = service_account.Credentials.from_service_account_file(
        secrets, scopes=scopes
    )
    credentials_delegated = credentials.with_subject(user_email)
    gmail_service = build("gmail", "v1", credentials=credentials_delegated)
    return gmail_service


# ## List labels

# In[8]:


def list_labels(service):
    """Get a list all labels in the user's mailbox.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.

    Returns:
    A list all Labels in the user's mailbox in JSON format.
    """
    try:
        response = service.users().labels().list(userId="me").execute()
        labels = response["labels"]
        return labels
    except Exception as e:
        s, r = getattr(e, "message", str(e)), getattr(e, "message", repr(e))
        print("s:", s, "len(s):", len(s))
        print("r:", r, "len(r):", len(r))


# In[10]:


def get_label(service, label_name):
    labels = list_labels(service)
    for label in labels:
        if label["name"].lower() == label_name.lower():
            return label["id"]


# In[12]:


def list_messages_matching_query(service, query=""):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: Typically 'me', the authorised user
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId="me", q=query).execute()
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])

        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = (
                service.users()
                .messages()
                .list(userId="me", q=query, pageToken=page_token)
                .execute()
            )
            messages.extend(response["messages"])

        return messages
    except Exception as e:
        s, r = getattr(e, "message", str(e)), getattr(e, "message", repr(e))
        print("s:", s, "len(s):", len(s))
        print("r:", r, "len(r):", len(r))


# In[13]:


def list_messages_matching_labels(service, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
    service: Authorized Gmail API service instance.
    user_id: Typically 'me', the authorised user
    label_ids: Only return Messages with these labelIds applied.

    Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
    """

    try:
        response = (
            service.users().messages().list(userId="me", labelIds=label_ids).execute()
        )
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])

        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = (
                service.users()
                .messages()
                .list(userId="me", labelIds=label_ids, pageToken=page_token)
                .execute()
            )
            messages.extend(response["messages"])

        return messages
    except Exception as e:
        s, r = getattr(e, "message", str(e)), getattr(e, "message", repr(e))
        print("s:", s, "len(s):", len(s))
        print("r:", r, "len(r):", len(r))


# In[15]:


def get_message(service, msg_id):
    """Get a Message and use it to create a MIME Message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: Typically 'me', the authorised user
    msg_id: The ID of the Message required.

    Returns:
    A message.
    """
    try:
        message = service.users().messages().get(userId="me", id=msg_id).execute()
        return message
    except Exception as e:
        print(getattr(e, "message", repr(e)))


# In[16]:


def get_message_body(service, msg_id):
    """Get a Message and use it to create a MIME Message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: Typically 'me', the authorised user
    msg_id: The ID of the Message required.

    Returns:
    A message.
    """
    try:
        message = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="raw")
            .execute()
        )
        msg_str = base64.urlsafe_b64decode(message["raw"].encode("ascii")).decode(
            "utf-8"
        )
        mail = mailparser.parse_from_string(msg_str)
        body_text = " ".join(mail.text_plain)
        return body_text
    except Exception as e:
        print(getattr(e, "message", repr(e)))


# In[25]:


def convert_message_to_json(service, message, body, message_folder):
    json_filename = message_folder / f"{message['id']}.json"
    message["body"] = body
    if not json_filename.exists():
        json_filename.write_text(json.dumps(message, indent=4))
        return json_filename
    else:
        return None


# In[27]:


def write_file(
    filetype,
    message,
    attachment_name,
    file_data,
    attachment_list,
    count,
    attachment_folder,
):
    filepath = attachment_folder / filetype
    filepath.mkdir(parents=True, exist_ok=True)
    af = (filepath / attachment_name).write_bytes(file_data)
    attachment_list.append(attachment_name)
    count += 1
    return attachment_list, count


def get_data(msg_id, part, service):
    if "data" in part["body"]:
        data = part["body"]["data"]
    else:
        att_id = part["body"]["attachmentId"]
        att = (
            service.users()
            .messages()
            .attachments()
            .get(userId="me", messageId=msg_id, id=att_id)
            .execute()
        )
        data = att["data"]
    file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
    return file_data


def build_filename(msg_id, part):
    print(f'Original filename: {part["filename"]}')
    part["filename"] = part["filename"].replace("-", " ")
    part["filename"] = part["filename"].replace("_", " ")
    parts = part["filename"].split()
    part["filename"] = "_".join(parts)
    attachment_name = Path(f"{msg_id}_{part['filename']}")
    attachment_name = attachment_name.with_suffix(attachment_name.suffix.lower())
    return attachment_name


def save_attachments(service, message, attachment_folder):
    msg_id = message["id"]
    pdf_attachment_list = []
    excel_attachment_list = []
    pdf_count = 0
    excel_count = 0
    for part in message["payload"]["parts"]:
        if part["filename"] and part["filename"] != "noname":
            file_data = get_data(msg_id, part, service)
            attachment_name = build_filename(msg_id, part)
            if "pdf" in attachment_name.suffix:
                pdf_attachment_list, pdf_count = write_file(
                    "pdf",
                    message,
                    attachment_name,
                    file_data,
                    pdf_attachment_list,
                    pdf_count,
                    attachment_folder,
                )
                print(f" --Saved PDF: {attachment_name}")
            elif "xls" in attachment_name.suffix or "csv" in attachment_name.suffix:
                excel_attachment_list, excel_count = write_file(
                    "xls",
                    message,
                    attachment_name,
                    file_data,
                    excel_attachment_list,
                    excel_count,
                    attachment_folder,
                )
                print(f" --Saved XLS: {attachment_name}")
            else:
                print(f' --Skipped {part["filename"]}')
    return pdf_attachment_list, pdf_count, excel_attachment_list, excel_count


# In[31]:


def update_labels(service, msg_id, to_do_label, done_label):
    msg_labels = {"removeLabelIds": [to_do_label], "addLabelIds": [done_label]}
    try:
        message = (
            service.users()
            .messages()
            .modify(userId="me", id=msg_id, body=msg_labels)
            .execute()
        )
        return message
    except Exception as e:
        print(getattr(e, "message", repr(e)))


# In[ ]:


# In[ ]:
