import requests
import gzip
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL da API
url = "https://www.sisprimecard.com.br/novo-portal/rest/v2/autenticacao/autenticar"

# Headers
headers = {
    "Content-Type": "application/json;charset=utf-8",
    "Cookie": "JSESSIONID=1D8853C49EB0D9591833DD65ECF829DF",
    "User-Agent": "Jersey/2.25 (HttpUrlConnection 0)",
}

# Dados do body
data = {
    "documento": "70;111;-65;13;-36;-70;-61;101;-83;25;-51;-4;120;102;66;-113;",
    "empresaId": 2,
    "identificadorDispositivo": "-49;-124;-44;76;9;44;-24;93;-75;-73;-127;-42;63;116;87;1;14;-6;-36;106;-123;-94;-7;83;-116;-117;7;43;13;105;-113;-3;-55;-23;-89;-63;36;99;76;-62;",
    "senha": "19;31;-30;-30;3;-72;96;-57;43;-27;29;32;-117;50;-89;-51;",
    "tipoMobile": 1
}

try:
    # Faz a requisição POST
    # IMPORTANTE: Desabilita a descompressão automática do requests
    response = requests.post(url, headers=headers, json=data, stream=True, verify=False)
    
    # Pega o conteúdo RAW (ainda comprimido se vier gzip)
    raw_content = response.raw.read()
    
    # Tenta descomprimir manualmente
    try:
        decompressed_data = gzip.decompress(raw_content)
        content_str = decompressed_data.decode('utf-8')
        print("Resposta (descomprimida com gzip):")
    except:
        # Se não for gzip, usa o conteúdo direto
        content_str = raw_content.decode('utf-8')
        print("Resposta (sem compressão):")
    

    # Se a resposta for JSON, exibe formatado
    try:
        json_response = json.loads(content_str)
        print("\n" + "="*50)
        print("JSON FORMATADO:")
        print("="*50)
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\nNão foi possível parsear como JSON: {e}")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")