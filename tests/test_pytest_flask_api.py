
import json

def test_get_help(client, get_help):
    app = client
    response = app.get("/help")
    response_json = response.json
    assert response.status_code == 200
    assert response_json == get_help

def test_get_help_single(client, get_help_single):
    app = client
    response = app.get("/help/single")
    response_json = response.json
    assert response.status_code == 200
    assert response_json == get_help_single

def test_get_help_batch(client, get_help_batch):
    app = client
    response = app.get("/help/batch")
    response_json = response.json
    assert response.status_code == 200
    assert response_json == get_help_batch

def test_get_help_languages(client, get_help_languages):
    app = client
    response = app.get("/help/languages")
    response_json = response.json
    assert response.status_code == 200
    assert response_json == get_help_languages

def test_post_single(client, expected_translation_single):
    app = client
    req_resp = expected_translation_single
    expected_request = req_resp['request']
    expected_response = req_resp['response']
    response = app.post("/translation/single", json = expected_request)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == expected_response

def test_post_batch(client, expected_translation_batch):
    app = client
    req_resp = expected_translation_batch
    expected_request = req_resp['request']
    expected_response = req_resp['response']
    response = app.post("/translation/batch", json = expected_request)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == expected_response