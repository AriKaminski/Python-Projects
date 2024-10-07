import requests
CLIENT_ID = '9d2d31eb-a359-4cc8-aa6b-8f866c586a8e'
CLIENT_SECRET = 'lL0v7tVdSE9ZvV7dLnpR1zjFW3eGvVIZhEb0paau'

def get_oauth_token():
    token_url = "https://www.warcraftlogs.com/oauth/token"
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(token_url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print(f"Failed to get token: {response.status_code}, {response.text}")
        return None
    
def get_character_data(access_token, character_name, server_slug, server_region):
    # Construct the GraphQL query with personal values
    query = f"""
    {{
      characterData {{
         character(name: "{character_name}", serverSlug: "{server_slug}", serverRegion: "{server_region}") {{
        canonicalID
        classID
        guildRank
        id
        level
        name
        encounterRankings(
          encounterID: 2902
          difficulty: 4                  
        )
        }}
      }}
    }}
    """

    url = "https://www.warcraftlogs.com/api/v2/client"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Sending the POST request with the GraphQL query
    print(url, query, headers)
    response = requests.post(url, json={'query': query}, headers=headers)

    if response.status_code == 200:
        character_data = response.json()
        return character_data
    else:
        print(f"Failed to get character data: {response.status_code}, {response.text}")
        return None

# Usage
access_token = get_oauth_token()

if access_token:
    character_name = 'Vannskii'         # Replace with your character name
    server_slug = 'stormrage'            # Replace with your server slug (lowercase)
    server_region = 'us'                 # Replace with your server region

    

    character_data = get_character_data(access_token, character_name, server_slug, server_region)

    ulgrax_parse = character_data['data']['characterData']['character']['encounterRankings']['ranks'][0]['rankPercent']

    print(ulgrax_parse)
    