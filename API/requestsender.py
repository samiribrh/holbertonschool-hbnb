import requests

review_id = "0d8f02b5-3a46-4406-8169-555758d88fd9"  # Replace with the actual review_id you want to delete
url = f"http://127.0.0.1:5000/reviews/{review_id}"  # Adjust the URL as per your Flask route

response = requests.delete(url)

if response.status_code == 204:  # Assuming 204 is the status code for successful deletion
    print("Review deleted successfully!")
elif response.status_code == 404:
    print("Review not found.")
else:
    print(f"Failed to delete review. Status code: {response.status_code}")
    print(response.text)
