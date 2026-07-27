import requests


BASE_URL = "http://localhost:8000"


def ask_nayan(query):

    try:

        response = requests.post(
            f"{BASE_URL}/ask",
            json={
                "question": query
            },
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )


        data = response.json()


        if response.status_code == 200:

            return data.get(
                "answer",
                "I could not generate a response."
            )


        else:

            return data.get(
                "error",
                "Something went wrong."
            )


    except requests.exceptions.ConnectionError:

        return "I cannot connect to my backend right now."


    except Exception as e:
        print("API Error:", e)

        return "I am unable to answer right now. Please try again later."