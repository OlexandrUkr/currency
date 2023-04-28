
def test_get_api_rate_list(api_client):
    response = api_client.get('/api/currency/rates/')
    assert response.status_code == 200


def test_post_api_rate_list(api_client):
    response = api_client.post('/api/currency/rates/')
    assert response.status_code == 400
    assert response.json() == {
        'buy': ['This field is required.'],
        'sale': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_get_api_sources_list(api_client):
    response = api_client.get('/api/currency/sources/')
    assert response.status_code == 200


def test_post_api_sources_list_error_400(api_client):
    response = api_client.post('/api/currency/sources/')
    assert response.status_code == 400
    assert response.json() == {
        'code_name': ['This field is required.'],
        'name': ['This field is required.'],
        'source_url': ['This field is required.']
    }


def test_post_api_sources_list_200(api_client):
    payload = {
        'code_name': 'privat48',
        'name': 'PrivatniyBank',
        'source_url': 'privat48.com'
    }
    response = api_client.post('/api/currency/sources/', data=payload)
    assert response.status_code == 201


def test_post_api_sources_list_not_double(api_client):
    payload = {
        'code_name': 'finance_ua',
        'name': 'finance_ua',
        'source_url': 'https://finance.ua/ru/currency'
    }
    response = api_client.post('/api/currency/sources/', data=payload)
    assert response.status_code == 400
    assert response.json() == {
        'code_name': ['source with this code name already exists.']
    }


def test_put_api_sources_update_source_200(api_client):
    payload = {
        'code_name': 'privat36',
        'name': 'PrivatniyBank36',
        'source_url': 'privat36.com'
    }
    response = api_client.put('/api/currency/sources/36/', data=payload)
    assert response.status_code == 200


def test_put_api_sources_update_source_400_codename_unique(api_client):
    payload = {
        'code_name': 'monobank',
        'name': 'PrivatniyBank36',
        'source_url': 'privat36.com'
    }
    response = api_client.put('/api/currency/sources/36/', data=payload)
    assert response.status_code == 400


def test_put_api_sources_update_source_400(api_client):
    response = api_client.put('/api/currency/sources/36/')
    assert response.status_code == 400
    payload = {
        'name': 'PrivatniyBank36',
        'source_url': 'privat36.com'
    }
    response = api_client.put('/api/currency/sources/36/', data=payload)
    assert response.status_code == 400


def test_put_api_sources_update_source_405_no_id(api_client):
    payload = {
        'code_name': 'monobank',
        'name': 'PrivatniyBank36',
        'source_url': 'privat36.com'
    }
    response = api_client.put('/api/currency/sources/', data=payload)
    assert response.status_code == 405


def test_patch_api_sources_part_update_source_200(api_client):
    payload = {
        'code_name': 'privat36'
    }
    response = api_client.patch('/api/currency/sources/36/', data=payload)
    assert response.status_code == 200
    payload = {
        'code_name': 'privat36'
    }
    response = api_client.patch('/api/currency/sources/36/', data=payload)
    assert response.status_code == 200
    payload = {
        'source_url': 'privat36.com'
    }
    response = api_client.patch('/api/currency/sources/36/', data=payload)
    assert response.status_code == 200


def test_patch_api_sources_part_update_source_400_codename_unique(api_client):
    payload = {
        'code_name': 'monobank'
    }
    response = api_client.patch('/api/currency/sources/36/', data=payload)
    assert response.status_code == 400


def test_patch_api_sources_part_update_source_405_no_id(api_client):
    payload = {
        'code_name': 'privat36'
    }
    response = api_client.patch('/api/currency/sources/', data=payload)
    assert response.status_code == 405
    payload = {
        'code_name': 'privat36'
    }
    response = api_client.patch('/api/currency/sources/', data=payload)
    assert response.status_code == 405
    payload = {
        'source_url': 'privat36.com'
    }
    response = api_client.patch('/api/currency/sources/', data=payload)
    assert response.status_code == 405


def test_delete_api_sources_delete_source_204(api_client):
    response = api_client.delete('/api/currency/sources/36/')
    assert response.status_code == 204


def test_delete_api_sources_delete_source_404(api_client):
    response = api_client.delete('/api/currency/sources/36/')
    assert response.status_code == 204
    response = api_client.delete('/api/currency/sources/36/')
    assert response.status_code == 404


def test_delete_api_sources_delete_source_405(api_client):
    response = api_client.delete('/api/currency/sources/')
    assert response.status_code == 405
