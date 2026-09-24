# Decisão — prioridade das cotas externas

Data: 2026-09-24 16:31, America/Sao_Paulo.

## Autoridade e alteração

Instrução expressa do usuário: “Prevaleça sempre com as cotas externas e altere as internas da forma que precisar.”

Requisito anterior, preservado aqui: “O imóvel deverá ter os mesmos ambientes e medidas do croqui.” Fonte: `REQUISITOS/convencoes.md`.

Decisão: manter os ambientes e as cotas externas; adaptar as internas para acomodar espessuras e circulação. A atualização pontual de `REQUISITOS/convencoes.md` formaliza a alteração autorizada. Não altera normas nem concede aprovação às etapas posteriores.

## Aplicação geométrica — revisão 02

- Largura externa 750 cm; lateral direita 1150 cm; lateral esquerda 1100 cm; trechos frontais 420/330 cm. Avanço de 50 cm resulta da diferença entre as laterais e é coerente com o croqui.
- Cadeias longitudinais preservadas: esquerda 350/300/150/300 cm e direita 350/150/300/350 cm. Pontos intermediários interpretados como eixos das divisórias de 9 cm; o croqui não detalha faces desses encontros. Esta é uma decisão de representação, não uma nova medida observada.
- Faces externas fixas; paredes externas voltadas para dentro, com 15 cm; internas com 9 cm; altura de parede 300 cm, conforme pé-direito. Cobertura e platibanda permanecem para desenvolvimento posterior, sem dimensão inventada nesta etapa de paredes.
- Corredor com 100 cm livres, entre x=320 e x=420 cm. Dimensões internas recalculadas na fonte geométrica JSON. Os dois dormitórios posteriores têm recortes de acesso; as cotas máximas não representam retângulos inteiramente utilizáveis.
- Mantida a topologia de acessos: banheiro direito permanece acessível pela lateral externa. A janela desse banheiro foi proposta sobre a porta (bandeira), pois a porta e uma janela lateral independente disputariam o comprimento disponível. Esta escolha de abertura decorre da autonomia já registrada para portas/janelas e depende de conferência de ventilação.
- Portas de 80 × 210 cm, entrada de 90 × 210 cm; janelas e passa-pratos descritos no memorial. Valores escolhidos pelo agente, não transcritos do croqui. São vãos geométricos, sujeitos ao detalhamento de caixilhos, marcos e estrutura.
- Terreno plano, rua abaixo e norte dispensado nesta fase: requisitos preexistentes, não novas inferências.

## Resultado e limitações

Gerados DXF AC1027 e SKP 2016, em `00_dados/output/`, com revisão v02. Grupos, materiais e layers do SketchUp organizados; em 2016 a nomenclatura do aplicativo é layers, não tags. O SKP foi gravado e reaberto pela biblioteca instalada do SketchUp 2016; nenhuma abertura pela interface gráfica é alegada. DXF lido e auditado com ezdxf; abertura em AutoCAD 2019 não executada.

Etapa 00 parcial: decisão dimensional atendida; implantação, parâmetros urbanísticos e aprovação da etapa permanecem pendentes. Não executar a etapa 01 nem a 02 com base apenas nesta decisão. Estado do projeto ATIVO, sem bloquear todo o projeto pela pendência cadastral.

Fontes e hashes, versões, testes e arquivos gerados: `00_dados/output/jose_da_silva_00_validacao_v02.json`. Interpretações e dimensões detalhadas: `00_dados/output/jose_da_silva_00_memorial_v02.md`. O diagnóstico v01 permanece como histórico anterior à decisão.
