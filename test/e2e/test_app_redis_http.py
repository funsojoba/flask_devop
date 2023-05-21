import pytest
import requests


@pytest.mark.timeout(1.5)
def test_should_update_redis(redis_client, http_client):
    # Given
    redis_client.set("page_views", 4)


    # When
    response = requests.get(flask_url)


    # Then

    assert response.status_code == 200

    assert response.text == "This page has been viewed 5 times"

    assert redis_client.get("page_count") == b"5"