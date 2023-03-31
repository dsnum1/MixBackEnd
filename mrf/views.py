import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
import requests
import datetime
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from spotipy.oauth2 import SpotifyOAuth
import random
import json
from django.views.decorators.csrf import csrf_exempt
from ast import literal_eval

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="4aef925cd56f424582097b25919c3584", client_secret="f94bffe44c804c3f83549c719a2223ff"),)

INT_MIN=-2147483648

def login(request):
    # Create a SpotifyOAuth object
    sp_oauth = SpotifyOAuth(client_id=credentials.client_ID, client_secret=credentials.client_SECRET, redirect_uri='http://127.0.0.1:5050/music/callback/', scope = credentials.scope)
    # Print the sp_oauth object to the console
    print("\n\nSP_OAuth Object:" ,sp_oauth, "\n\n")
    # Redirect the user to the Spotify login page
    # Get the authorization URL
    url = sp_oauth.get_authorize_url()
    # Print the authorization url to the console
    print(url)

    # Redirect the user to the Spotify login page
    return HttpResponseRedirect(url)


@csrf_exempt
def index(request):
    print(request.POST)
    starting = request.POST.get("starting", "")
    ending = request.POST.get("posting","")
    playlist_name = request.POST.get("nameOfPlaylist", "")
	
    print(starting, type(starting))
 
   
    duration = AustinGPSDuration(starting, ending)
    print(duration)
    prepared_data = retrieve_spotify_playlist()
    if(type(duration)!=int):
        data = {
            "message":"The address you entered is not valid",
        }
        return HttpResponse( json.dumps( data ) )
 

    best_combination = driver_function(duration=duration, prepared_data=prepared_data)
    ls = []
    for music in best_combination:
        ls.append(music[2])
    link = "https://open.spotify.com/playlist/"+ create_playlist(ls, playlist_name, "This playlist was created by Mix&Ride created by Divyansh Sharma")

    data = {'playlist_link' : link, 'message' : "Sucessfully creeated a spotify playlist"}
    print("This is data", data)
    return HttpResponse( json.dumps( data ) )

def AustinGPSDurationRequestFunction(request):
    origin = request.GET["origin"]
    destinations = request.GET["destination"] 
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&units=SI&mode=driving&key=AIzaSyB2md1asmg34SJTiM9SpW0Kr-ggE7CE5lk"
    #url for request, adds user input of locations
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response=json.loads(response.text)
    print(response.text)
    try:
        duration= response['rows'][0]['elements'][0]['duration']['value']
    except Exception as e:
        duration =  e

    return duration


def AustinGPSDuration(starting, ending):
    origin=starting
    destination = ending
    print("This is the entered path",starting, ending)
    #user input for postal codes
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={starting}&destinations={ending}&units=SI&mode=driving&key=AIzaSyB2md1asmg34SJTiM9SpW0Kr-ggE7CE5lk"
    #url for request, adds user input of locations


    print(url, type(url))
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response=json.loads(response.text)
    print("This is the response :::\n", response)

    #access duration in seconds from json
    try:
        duration= response['rows'][0]['elements'][0]['duration']['value']
    except Exception as e:
        duration =  e
    return duration


def nextPermutation(prepared_data: list) -> None:
    if sorted(prepared_data, key =lambda x: x["duration_ms"],reverse=True)==prepared_data:             # if nums is sorted in descening order
        return None                                 # return none
    n=len(prepared_data)                                     # 
    brk_point=-1
    for pos in range(n-1,0,-1):
        if prepared_data[pos]["duration_ms"]>prepared_data[pos-1]["duration_ms"]:
            brk_point=pos
            break
    else:
        prepared_data.sort(key=lambda x:x["duration_ms"])
    
    replace_with=-1
    for j in range(brk_point,n):
        if prepared_data[j]["duration_ms"]>prepared_data[brk_point-1]["duration_ms"]:
            replace_with=j
        else:
            break
    prepared_data[replace_with]["duration_ms"],prepared_data[brk_point-1]["duration_ms"]=prepared_data[brk_point-1]["duration_ms"],prepared_data[replace_with]["duration_ms"]
    prepared_data[brk_point:]=sorted(prepared_data[brk_point:], key= lambda x: x["duration_ms"])
    return prepared_data



# Function to find the all the
# possible solutions of the
# 0/1 knapSack problem
def knapSack(W, prepared_data, n):
	# Mapping weights with Profits
    # for i in range(len(prepared_data)):
    #         print(i, prepared_data[i])
    umap=dict()
	
    set_sol=set()
    # Making Pairs and inserting
    # o the map
    for i in range(n) :
        umap[prepared_data[i]["duration_ms"]]={"score":prepared_data[i]["score"], "id":prepared_data[i]["id"]}

    result = INT_MIN
    remaining_weight=0
    sum = 0
	
	# Loop to iterate over all the
	# possible permutations of array
    while True:
        sum = 0
		# Initially bag will be empty
        remaining_weight = W
        possible=[]

        # Loop to fill up the bag
        # until there is no weight
        # such which is less than
        # remaining weight of the
        # 0-1 knapSack
    
        prepared_data = prepared_data[:-4]
        n = len(prepared_data)
        for i in range(n) :
            # print(prepared_data[i]["duration_ms"], remaining_weight)
            if (prepared_data[i]["duration_ms"] <= remaining_weight) :
                remaining_weight -= prepared_data[i]["duration_ms"]
                sum += (umap[prepared_data[i]["duration_ms"]]["score"])
                possible.append((prepared_data[i]["duration_ms"],
                    umap[prepared_data[i]["duration_ms"]]["score"],
                    umap[prepared_data[i]["duration_ms"]]["id"])
                )
        
		
        possible.sort()
        if (sum > result) :
            result = sum

        if (tuple(possible) not in set_sol):
            # for sol in possible:
            #     print(sol[0], ": ", sol[1], ", ",end='')
            
            # print()
            set_sol.add(tuple(possible))

             

        if not nextPermutation(prepared_data):
            break
    return set_sol


def driver_function(duration, prepared_data):	
    val=[1, 1, 1, 1 , 1, 1,1,1]
    wt=[180, 177, 169, 263, 197, 213, 216, 301]
    W = duration
    n = len(prepared_data)

    # n = len(val1)
    maximum_sum_val = 0
    combo = None
    maximum = knapSack(W, prepared_data, n)
    for combo in maximum:
        sum_val = 0
        for element in combo:
            sum_val += element[0]
        
        if(sum_val>=maximum_sum_val):
            maximum_sum_val = sum_val
            best_combo = combo
              
    return best_combo

def retrieve_spotify_playlist():
    master_playlist = spotify.playlist(playlist_id="37i9dQZF1DXcBWIGoYBM5M")  # retrieve playlist
    prepare_data = []
    for element in master_playlist["tracks"]["items"]:
        if(element !=None):
            if(element["track"]!=None):
                prepare_data.append(
                     {
                        "id": element["track"]["id"],
                        "name":element["track"]["name"],
                        "artist":element["track"]["artists"][0]["name"],
                        "duration_ms": int(element["track"]["duration_ms"]/1000),
                        "score":1
                     }
                )
                # print(element["track"]["name"]
    random.shuffle(prepare_data)
    with open("master_playlist.json", "w") as f:
        json.dump(obj=master_playlist, fp=f)
    
    return prepare_data
      

# def spotify_control():
#     birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

#     with open("master_playlist.json", "w") as f:
#         json.dump(obj=master_playlist, fp=f)


#     tracks = master_playlist["tracks"]["items"][0]

#     dc = {}
#     dc["songs"] = []

#     name = master_playlist["tracks"]["items"][0]["track"]["artists"][0]["name"]
#     song_name = master_playlist["tracks"]["items"][0]["track"]["name"]
#     duration = master_playlist["tracks"]["items"][0]["track"]["duration_ms"]

#     print(duration)
#     with open("master_playlist.json", "w") as f:
#         json.dump(obj=master_playlist, fp=f)




    #### create a playlist
def create_playlist(items, user_entered_name, user_entered_desc):
    # SPOTIFY_PLAYLIST_CREATE_URL="https://api.spotify.com/v1/users/user_id/playlists \ "
    SPOTIFY_CLIENT_ID = "4aef925cd56f424582097b25919c3584"
    SPOTIFY_SECRET = "f94bffe44c804c3f83549c719a2223ff"
    REDIRECT_URL = "http://localhost:8888/callback"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            redirect_uri=REDIRECT_URL,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_SECRET,
            cache_path="token.txt"
        )
    )

    sp.user_playlist_create(user="xxfantropicgreendayxx", name=user_entered_name, public=True, collaborative=False, description=user_entered_desc)
    y = sp.user_playlists(user="xxfantropicgreendayxx")

    created_playlist_id = y["items"][0]["id"]
    # print(created_playlist_id)
    sp.playlist_add_items(playlist_id=created_playlist_id, items=items, position=0)

    return created_playlist_id

