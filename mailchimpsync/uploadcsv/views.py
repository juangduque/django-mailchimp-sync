from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadNewFileForm
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from io import TextIOWrapper
import io
import csv
import requests
import json

API_KEY = "9c514b6cead3fca2b6e7078a39899139-us21"
SERVER_PREFIX = "us21"
LIST_ID = "c71779671d"

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": API_KEY,
    "server": SERVER_PREFIX
})

mailchimp_name_tag_map = {
    "Email Address": "EMAIL",
    "First Name": "FNAME",
    "Last Name": "LNAME",
    "Full address": "MMERGE15",
    "Address - Combined": "ADDRESS",
    "Phone Number": "PHONE",
    "phone creation timestamp": "MMERGE6",
    "Country": "MMERGE7",
    "State abreviation": "MMERGE8",
    "ZIP code": "MMERGE9",
    "System record ID": "MMERGE10",
    "Date changed": "MMERGE11",
    "Email change timestamp": "MMERGE12",
    "Today visitors attribute": "MMERGE13",
    "Today visitors Attribute change timestamp": "MMERGE14",
    "Phone change timestamp": "MMERGE16",
}

csv_file_headers = [
    'First name', #0
    'Last/Organization/Group/Household name', #1
    'System record ID', #2
    'Date changed', #3
    'Email Addresses\\Email address', #4
    'Email Addresses\\Date changed', #5
    'Todays Visitors Attribute\\Value', #6
    'Todays Visitors Attribute\\Date changed', #7
    'Addresses\\Address line 1', #8
    'Addresses\\Address line 2', #9
    'Addresses\\City', #10
    'Addresses\\ZIP', #11
    'Addresses\\State abbreviation', #12
    'Addresses\\Country abbreviation', #13
    'Phones\\Number', #14
    'Phones\\Date changed' #15
]

fields_to_data = {
    "Email Address": csv_file_headers[4],
    "First Name": csv_file_headers[0],
    "Last Name": csv_file_headers[1],
    "Full address": csv_file_headers[8] + " " + csv_file_headers[9] + " " + csv_file_headers[10] + " " + csv_file_headers[12] + " " + csv_file_headers[11] + " " + csv_file_headers[13],
    "Phone Number": csv_file_headers[14],
    "Country": csv_file_headers[13],
    "State abreviation": csv_file_headers[12],
    "ZIP code": csv_file_headers[11],
    "System record ID": csv_file_headers[2],
    "Date changed": csv_file_headers[3],
    "Email change timestamp": csv_file_headers[5],
    "Today visitors attribute": csv_file_headers[6],
    "Today visitors Attribute change timestamp": csv_file_headers[7],
    "Phone change timestamp": csv_file_headers[15],
}

def get_merge_fields_names():
    merge_fields = client.lists.get_list_merge_fields(LIST_ID)
    merge_fields_names = []
    for merge_field in merge_fields['merge_fields']:
        merge_fields_names.append(merge_field['name'])
    return merge_fields_names

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        csv_file_wrapper = TextIOWrapper(csv_file, encoding='utf-8')
        # Use Python's built-in CSV library to read the file
        csv_reader = csv.DictReader(csv_file_wrapper)
        headers = csv_reader.fieldnames
        email_header = "Email Address"
        for row in csv_reader:
            email = row.get(email_header)
            # merge_fields = {}
            # # For each row, extract the necessary fields (e.g. email, first name, last name)
            # for header in headers:
            #     merge_fields[header] = row.get(header)
            try:
                response = client.lists.add_list_member(
                    LIST_ID,
                    {
                        "email_address": email,
                        "status": "subscribed",
                        "merge_fields": {
                            "FNAME": row.get("First Name"),
                            "LNAME": row.get("Last Name")
                        }
                    }
                )
            except ApiClientError as e:
                # Handle any errors that occur
                print("An error occurred: {}".format(e.text))
                return redirect('upload_error')
        return redirect('success')
    else:
        print(get_merge_fields_names())
        form = UploadNewFileForm()
    return render(request, 'upload.html', {'form': form})

def download_list(request):
    try:
        url = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{LIST_ID}/members'
        headers = {
            'Authorization': f'apikey {API_KEY}',
            'Content-Type': 'application/json'
        }
        params = {
            'fields': 'members.email_address,members.merge_fields',
            'count': 1000
        }

        response = requests.get(url, headers=headers, params=params)

        # Check if the response was successful
        if response.status_code == 200:
            # Convert the response data to CSV format
            merge_fields = get_merge_fields_names()
            csv_data = io.StringIO()
            writer = csv.writer(csv_data)
            writer.writerow(merge_fields) # replace with your merge field names
            for member in response.json()['members']:
                row = [member['email_address'], member['merge_fields']['FNAME'], member['merge_fields']['LNAME']]  # replace with your merge field data
                writer.writerow(row)

            # Create an HTTP response with the CSV data
            response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported-contacts.csv"'
            return response
        else:
            return HttpResponse('Error:', response.status_code, response.text)
    except ApiClientError as e:
        # Handle any errors that occur
        print("An error occurred: {}".format(e.text))
        return redirect('upload_error')
    
def list_download(request):
    return render(request, 'list_download.html', {})

def connection_check(request):
    is_error = False
    response = None
    try:
        response = client.ping.get()
        response2 = client.lists.get_all_lists()
        for list in response2['lists']:
            print(list['name'], list['id'])
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        is_error = True
    return render(request, 'connection_check.html', {
        'response': response,
        'is_error': is_error,
    })

def success(request):
    return render(request, 'success.html')

def error(request):
    return render(request, 'error.html')