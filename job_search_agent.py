import requests

# --- Your Adzuna API credentials ---
APP_ID = "16f394cc"
APP_KEY = "b192cf79787eacd4d6cc5fc78ae2f996"

def search_jobs(title, location="India", results=3):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": title,
        "where": location,
        "results_per_page": results,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    jobs = []
    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name", "N/A"),
            "location": job.get("location", {}).get("display_name", "N/A"),
            "url": job.get("redirect_url")
        })

    return jobs
