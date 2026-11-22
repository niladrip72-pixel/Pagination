from celery import shared_task
import requests   # Importing Requests library , which sends HTTP requests to external APIs.

from .models import Post

@shared_task
def fetch_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url,timeout=30)   # It calls the external API
    response.raise_for_status()  # It raises an exception if the response has an unsuccessful HTTP status, such as 404 or 500
    posts:list = response.json()   # Converts the API response into Python Data.

    for item in posts:        # The for loop process one posts at a time.
        Post.objects.update_or_create(      # Saves each post, or updates it if that API ID already exists.
            api_id = item["id"],
            defaults={
                "user_id" : item["userId"],
                "title" : item["title"],
                "body" : item["body"],
            }
        )
    return f"{len(posts)} posts saved successfully !"    # The returns message reports how many posts were processed.

#  The advantage of update_or_create() is that clicking the fetch button repeatedly won't create duplicate posts for the same API IDs.