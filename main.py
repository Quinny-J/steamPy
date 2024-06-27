# I'm still learning python. 
# Don't judge me harshly :)
# Made by @Quinny-J
# 27/06/2024

# if you have it installed but get an error run the last line in term
# pip install requests
# python -m pip install requests

# References 
# Steam API - https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29
# Requests LIB - https://requests.readthedocs.io/en/latest/

# Import Libs
import requests 

# get_steam_id(api_key, vanity_url) Returns SteamID
def get_steam_id(api_key, vanity_url):
    base_url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        "key": api_key,
        "vanityurl": vanity_url
    }

    # Make a request with the params provided to the func
    response = requests.get(base_url, params=params)

    # Check for 200.ok which means success if not something is wrong
    if response.status_code == 200:
        data = response.json()
        success = data.get("response", {}).get("success", 0)
        if success == 1:
            steam_id = data.get("response", {}).get("steamid", None)
            return steam_id
        else:
            print("Failed to resolve vanity URL.")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# get_player_summaries(api_key, steam_id) Returns Games/Player Summary
def get_player_summaries(api_key, steam_id):
    base_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": api_key,
        "steamids": steam_id
    }

    # Make a request with the params provided to the func
    response = requests.get(base_url, params=params)
    
    # Check for 200.ok which means success if not something is wrong
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def main():
    api_key = "YOURAPIKEYHERE"  # Replace this with your own Steam API key

    print("Choose an option:")
    print("1. Enter Steam ID")
    print("2. Enter Vanity URL")

    # Take the user input in which func they want to run
    option = input("Option (1/2): ")

    # Check if 1 or 2 was entered if not send a error message
    if option == "1":
        steam_id = input("Enter the Steam ID: ")
    elif option == "2":
        vanity_url = input("Enter the Vanity URL: ").strip() # Strip whitespace from start and end
        if not vanity_url: # Check if we have a vanity url
            print("Vanity URL cannot be empty.")
            return
        steam_id = get_steam_id(api_key, vanity_url)
    else:
        print("Invalid option. Please choose 1 or 2.")
        return

    # check if we have got a steamid
    if steam_id:
        print(f"Resolved Steam ID: {steam_id}")

        # Display the results in a specific format 
        output_type = input("(RAW/PRETTY/SIMPLE) Pick an output type: ").strip().lower()

        # check if we have a valid output type
        while output_type not in ["raw", "pretty", "simple"]:
            print("Invalid output type. Please enter 'raw', 'pretty', or 'simple'.")
            output_type = input("(RAW/PRETTY/SIMPLE) Pick an output type: ").strip().lower()

        # Execute func and assign the data that the func has gathered to data :)
        data = get_player_summaries(api_key, steam_id)

        # Again checking if we have the data in data
        if data:
            # Prints the output type selected
            print(f"Player Summaries (Output Type: {output_type}):")
            if output_type == "pretty": # Nicely formatted json
                import json
                print(json.dumps(data, indent=2))
            elif output_type == "simple": # Printed line by line in the console
                # For player_info i had to get the players object which stores all the info
                # This was a bit of a challenge but i overcome it. NEVER LET SOMETHING STOP YOU !
                # Assign the variables with the seperate data to make life easier  
                player_info = data.get("response", {}).get("players", [{}])[0] 
                avatar = player_info.get("avatar", "")
                profileurl = player_info.get("profileurl", "")
                personaname = player_info.get("personaname", "")
                country = player_info.get("loccountrycode", "")
                
                # Putting f infront of the quotes allows me to pull the variable inside of the string
                print(f"Avatar: {avatar}")
                print(f"Profile URL: {profileurl}")
                print(f"Personaname: {personaname}")
                print(f"Base Location: {country}")
            else:
                print(data)
        else:
            print("Data retrieval failed.") # Something went wrong during the request
    else:
        print("Steam ID retrieval failed.") # Something went wrong during the request


# Mainly for debug purpose
# Helps when imported or to be ran directly
if __name__ == "__main__":
    main()