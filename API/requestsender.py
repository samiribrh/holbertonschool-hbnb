import requests

place_id = "e2ef60c6-95ff-4afb-bc5a-bf9f19603a2a"  # Replace with the actual place_id for which you want to fetch reviews
url = f"http://127.0.0.1:5000/places/{place_id}/reviews"

response = requests.get(url)

if response.status_code == 200:  # Assuming 200 is the status code for successful retrieval
    reviews = response.json()
    if reviews.get('message'):
        print(reviews['message'])
    else:
        for review_id, review_data in reviews.items():
            print(f"Review ID: {review_id}")
            print(f"Review Data: {review_data}")
else:
    print(f"Failed to fetch reviews. Status code: {response.status_code}")
    print(response.text)
