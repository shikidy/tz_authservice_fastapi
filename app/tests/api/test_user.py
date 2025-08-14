from fastapi.testclient import TestClient

from app.core.settings import config


def test_login(client: TestClient):
    data = {
        "email": config.TEST_EMAIL,
        "password": config.TEST_PASSWORD
    }

    # Refresh token
    response_refresh = client.post("api/v1/user/refresh_token", json=data)
    assert response_refresh.status_code == 200, "Login response not successful"

    response_data = response_refresh.json()

    assert response_data.get("token"), "Token not returned"
    assert response_data.get("type") == "refresh", "Token type is not refresh"
    
    # Access token
    access_data = {
        "refresh_token": response_data.get("token")
    }
    response_access = client.post("api/v1/user/access_token", json=access_data)

    assert response_access.status_code == 200, "Access token request not successful"
    response_data_access = response_access.json()
    assert response_data_access.get("token"), "Access token not returned"

    # Me
    user_data_response = client.get(
        "api/v1/user/", 
        headers={
            "authorization": f"Bearer {response_data_access.get("token")}"
        }
    )

    assert user_data_response.status_code == 200, "Fetch user data request not successful"

    parsed_user_data = user_data_response.json()
    assert all((parsed_user_data.get("email"), parsed_user_data.get("firstname")))
