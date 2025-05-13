# app.py
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from asteval import Interpreter

app = FastAPI(title="API de Tarefas")

class Tarefa(BaseModel):
    id: str
    titulo: str
    feita: bool = False

class TarefaInput(BaseModel):
    titulo: str

tarefas: List[Tarefa] = []

@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    return tarefas

@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: TarefaInput):
    nova = Tarefa(id=str(uuid4()), titulo=tarefa.titulo)
    tarefas.append(nova)
    return nova

@app.post("/calcular")
async def calcular(request: Request):
    dados = await request.json()
    expressao = dados.get("expressao")

    ae = Interpreter()
    resultado = ae(expressao)

    if ae.error:
        raise HTTPException(status_code=400, detail="Expressão inválida")

    return {"resultado": resultado}
