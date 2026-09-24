"""Consultas publicas, somente leitura; evidencias gravadas dentro da etapa 00."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import re
import sys

OUT=Path(__file__).resolve().parent / 'consulta_lote_v02'
OUT.mkdir(exist_ok=True)

def fetch(item):
    name,url=item
    record={'url':url,'data':datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat()}
    try:
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response:
            raw=response.read()
            record.update(status=response.status,bytes=len(raw))
        (OUT/(name+'.txt')).write_bytes(raw)
        text=raw.decode('utf-8',errors='replace')
        record['scripts']=re.findall(r'<script[^>]+src=[^>]+',text)
        if 'GetCapabilities' in url:
            record['nomes']=re.findall(r'<(?:\w+:)?Name>([^<]+)</(?:\w+:)?Name>',text)
        else:
            record['inicio']=text[:400]
    except Exception as e:
        record['erro']=str(e)
    (OUT/(name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return record

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    items=[
        ('bhmap','https://bhmap.pbh.gov.br/v2/home.html'),
        ('wfs_oficial','https://bhmap.pbh.gov.br/v2/api/idebhgeo/wfs?service=WFS&request=GetCapabilities'),
        ('geosiurbe','https://webmapsiurbe.pbh.gov.br/'),
    ]
    if '--enderecos' in sys.argv:
        base='https://bhmap.pbh.gov.br/v2/api/idebhgeo/wfs?'
        common=dict(service='WFS',version='1.0.0',request='GetFeature',
                    typeName='ide_bhgeo:ENDERECO',outputFormat='application/json',maxFeatures=2000)
        filters={
            'endereco_exato': "NOME_LOGRADOURO ILIKE 'OLIVEIRA' AND NUMERO_IMOVEL = 1356",
            'enderecos_rua': "NOME_LOGRADOURO ILIKE 'OLIVEIRA' AND NOME_BAIRRO_POPULAR ILIKE 'CRUZEIRO'",
            'cep_numero': "CEP = 30310150 AND NUMERO_IMOVEL = 1356",
        }
        items=[(name,base+urlencode(dict(common,CQL_FILTER=condition))) for name,condition in filters.items()]
    for result in ThreadPoolExecutor(3).map(fetch,items):
        result.pop('nomes',None)
        print(json.dumps(result,ensure_ascii=False))
