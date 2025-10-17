# 🧠 Técnicas de Extração de Informações da Response (HTTP)

Este guia ensina, passo a passo, **como interceptar, capturar e decodificar respostas HTTP (response)** em diferentes contextos — seja via `mitmproxy`, `requests` no Python ou diretamente com `curl`.
Essas técnicas são úteis para depuração, engenharia reversa, análise de APIs e aprendizado sobre tráfego de rede.

---

## 🧩 1. Interceptando com o `mitmproxy`

Arquivo: `interceptor.py`

### 📋 Como funciona

O `mitmproxy` atua como um proxy intermediário. Ele intercepta as requisições e respostas HTTP/HTTPS, permitindo inspecionar e até **modificar o conteúdo da response antes de chegar ao aplicativo**.

### 🚀 Passos de uso

1. Instale o `mitmproxy`:

   ```bash
   pip install mitmproxy
   ```
2. Execute o script:

   ```bash
   mitmproxy -s interceptor.py
   ```
3. Configure o proxy no dispositivo (ex: IP do PC e porta `8080`).
4. Instale o certificado do mitmproxy no Android/iOS.
5. Execute o app e veja as respostas interceptadas sendo modificadas em tempo real.

### 💡 Exemplo

O script abaixo altera o campo `nomeEmbossado` da resposta JSON da API `sisprimecard.com.br`:

```python
if "cartao" in response_data and "nomeEmbossado" in response_data["cartao"]:
    original_name = response_data["cartao"]["nomeEmbossado"]
    response_data["cartao"]["nomeEmbossado"] = "PUGNO"
    print(f"[+] Nome alterado: {original_name} -> PUGNO")
```

---

## 🧰 2. Capturando e Descomprimindo com `Python + requests`

Arquivo: `v1.py`

### 📋 Problema comum

Muitas APIs retornam dados **comprimidos em GZIP** — o que dificulta a visualização direta no terminal.

### 🧠 Solução

O script abaixo força a leitura **crua (raw)** da resposta, tenta descomprimir manualmente (se for gzip) e em seguida **formata o JSON** para leitura.

```python
response = requests.post(url, headers=headers, json=data, stream=True, verify=False)
raw_content = response.raw.read()

try:
    decompressed_data = gzip.decompress(raw_content)
    content_str = decompressed_data.decode('utf-8')
except:
    content_str = raw_content.decode('utf-8')
```

Se o conteúdo for JSON, ele é automaticamente exibido formatado:

```python
json_response = json.loads(content_str)
print(json.dumps(json_response, indent=2, ensure_ascii=False))
```

---

## 🧩 3. Usando `curl` para extrair e visualizar respostas

Arquivos: `curl.txt` e `prompt.txt`

### 📋 Comando completo

```bash
curl -H "Content-Type: application/json;charset=utf-8" \
     -H "User-Agent: Jersey/2.25 (HttpUrlConnection 0)" \
     -H "Cookie: JSESSIONID=SEU_COOKIE" \
     --data-binary '{"documento":"..."}' \
     "https://www.sisprimecard.com.br/novo-portal/rest/v2/autenticacao/autenticar" \
     --output response.gz

# Depois descomprime e mostra o conteúdo
gunzip response.gz
cat response
```

💡 Dica: se quiser encadear tudo em um único comando:

```bash
curl [opções] -o response.tmp [URL] && gzip -c response.tmp > response.gz && rm response.tmp && gunzip -c response.gz
```

---

## 🧩 4. Visualizando e Analisando via Proxy Tool (`Charles`, `Burp`, etc.)

Arquivo: `sisprime pugno.chls`

Essas ferramentas permitem interceptar requisições HTTPS de apps mobile, visualizar headers, bodies e cookies, além de exportar as sessões (`.chls` no caso do Charles).
Você pode combinar isso com o `interceptor.py` para manipular as respostas em tempo real.

---

## 🧠 Conclusão

Essas três abordagens cobrem **todas as camadas da análise de tráfego**:

| Técnica                     | Ferramenta        | Quando usar                                             |
| --------------------------- | ----------------- | ------------------------------------------------------- |
| Interceptação e modificação | `mitmproxy`       | Para analisar apps mobile e modificar responses         |
| Extração programática       | `requests + gzip` | Para automatizar requisições e tratar JSONs comprimidos |
| Linha de comando            | `curl`            | Para testes rápidos e scripts shell                     |
| Análise gráfica             | `Charles/Burp`    | Para inspecionar e exportar tráfego HTTPS               |

---

## ⚙️ Requisitos

* Python 3.8+
* pacotes: `requests`, `mitmproxy`, `urllib3`
* Ferramentas opcionais: `curl`, `Charles Proxy` ou `Burp Suite`

---

## ✍️ Autor

**Pugno** — Especialista em automação e engenharia reversa de APIs.
Focado em ensinar **debug HTTP**, **interceptação de tráfego** e **entendimento prático de redes modernas**.
