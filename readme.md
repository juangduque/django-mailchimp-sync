In admin site:
user: admin
pw: 123456

my_csv_uploader_app_api_key: 9c514b6cead3fca2b6e7078a39899139-us21

response = client.ping.get()
{'health_status': "Everything's Chimpy!"}


response2 = client.lists.get_all_lists()
for list in response2['lists']:
    print(list['name'], list['id'])

def create_new_list():
    try:
        new_list = client.lists.create_list(
            {
                "name": "contact list name",
                "permission_reminder": "permission_reminder",
                "email_type_option": True,
                "contact": {
                    "company": "company",
                    "address1": "address1",
                    "city": "city",
                    "country": "country"
                },
                "campaign_defaults": {
                    "from_name": "from_name",
                    "from_email": "Maud_Lehner27@gmail.com",
                    "subject": "subject",
                    "language": "language"
                }
            }
        )

        print(new_list)
    except ApiClientError as error:
        print("Error: {}".format(error.text))

        # # Add a contact to the new list
        # list_id = new_list["id"]
        # contact_data = {
        #     "email_address": "example@example.com",
        #     "status": "subscribed",
        #     "merge_fields": {
        #         "FNAME": "John",
        #         "LNAME": "Doe"
        #     }
        # }

        # response = client.lists.add_list_member(list_id, contact_data)
        # print(response)

{
    'First name'
    'Last/Organization/Group/Household name'
    'System record ID'
    'Date changed'
    'Email Addresses\\Email address'
    'Email Addresses\\Date changed'
    'Todays Visitors Attribute\\Value'
    'Todays Visitors Attribute\\Date changed'
    'Addresses\\Address line 1'
    'Addresses\\Address line 2'
    'Addresses\\City'
    'Addresses\\ZIP'
    'Addresses\\State abbreviation'
    'Addresses\\Country abbreviation'
    'Phones\\Number'
    'Phones\\Date changed'
}

[{'email_address': 'jturner@socialgoodsoftware.com', 'merge_fields': {'FNAME': '', 'LNAME': '', 'ADDRESS': '', 'PHONE': '', 'BIRTHDAY': '', 'MMERGE6': '', 'MMERGE7': '', 'MMERGE8': '', 'MMERGE9': '', 'MMERGE10': '', 'MMERGE11': '', 'MMERGE12': '', 'MMERGE13': '', 'MMERGE14': '', 'MMERGE15': '', 'MMERGE16': ''}}]

[('Address', 'ADDRESS'), ('Birthday', 'BIRTHDAY'), ('First Name', 'FNAME'), ('Last Name', 'LNAME'), ('System record ID', 'MMERGE10'), ('Date changed', 'MMERGE11'), ('Email change timestamp', 'MMERGE12'), ('Today visitors attribute', 'MMERGE13'), ('Today visitors Attribute change timestamp', 'MMERGE14'), ('Full address', 'MMERGE15')]


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

An error occurred: {"title":"Member Exists","status":400,"detail":"jturne@socialgoodsoftware.com is already a list member. Use PUT to insert or update list members.","instance":"85abe27a-625c-5aec-5077-1dd492c41f98"}

An error occurred: {"title":"Member Exists","status":400,"detail":"rick@socialgoodsoftware.com is already a list member. Use PUT to insert or update list members.","instance":"7f15febe-615f-be8b-9d2b-3e83a243c5f0"}

An error occurred: {"type":"https://mailchimp.com/developer/marketing/docs/errors/","title":"Invalid Resource","status":400,"detail":"jturne@socialgoodsoftware.com has signed up to a lot of lists very recently; we're not allowing more signups for now","instance":"cd25c7ac-d736-0ab1-78eb-e819d764e827"}

An error occurred when checking the existence of contact: {"type":"https://mailchimp.com/developer/marketing/docs/errors/","title":"Resource Not Found","status":404,"detail":"The requested resource could not be found.","instance":"523ddb0e-b9c6-6ebc-a6a2-b69ef91861ce"}

An error occurred when checking the existence of contact: {"type":"https://mailchimp.com/developer/marketing/docs/errors/","title":"Resource Not Found","status":404,"detail":"The requested resource could not be found.","instance":"1aea85af-2f2c-a494-fc83-be9683d157c9"}

It's also worth noting that repeatedly attempting to add the same email address in a short period of time may trigger Mailchimp's abuse prevention measures and result in your account being suspended or terminated.