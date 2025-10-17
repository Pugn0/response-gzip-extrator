from mitmproxy import http
import json

def response(flow: http.HTTPFlow) -> None:
    """
    Intercepta e modifica a resposta da API SisPrimeCard
    """
    # Verifica se é a URL que queremos interceptar
    if "sisprimecard.com.br" in flow.request.pretty_url and "autenticar" in flow.request.pretty_url:
        
        try:
            # Decodifica a resposta JSON
            response_data = json.loads(flow.response.text)
            
            # Modifica o campo nomeEmbossado
            if "cartao" in response_data and "nomeEmbossado" in response_data["cartao"]:
                original_name = response_data["cartao"]["nomeEmbossado"]
                response_data["cartao"]["nomeEmbossado"] = "PUGNO"
                
                print(f"[+] Nome alterado: {original_name} -> PUGNO")
                
                # Você pode modificar outros campos também
                # response_data["cartao"]["numero"] = "5282 23** **** 0000"
                # response_data["cartao"]["limiteCredito"] = "99.999,99"
            
            # Atualiza a resposta com os dados modificados
            flow.response.text = json.dumps(response_data, ensure_ascii=False)
            
            print("[+] Resposta modificada com sucesso!")
            print(f"[+] Nova resposta: {flow.response.text[:200]}...")
            
        except Exception as e:
            print(f"[-] Erro ao modificar resposta: {e}")

# Para usar este script:
# 1. Instale o mitmproxy: pip install mitmproxy
# 2. Execute: mitmproxy -s interceptor.py
# 3. Configure o proxy no seu dispositivo (porta 8080)
# 4. Instale o certificado do mitmproxy no dispositivo
# 5. Execute o app e veja a mágica acontecer!