#!/usr/bin/env python
# coding: utf-8

# # Remittance processor
#
# This application reads a list of remittances from Docparser and creates a dataframe saved as an Excel file.

# In[3]:


import json
import numpy as np
import pandas as pd
import re
import requests
import zipfile

from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import List
from pathlib import Path

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from money2float import money
import semi_structured_text_extractor as sste
import split_alphanumeric as sa

pd.options.display.float_format = "{:,.2f}".format


# In[4]:


def get_content(download_url, auth_key):
    res = requests.get(download_url, auth=(auth_key, ""), timeout=5)
    try:
        content = res.json()
    except:
        content = {}
    return content


# In[6]:


def download_pdf(filename, url):
    response = requests.get(url)
    filename.write_bytes(response.content)


# In[7]:


def make_text_file_ready(text, strings_to_delete):
    try:
        text = re.sub("[^A-Za-z0-9_ ]+", "", text).lower()
        text_list = text.split()
        good_text = []
        already_got_it = []
        for item in text_list:
            if item not in strings_to_delete and item not in already_got_it:
                good_text.append(item)
                already_got_it.append(item)
        text = "_".join(good_text)
    except:
        text = "missing_value"
    return text


# In[9]:


def make_filename(header, remittance, strings_to_delete):
    extension = Path(remittance["file_name"]).suffix
    insured_shortname = make_text_file_ready(
        header["insurer_short_name"], strings_to_delete
    )
    broker = make_text_file_ready(header.get("broker", ""), strings_to_delete)
    remittance_date = make_text_file_ready(
        remittance.get("remittance_date", "missing"), strings_to_delete
    )
    filename = Path(remittance["file_name"]).stem
    filename = make_text_file_ready(filename, strings_to_delete)
    try:
        filename = filename.rsplit("_")[1]
    except:
        pass

    new_filename = "_".join(
        [insured_shortname, broker, remittance_date, filename, extension]
    )
    return new_filename.replace("_.", ".")


# In[4]:


def determine_sign(target):
    if target:
        if "CR" in str(target) or "-" in str(target) or "(" in str(target):
            try:
                target = target.strip("-")
                target = target.strip("CR")
                target = target.strip("()")
            except:
                pass
            target = money(target) * -1
        return money(target)


# In[12]:


def make_header(remittance, strings_to_delete):
    header = {}
    try:
        header["insurer"] = " ".join(remittance.get("insurer").split())
    except:
        header["insurer"] = ""
    header["insurer_short_name"] = make_text_file_ready(
        header["insurer"], strings_to_delete
    )
    header["broker"] = remittance.get("broker", "")
    header["broker_abn"] = remittance.get("broker_abn", "")
    header["remittance_date"] = remittance.get("remittance_date", "")
    try:
        header["remittance_total"] = determine_sign(remittance["remittance_total"])
    except:
        header["remittance_total"] = None
    header["doc_format"] = remittance.get("tagger", "")
    header["original_filename"] = remittance.get("file_name", "")
    header["full_text"] = remittance.get("full_text", "")
    return header


# In[53]:


def build_row(text, header):
    lines = sste.split_text(text, "^^^")
    dates = sste.find_objects(lines, "dates")
    numbers = sste.find_objects(lines, "numbers")
    numbers = np.ravel(numbers)
    doc_format = header["doc_format"]

    try:
        if doc_format == "wuf":
            response = {"insured_name": " ".join(lines[0][:])}

        if doc_format == "ins_set_statement":
            response = {
                "policy_number": lines[0][-1],
                "type": "",
                "effective_date": dates[1][0],
                "invoice_number": lines[1][3],
                "insured_name": " ".join(lines[0][2:-2]),
            }

        if doc_format == "aub_group":
            insured_name = f"{' '.join(lines[0][2:-1])}"
            if not insured_name:
                insured_name = f"{' '.join(lines[0][2:])}"
            response = {
                "policy_number": lines[2][0],
                "type": lines[4][-1],
                "effective_date": dates[0][0],
                "invoice_number": lines[4][0],
                "insured_name": insured_name,
            }

        if doc_format == "macquarie":
            response = {
                "policy_number": lines[0][0],
                "type": lines[0][1],
                "effective_date": dates[0][0],
                "invoice_number": lines[0][-1],
                "insured_name": " ".join(lines[1][:-1]),
            }

        if doc_format == "insurance_house":
            response = {
                "policy_number": lines[3][0],
                "type": "",
                "effective_date": dates[0][0],
                "invoice_number": "",
                "insured_name": " ".join(lines[0][:]),
            }

        if doc_format == "portrait":
            response = {
                "policy_number": " ".join(lines[3][:]),
                "type": lines[6][-1],
                "effective_date": dates[0][0],
                "invoice_number": lines[1][-1],
                "insured_name": " ".join(lines[0][:]),
                "premium_inc_commission_inc_gst": lines[2][-1],
                "broker_commission": lines[5][-1],
                "gst_broker_commission": lines[8][-1],
            }

        if doc_format == "brokerplus":
            insured_name = ""
            for line in lines[:-1]:
                insured_name = f"{insured_name} " + f"{' '.join(line)}"
            response = {"insured_name": insured_name}

        if doc_format == "advisernet":
            if f"{lines[3][0]}" not in numbers:
                print(f"{lines[3][0]}")
                print(numbers)
                policy_number = lines[3][0]
            else:
                policy_number = ""
            response = {
                "policy_number": policy_number,
                "type": " ".join(lines[2][1:]),
                "effective_date": dates[0][0],
                "invoice_number": lines[3][-1],
                "insured_name": " ".join(lines[0][1:]),
            }

        for i, line in enumerate(lines):
            print(i, line)
        print(dates)
        print(numbers)

    except:
        print("Failed to build row")
        print()
        print(text)
        print()
        response = {}
    return response


# In[22]:


def convert_fee_group(rows, fee_mapping):
    return_rows = []
    for row in rows:
        fee_group_list = sa.build_fee_group_list(row["fee_group"])
        mapped_group = sa.map_fee_group_to_fields(fee_group_list, fee_mapping)
        for name, value in mapped_group.items():
            row[name] = value
        return_rows.append(row)
    return return_rows


# In[23]:


def save_template_file(tag, remittance):
    (Path.cwd() / "test_data" / f"{tag}.json").write_text(
        json.dumps(remittance, indent=4)
    )


# In[24]:


def process_remittance(header, rows, return_columns):
    transformed_rows = []
    for row in rows:
        policy_data = row.get("policy_data", False)
        if policy_data:
            row_builder = build_row(policy_data, header["doc_format"])
            if row_builder:
                for k, v in row_builder.items():
                    row[k] = v
        final = {**header, **row}
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    columns = [x for x in return_columns if x in df.columns]
    df = df[columns]
    return df


# In[25]:


def calculate_columns(df, columns, money_columns):
    all_money_columns = [x for x in money_columns["all"] if x in df.columns]
    add_columns = [x for x in money_columns["add"] if x in df.columns]
    subtract_columns = [x for x in money_columns["subtract"] if x in df.columns]
    for column in all_money_columns:
        df[column] = df[column].apply(lambda x: determine_sign(x))
    df["calculated_remittance_detail"] = (
        df[add_columns].sum().sum() - df[subtract_columns].sum().sum()
    )
    df["calculated_remittance_total"] = df["line_net"].sum()
    df["total_difference"] = df["remittance_total"] - df["calculated_remittance_total"]
    df["total_difference"] = df["total_difference"].round(decimals=2).abs()
    return_columns = [x for x in columns if x in df.columns]
    return df[return_columns]


# In[27]:


def convert_section_totals(df, remittance):
    try:
        section_totals_df = pd.DataFrame(remittance["section_totals"], index=[0])
        df["remittance_total"] = (
            section_totals_df["total"].apply(lambda x: determine_sign(x)).sum()
        )
        remittance_total = df["remittance_total"].iloc[0]
    except:
        section_totals_df = pd.DataFrame.from_dict(remittance["section_totals"])
        try:
            df["remittance_total"] = (
                section_totals_df["total"].apply(lambda x: determine_sign(x)).sum()
            )
            remittance_total = df["remittance_total"].iloc[0]
        except:
            remittance_total = 0
    return remittance_total


# In[28]:


def make_hyperlink(folder, rel_location):
    url = f'=HYPERLINK("{rel_location}remittances\\{folder.parent.name}\\{folder.name}", "PDF")'
    return url


# In[29]:


def create_mapping(target, cp):
    rows = pd.read_excel(cp / "company_mapping.xlsx", sheet_name=target)
    rows.to_dict(orient="records")
    mapping = {}
    for row in rows.values:
        mapping[row[0]] = row[1]
    return mapping


# In[31]:


def replace_blanks(field, mapping, remittance):
    if field == None:
        for item in mapping.keys():
            if item.lower() in remittance["full_text"].lower():
                print(item)
                return item
    else:
        return field


# In[33]:


def normalise_header(
    header, remittance, strings_to_delete, insurer_short_name_mapping, broker_mapping
):
    header["insurer_short_name"] = insurer_short_name_mapping.get(
        header["insurer_short_name"], header["insurer_short_name"]
    )
    header["broker"] = broker_mapping.get(header["broker"], header["broker"])
    header["broker"] = replace_blanks(header["broker"], broker_mapping, remittance)
    header["new_filename"] = make_filename(header, remittance, strings_to_delete)
    return header


# In[35]:


def save_remittance_file(source_filename, remittance):
    if not source_filename.exists() and source_filename.suffix == ".pdf":
        download_pdf(source_filename, remittance["media_link"])
        print(f"Downloading {source_filename}")
    #         return
    else:
        pass


# ## Create zip files

# In[41]:


def create_files_grouped_by_column(df, column):
    gb = df.groupby(column)
    [gb.get_group(x) for x in gb.groups]
    return gb


# In[ ]:


def save_daily_files(all_dfs, column, email_folder, email_arrival_date):
    insurers_folder = email_folder / "insurers"
    insurers_folder.mkdir(parents=True, exist_ok=True)
    groups = create_files_grouped_by_column(all_dfs, column)
    for group in groups:
        display(group[0])
        insurer_name_date = f"{group[0]}_{email_arrival_date}"
        excel_filename = (insurers_folder / insurer_name_date).with_suffix(".xlsx")
        group[1].to_excel(excel_filename, index=False)
        display(group[1])


# In[ ]:


def get_all_daily_insurer_files(email_folder):
    insurers_folder = email_folder / "insurers"
    files = list(insurers_folder.glob("*.xlsx"))
    df_lists = []
    for file in files:
        df = pd.read_excel(file)
        df = df[
            ["insurer_short_name", "remittance_date", "new_filename"]
        ].drop_duplicates()
        df["excel_file"] = (
            "./remittance_data/" + email_folder.name + "/insurers/" + file.name
        )
        df["pdf_file"] = (
            "./remittances/" + df["remittance_date"] + "/" + df["new_filename"]
        )
        df_lists.append(df.to_dict(orient="records"))
    return df_lists


# In[ ]:


def make_zip_file(df_lists, email_arrival_date):
    for i, df_list in enumerate(df_lists):
        zipfile_folder = Path.cwd() / "zips_to_email" / email_arrival_date
        print(zipfile_folder)
        zipfile_folder.mkdir(parents=True, exist_ok=True)
        zipfile_name = f"{df_list[0]['insurer_short_name']}_{email_arrival_date}.zip"
        with zipfile.ZipFile(zipfile_folder / zipfile_name, "w") as new_zip:
            excel_file = df_list[0]["excel_file"]
            new_zip.write(
                excel_file, arcname=f"{df_list[0]['insurer_short_name']}.xlsx"
            )
            for row in df_list:
                new_zip.write(row["pdf_file"], arcname=row["pdf_file"])
    return f"Successfully created {len(df_lists)} zip file(s)"


# In[ ]:


def make_common_zip_file(df_lists, email_arrival_date):
    for i, df_list in enumerate(df_lists):
        zipfile_folder = Path.cwd() / "zips_to_email" / email_arrival_date
        email_arrival_month = email_arrival_date.split("-")[:-1]
        insurer_short_name = df_list[0]["insurer_short_name"]
        arcname_excel = f"./remittance_data/{insurer_short_name}/{email_arrival_month}/{insurer_short_name}_{email_arrival_date}.xlsx"
        print(zipfile_folder)
        zipfile_folder.mkdir(parents=True, exist_ok=True)
        zipfile_name = f"{df_list[0]['insurer_short_name']}_{email_arrival_date}.zip"
        with zipfile.ZipFile(zipfile_folder / zipfile_name, "w") as new_zip:
            excel_file = df_list[0]["excel_file"]
            new_zip.write(
                excel_file, arcname=f"{df_list[0]['insurer_short_name']}.xlsx"
            )
            for row in df_list:
                new_zip.write(row["pdf_file"], arcname=row["pdf_file"])
    return f"Successfully created {len(df_lists)} zip file(s)"


# In[ ]:
