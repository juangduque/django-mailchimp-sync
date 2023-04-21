def map_csv_row_to_merge_fields(csv_file_headers):
    return {
    "EMAIL": csv_file_headers["Email Addresses\\Email address"],
    "FNAME": csv_file_headers["First name"],
    "LNAME": csv_file_headers["Last/Organization/Group/Household name"],
    "MMERGE15": csv_file_headers["Addresses\\Address line 1"] + " " + csv_file_headers["Addresses\\Address line 2"] + " " + csv_file_headers["Addresses\\City"] + " " + csv_file_headers["Addresses\\State abbreviation"] + " " + csv_file_headers["Addresses\\ZIP"] + " " + csv_file_headers["Addresses\\Country abbreviation"],
    "PHONE": csv_file_headers["Phones\\Number"],
    "MMERGE7": csv_file_headers["Addresses\\Country abbreviation"],
    "MMERGE8": "Addresses\\State abbreviation",
    "MMERGE9": csv_file_headers["Addresses\\ZIP"],
    "MMERGE10": csv_file_headers["System record ID"],
    "MMERGE11": csv_file_headers["Date changed"],
    "MMERGE12": csv_file_headers["Email Addresses\\Date changed"],
    "MMERGE13": csv_file_headers["Todays Visitors Attribute\\Value"],
    "MMERGE14": csv_file_headers["Todays Visitors Attribute\\Date changed"],
    "MMERGE16": csv_file_headers["Phones\\Date changed"],
    }

def get_merge_fields_names():
    return [
        "Email Address",
        "First Name",
        "Last Name",
        "Full address",
        "Phone Number",
        "Country",
        "State abreviation",
        "ZIP code",
        "System record ID",
        "Date changed",
        "Email change timestamp",
        "Today visitors attribute",
        "Today visitors Attribute change timestamp",
        "Phone change timestamp"
    ]

def map_to_member_fields(member):
    return [
        member["email_address"],
        member["merge_fields"]["FNAME"],
        member["merge_fields"]["LNAME"],
        member["merge_fields"]["MMERGE15"],
        member["merge_fields"]["PHONE"],
        member["merge_fields"]["MMERGE7"],
        member["merge_fields"]["MMERGE8"],
        member["merge_fields"]["MMERGE9"],
        member["merge_fields"]["MMERGE10"],
        member["merge_fields"]["MMERGE11"],
        member["merge_fields"]["MMERGE12"],
        member["merge_fields"]["MMERGE13"],
        member["merge_fields"]["MMERGE14"],
        member["merge_fields"]["MMERGE16"]
    ]