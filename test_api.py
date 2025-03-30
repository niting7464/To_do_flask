import requests

base_url = "http://127.0.0.1:5000"
def test_api(endpoint, method="GET", data=None):
    url = f"{base_url}/{endpoint}"
    
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json=data)
    elif method == "PUT":
        response = requests.put(url, json=data)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        return f"Invalid method: {method}"

    # Debugging output to see raw response
    print(f"Raw response from {url}: {response.status_code} {response.text}")

    try:
        return response.status_code, response.json()
    except requests.exceptions.JSONDecodeError:
        return response.status_code, "Response is not JSON"



# print("Testing Home Route:", test_api(""))
# print("Testing Add Task:", test_api("tasks/add", "POST", {"content": "My New Task"}))
# print("Testing Delete Task:", test_api("tasks/delete/1", "DELETE"))


