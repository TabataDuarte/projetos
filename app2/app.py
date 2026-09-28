import os
import json
from flask import Flask, jsonify, abort
import psycopg
import redis
 
app = Flask(__name__)
cache = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, socket_timeout=1)
 
 
def db_password() -> str:
   with open(os.environ.get("DB_PASSWORD_FILE", "/run/secrets/db_password"), encoding="utf-8") as f:
       return f.read().strip()
 
 
def conectar():
   return psycopg.connect(host=os.environ["DB_HOST"], dbname="pix", user="pix", password=db_password())
 
 
@app.get("/health")
def health():
   return {"status": "ok"}
 
 
@app.get("/saldo/<int:conta>")
def saldo(conta: int):
   chave = f"saldo:{conta}"
   try:
       emcache = cache.get(chave)
       if emcache:
           return jsonify(json.loads(emcache) | {"cache": True})
   except redis.RedisError:
       pass # cache indisponível não derruba a consulta
   with conectar() as c, c.cursor() as cur:
       cur.execute("SELECT saldo FROM contas WHERE id = %s", (conta,))  # consulta parametrizada
       linha = cur.fetchone()
   if not linha:
       abort(404)
   resposta = {"conta": conta, "saldo": float(linha[0])}
   try:
       cache.setex(chave, 30, json.dumps(resposta))
   except redis.RedisError:
       pass
   return jsonify(resposta | {"cache": False})
