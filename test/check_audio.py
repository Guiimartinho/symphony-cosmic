# check_audio.py (Versão 4 - Correção do erro 'tuple')
from pyo import pa_get_devices_infos

print("--- Análise Detalhada dos Dispositivos de SAÍDA ---")

try:
    # CORREÇÃO: pa_get_devices_infos() retorna uma TUPLA de dicionários.
    # Vamos iterar diretamente sobre esta tupla usando enumerate().
    all_devices_info = pa_get_devices_infos()
    
    # Itera sobre cada dicionário de dispositivo na tupla
    for device_id, device_info in enumerate(all_devices_info):
        # Filtra para mostrar apenas dispositivos de SAÍDA de áudio
        if device_info.get('output_channels', 0) > 0:
            print("-" * 25)
            nome = device_info.get('name', 'Nome não disponível')
            api = device_info.get('host api_name', 'API não disponível')
            
            print(f"  Nome do Dispositivo: {nome}")
            print(f"  API de Áudio: {api}")
            print(f"  ID do Dispositivo: {device_id}")

    print("-" * 25)
    print("\nDiagnóstico concluído.")

except Exception as e:
    print(f"\nOcorreu um erro ao verificar os dispositivos: {e}")