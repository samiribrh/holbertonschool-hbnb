import requests

place_id = "b26f0a72-1fdb-49d1-b2ad-33b95144e677"  # Replace with the actual place_id you want to delete
url = f"http://127.0.0.1:5000/places/{place_id}"

response = requests.delete(url)

if response.status_code == 204:  # Assuming 204 is the status code for a successful deletion
    print("Place deleted successfully!")
elif response.status_code == 404:
    print("Place not found.")
else:
    print(f"Failed to delete place. Status code: {response.status_code}")
    print(response.text)
