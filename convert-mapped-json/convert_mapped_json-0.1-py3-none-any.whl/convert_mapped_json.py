#!/usr/bin/env python
# coding: utf-8

# # Convert Invoice
#
# This notebook takes invoice data and converts it to the Purchase Plus format.

# In[1]:


import json
from datetime import date, datetime
from yaml import load, Loader
from pathlib import Path


# In[4]:


invoice_template_header = {
    "identity": "richard.match.editor.invoices@marketboomer.com",
    "invoices": [
        {
            "invoiceHeader": {
                "invoiceID": "INV12312",
                "invoiceDate": "2019-03-27",
                "currency": "AUD",
                "taxLocation": "AU",
                "invoiceURI": "https://example.com/invoice.pdf",
                "billingAddress": {
                    "line1": "1 Somewhere Rd",
                    "city": "Sydney",
                    "stateProvince": "NSW",
                    "postalCode": "2000",
                    "country": "AU",
                },
            },
            "invoiceOrder": [
                {
                    "purchaseOrderID": "PO55555",
                    "supplyOrderID": "PO55555",
                    "invoiceLine": [],
                }
            ],
            "invoiceSummary": {
                "subTotalAmount": 50,
                "shippingAmount": 0,
                "netAmount": 50,
                "tax": [
                    {"taxCategory": "GST", "taxPercentage": 10, "taxAmount": 5},
                    {"taxCategory": "Shipping", "taxPercentage": 10, "taxAmount": 0},
                ],
                "grossAmount": 55,
            },
            "comments": [{"body": "This is a comment on the invoice"}],
        }
    ],
}


# In[5]:


invoice_template_line = {
    "supplierProductCode": "1232",
    "purchaserProductCode": "",
    "description": "Coca Cola 600 ml bottle carton of 24",
    "quantity": 5,
    "unitPrice": 10,
    "netAmount": 50,
    "tax": [{"taxCategory": "GST", "taxPercentage": "", "taxAmount": 5}],
    "grossAmount": 55,
}


# In[7]:


header_key_mapping = {
    "PartnerInternalNo": "identity",
    "InvoiceNumber": "invoiceID",
    "InvoiceDate": "invoiceDate",
    "PurchaseOrderNumber": "purchaseOrderID",
    "InvAmountExcGST": "netAmount",
    "InvGST": "taxAmount",
    "InvAmountIncGST": "grossAmount",
}

line_key_mapping = {
    "InHouseProductID": "supplierProductCode",
    "InHouseProductDescription": "description",
    "InvoicedQuantity": "quantity",
    "LineGST": "taxAmount",
    "LineAmountIncGST": "grossAmount",
}


# In[8]:


def transform_dict(start_dict, mapping):
    end_dict = {}
    for k, v in mapping.items():
        end_dict[v] = start_dict[k]
        if isinstance(end_dict[v], date) or isinstance(end_dict[v], datetime):
            end_dict[v] = date.isoformat(end_dict[v])
    return end_dict


# In[9]:


def substitute(template, input_dictionary, mapping=""):
    if mapping:
        replacement = transform_dict(input_dictionary, mapping)
    else:
        replacement = input_dictionary
    for k, v in template.items():
        if k in replacement.keys():
            print(f"Replacing {template[k]} with {replacement[k]}")
            template[k] = replacement[k]
        elif isinstance(v, dict):
            substitute(v, replacement)
        elif isinstance(v, list):
            for d in v:
                substitute(d, replacement)
        else:
            print(f"{k} untouched")
    return template
