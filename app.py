# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="API de Tarefas")

class Tarefa(BaseModel):
    id: str
    titulo: str
    feita: bool = False

class TarefaInput(BaseModel):
    titulo: str

# Banco de dados temporário em memória
tarefas: List[Tarefa] = []

@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    return tarefas

@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: TarefaInput):
    nova = Tarefa(id=str(uuid4()), titulo=tarefa.titulo)
    tarefas.append(nova)
    return nova

@app.put("/tarefas/{id}", response_model=Tarefa)
def marcar_como_feita(id: str):
    for t in tarefas:
        if t.id == id:
            t.feita = True
            return t
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: str):
    for t in tarefas:
        if t.id == id:
            tarefas.remove(t)
            return {"mensagem": "Tarefa removida"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
