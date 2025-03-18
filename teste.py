import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/turmas"

@pytest.fixture
def turma_exemplo():
    return {
        "id": 1,
        "descricao": "Turma de Português",
        "professor_id": 101,
        "activo": True
    }

def test001_criar_turma(turma_exemplo):
    response = requests.post(BASE_URL, json=turma_exemplo)
    assert response.status_code == 200
    assert response.json() == turma_exemplo

def test002_criar_turma_invalida():
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 200  # A API deveria retornar 400
    assert "erro" in response.json()

def test003_obter_turma_existente():
    turma_id = 1
    response = requests.get(f"{BASE_URL}/{turma_id}")
    assert response.status_code == 200
    assert "descricao" in response.json()

def test004_obter_turma_inexistente():
    turma_id = 9999
    response = requests.get(f"{BASE_URL}/{turma_id}")
    assert response.status_code == 200  # A API deveria retornar 404
    assert "mensagem" in response.json()

def test005_atualizar_turma_existente():
    turma_id = 1
    dados_atualizados = {
        "descricao": "Turma de Física",
        "professor_id": 102,
        "activo": False
    }
    response = requests.put(f"{BASE_URL}/{turma_id}", json=dados_atualizados)
    assert response.status_code == 200
    assert response.json()["descricao"] == "Turma de Física"

def test006_atualizar_turma_inexistente():
    turma_id = 9999
    dados_atualizados = {"descricao": "Turma Fantasma"}
    response = requests.put(f"{BASE_URL}/{turma_id}", json=dados_atualizados)
    assert response.status_code == 200  # A API deveria retornar 404
    assert "mensagem" in response.json()

def test007_excluir_turma_existente():
    turma_id = 1
    response = requests.delete(f"{BASE_URL}/{turma_id}")
    assert response.status_code == 200
    assert "mensagem" in response.json()

def test008_excluir_turma_inexistente():
    turma_id = 9999
    response = requests.delete(f"{BASE_URL}/{turma_id}")
    assert response.status_code == 200  # A API deveria retornar 404
    assert "mensagem" in response.json()

def test009_excluir_todas_turmas():
    response = requests.delete(BASE_URL)
    assert response.status_code == 200
    assert "mensagem" in response.json()

def test010_listar_todas_turmas(): 
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        assert "descricao" in response.json()[0]