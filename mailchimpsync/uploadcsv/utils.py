def map_csv_row_to_merge_fields(row):
    return {
    "EMAIL": row["Email Addresses\\Email address"],
    "FNAME": row["First name"],
    "LNAME": row["Last/Organization/Group/Household name"],
    "MMERGE15": row["Addresses\\Address line 1"] + " " + row["Addresses\\Address line 2"] + " " + row["Addresses\\City"] + " " + row["Addresses\\State abbreviation"] + " " + row["Addresses\\ZIP"] + " " + row["Addresses\\Country abbreviation"],
    "PHONE": row["Phones\\Number"],
    "ADDRESS": row["Addresses\\Address line 1"] + " " + row["Addresses\\Address line 2"] + " " + row["Addresses\\City"] + " " + row["Addresses\\State abbreviation"] + " " + row["Addresses\\ZIP"] + " " + row["Addresses\\Country abbreviation"],
    "PHONE": row["Phones\\Number"],
    "MMERGE7": row["Addresses\\Country abbreviation"],
    "MMERGE8": row["Addresses\\State abbreviation"],
    "MMERGE9": row["Addresses\\ZIP"],
    "MMERGE10": row["System record ID"],
    "MMERGE11": row["Date changed"],
    "MMERGE12": row["Email Addresses\\Date changed"],
    "MMERGE13": row["Todays Visitors Attribute\\Value"],
    "MMERGE14": row["Todays Visitors Attribute\\Date changed"],
    "MMERGE16": row["Phones\\Date changed"],
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