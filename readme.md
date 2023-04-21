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
