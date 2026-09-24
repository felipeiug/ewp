"""Validação documental; executar da raiz EWP. Não valida projeto ou CAD."""
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[2]
baseline = root / 'HIPOTESES_DECISOES/output/2026-09-24_1106_integridade_inicial.json'
originals = json.loads(baseline.read_text(encoding='utf-8'))
changed_allowed = {'ENGINEERING.md', 'WORKFLOW/STEP_BY_STEP.md'}
results = []


def check(name, condition):
    results.append((name, bool(condition)))


for rel, digest in originals.items():
    if rel not in changed_allowed:
        p = root / rel
        check('Original preservado: ' + rel,
              p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == digest)

for source, backup in [
    ('ENGINEERING.md', '2026-09-24_1106_engineering_anterior.md'),
    ('WORKFLOW/STEP_BY_STEP.md', '2026-09-24_1106_fluxo_anterior.md'),
]:
    p = root / 'HIPOTESES_DECISOES/output' / backup
    check('Cópia histórica exata: ' + source,
          hashlib.sha256(p.read_bytes()).hexdigest() == originals[source])

for area in ['HIPOTESES_DECISOES', 'REQUISITOS', 'NORMAS', '00_dados']:
    check('Estrutura: ' + area, all((root / area / s).is_dir() for s in ['input', 'output'])
          and (root / area / 'README.md').is_file())

engineering = (root / 'ENGINEERING.md').read_text(encoding='utf-8')
check('Step by Step único em ENGINEERING', engineering.count('## Step by Step') == 1)
check('Status permitido', '- Status: INICIAL — CONTEXTO A CONFIRMAR' in engineering)
check('Caminhos ativos sem 00_entrada', '00_entrada/' not in engineering)
check('Dependências futuras explicitamente pendentes',
      engineering.count('- Dependência proposta, A CONFIRMAR:') == 2)
check('Fluxo externo identificado como histórico',
      (root / 'WORKFLOW/STEP_BY_STEP.md').read_text(encoding='utf-8').startswith('# Referência histórica — não executar'))

with (root / '00_dados/output/jose_da_silva_00_inventario_v01.csv').open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
check('Inventário com 33 dimensões e IDs únicos', len(rows) == 33 and len({r['id'] for r in rows}) == 33)
for row in rows:
    check('Conversão e fonte: ' + row['id'],
          Decimal(row['valor_original']) * Decimal(row['fator_para_cm']) == Decimal(row['valor_cm'])
          and (root / row['fonte']).is_file())
values = {r['id']: Decimal(r['valor_cm']) for r in rows}
check('Fechamento superior', values['C02'] + values['C03'] == values['C01'])
check('Fechamento inferior', values['C13'] + values['C14'] == values['C01'])
check('Fechamento direito', sum(values[f'C{i:02}'] for i in range(9, 13)) == values['C04'])
check('Diferença de 50 cm identificada, não corrigida',
      values['C04'] - sum(values[f'C{i:02}'] for i in range(5, 9)) == 50)
check('Extração normativa legível', 'OCUPAÇÃO DO SOLO' in
      (root / 'NORMAS/output/jose_da_silva_00_extracao_normativa_v01.txt').read_text(encoding='utf-8'))

print('# Validação documental — revisão 01\n')
print('Data: 2026-09-24. Fuso: America/Sao_Paulo. Método: script Python 3.12, SHA-256 e aritmética Decimal.\n')
print('Comando: `python 00_dados/output/jose_da_silva_00_validar_v01.py`\n')
for name, ok in results:
    print(f'- {"PASSOU" if ok else "FALHOU"}: {name}')
print(f'\nResultado: {sum(ok for _, ok in results)}/{len(results)} verificações passaram.')
print('\nLimite: estes testes validam estrutura, preservação e transcrição aritmética; não validam geometria, legislação, acessibilidade ou abertura de DWG/SKP. Etapa 00 permanece aberta.')
raise SystemExit(0 if all(ok for _, ok in results) else 1)
