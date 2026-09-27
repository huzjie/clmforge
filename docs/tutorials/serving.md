# 教程：部署 HTTP 服务

```bash
python -m clmforge serve --host 0.0.0.0 --port 8765 --token secret
curl -H "Authorization: Bearer secret" \
     -X POST http://127.0.0.1:8765/decide \
     -d '{"state": "2+3?", "keys": ["calc", "search"]}'
```

Docker：`docker build -t clmforge . && docker run -p 8765:8765 clmforge`

K8s：`kubectl apply -f k8s/`；Helm：`helm install clmforge helm/clmforge`。
