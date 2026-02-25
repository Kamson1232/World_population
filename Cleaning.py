import pandas as pd


Countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso",
    "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba",
    "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Greece", "Greenland", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
    "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
    "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
    "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
    "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
    "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela",
    "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Loading data, droping not wanted collumns and changing 'Value' data type

df = pd.read_csv(
    r'C:\Users\Kamil\Desktop\World_population_project\raw_data\UNdata_Delimited.csv', sep=None, engine='python')
df = df.drop(columns=['Value Footnotes', 'Unnamed: 11'])
df['Value'] = df['Value'].astype(int)

# Checking population value for each country

df_check = df.groupby('Country or Area')['Value'].sum(
).reset_index().sort_values('Value', ascending=False)

# Removing duplicates and false data caused by 'City type' and 'Record Type' columns

df = df.groupby(['Country or Area', 'Year', 'Sex', 'City'])[
    'Value'].max().reset_index()

# Removing duplicated cities for Australia

df = df.drop(df[(df['Country or Area'] == 'Australia') & (
    df['City'].str.contains('Greater', case=False, na=False))].index)

# Now I want to check for teoritories and countries names that contains language-specific letters and brackets

df_names = df.loc[~df['Country or Area'].isin(Countries)]

df_names = df_names['Country or Area'].unique()

# df_names gives me a list of not wanted rows and rows that 'Country or Area' value needs to be changed

names_to_change = {
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Brunei Darussalam': 'Brunei',
    "Côte d'Ivoire": 'Ivory Coast',
    "Democratic People's Republic of Korea": 'North Korea',
    'Holy See': 'Vatican City',
    'Iran (Islamic Republic of)': 'Iran',
    "Lao People's Democratic Republic": 'Laos',
    'Micronesia (Federated States of)': 'Micronesia',
    'Netherlands (Kingdom of the)': 'Netherlands',
    'Republic of Korea': 'South Korea',
    'Republic of Moldova': 'Moldova',
    'Republic of South Sudan': 'South Sudan',
    'Russian Federation': 'Russia',
    'State of Palestine': 'Palestine',
    'Türkiye': 'Turkey',
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'United Republic of Tanzania': 'Tanzania',
    'United States of America': 'United States',
    'Venezuela (Bolivarian Republic of)': 'Venezuela'
}


names_to_drop = ["American Samoa", "Anguilla", "Aruba", "Bermuda", "British Virgin Islands", "Cayman Islands", "Cook Islands", "Falkland Islands (Malvinas)", "Faroe Islands", "French Guiana",
                 "French Polynesia", "Gibraltar", "Greenland", "Guadeloupe", "Guam", "Guernsey", "Isle of Man", "Jersey", "Martinique", "Mayotte", "Montserrat", "Netherlands (Kingdom of the)",
                 "New Caledonia", "Niue", "Northern Mariana Islands", "Pitcairn", "Puerto Rico", "Reunion", "Saint Helena ex. dep.", "Saint Pierre and Miquelon", "Turks and Caicos Islands",
                 "United States Virgin Islands", "Wallis and Futuna Islands", "Åland Islands"]

# Dropping and renaming

df = df.drop(df[df['Country or Area'].isin(names_to_drop)].index)

df['Country or Area'] = df['Country or Area'].replace(names_to_change)

# It seems like some of the rows are structured incorrectly

df_test = df['Sex'].unique()

# We get fourth value "Total" which doesn't make sense

df_test = df.loc[df['Sex'] == 'Total']

# So we drop those rows

df = df.drop(df[df['Sex'] == 'Total'].index)


df.to_csv(r"C:\Users\Kamil\Desktop\World_population_project\clean_data\df_data.csv", index=False)
