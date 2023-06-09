from django.shortcuts import render, redirect
from django.http import HttpResponse
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from io import TextIOWrapper
from .forms import UploadNewFileForm
from .utils import get_merge_fields_names, map_csv_row_to_merge_fields, map_to_member_fields
import io, csv, requests, json


API_KEY = "9c514b6cead3fca2b6e7078a39899139-us21"
SERVER_PREFIX = "us21"
LIST_ID = "c71779671d"
DEBUG = True

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": API_KEY,
    "server": SERVER_PREFIX
})

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        extension = csv_file.name.split('.')[-1] # Get the file extension
        if extension.lower() != "csv":
            return redirect('file_format_error') # Return an error if the file is not a CSV
        csv_file_wrapper = TextIOWrapper(csv_file, encoding='utf-8')            
        csv_reader = csv.DictReader(csv_file_wrapper) # Use Python's built-in CSV library to read the file
        headers = csv_reader.fieldnames
        email_header = ""
        # Set a default email header
        if "Email Addresses\\Email address" in headers:
            email_header = "Email Addresses\\Email address"
        else:
            email_header = "email" # Generic email header
        user_sync_counter = 0
        for row in csv_reader:
            email = row.get(email_header)
            merge_fields = map_csv_row_to_merge_fields(row)
            # Log the merge fields of the contact to be added
            if DEBUG: 
                print("merge_fields: ", user_sync_counter)
                print(json.dumps(merge_fields, indent=4, sort_keys=True))
            # Check if the member is already subscribed
            try:
                response = client.lists.get_list_member(LIST_ID, email)
            except ApiClientError as e:
                print("An error occurred when checking the existence of contact: {}".format(e.text))
                return redirect('error')            
            if response.get("status") == "subscribed":
                continue
            else:
                # Add the member to the list 
                try:
                    client.lists.add_list_member(
                        LIST_ID,
                        {
                            "email_address": email,
                            "status": "subscribed",
                            "merge_fields": merge_fields
                        }
                    )
                    user_sync_counter += 1
                    request.session['user_sync_counter'] = user_sync_counter
                except ApiClientError as e:
                    # Handle any errors that occur
                    print("An error occurred when adding a contact to the list: {}".format(e.text))
                    return redirect('error')
        return redirect('success')
    else:
        form = UploadNewFileForm()
    return render(request, 'list/upload.html', {'form': form})

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
                row = map_to_member_fields(member) # replace with your merge field data
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
    return render(request, 'list/download.html', {})

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

def index(request):
    return render(request, 'index.html')

def success(request):
    return render(request, 'success.html')

def error(request):
    return render(request, 'error/error.html')

def file_format_error(request):
    return render(request, 'error/file_error.html')