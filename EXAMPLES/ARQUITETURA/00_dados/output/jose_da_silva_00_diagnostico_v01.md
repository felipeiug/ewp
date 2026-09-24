# Casa 001 — diagnóstico da etapa 00 — revisão 01

Data: 2026-09-24. Fuso: America/Sao_Paulo. Etapa aberta; diagnóstico documental concluído, desenhos pendentes. Este registro não é projeto legal ou executivo.

## Fontes e método

Leitura visual de `00_dados/input/croqui.jpg`; requisitos em `REQUISITOS/convencoes.md`, `restricoes.md` e `unidades.md`; contexto em `ENGINEERING.md`; fluxo anterior preservado em `HIPOTESES_DECISOES/output/`. Carimbo preservado, sem emissão de prancha. Inventário em `jose_da_silva_00_inventario_v01.csv`. Análise da fonte normativa em `NORMAS/output/jose_da_silva_00_fontes_v01.md`.

Não se mediram pixels nem se tomou a malha do papel como escala. Cotas explícitas em metros foram multiplicadas por 100; dimensões internas sem sufixo foram interpretadas na mesma unidade do croqui, com essa inferência identificada no CSV. Valores do lote e pé-direito são requisitos, não observações do croqui. Níveis: unidade A CONFIRMAR, pois `unidades.md` contém “metro (`cm`)”.

## Ambientes identificados

Três dormitórios, dois banheiros, cozinha, estar, jantar e circulação central sem dimensão explícita. Medidas nominais dos ambientes transcritas no CSV. Garagem não aparece no croqui.

## Fechamento das cotas

- Superior: 375 + 375 = 750 cm; inferior: 420 + 330 = 750 cm. Fechamento aritmético de largura, sem comprovar inclusão de paredes.
- Direita: 350 + 150 + 300 + 350 = 1150 cm, igual ao total indicado.
- Esquerda: 350 + 300 + 150 + 300 = 1100 cm; diferença para o total direito = 50 cm. Há um ressalto desenhado na base direita, mas sua dimensão não está cotada; não atribuir automaticamente os 50 cm ao ressalto sem confirmação.
- As larguras dos dormitórios superiores somam a largura total: se fossem medidas livres internas e largura externa, não sobraria espessura para paredes. Confirmar se as cotas são livres, entre eixos ou externas; não corrigir os ambientes arbitrariamente.
- Lote documental: 1050 × 1400 cm. Somente para comparação aritmética, alinhando 750 com 1050 e 1150 com 1400, restariam 300 cm na largura e 250 cm no comprimento. Não são recuos definidos nem prova de espaço para estacionamento.

## Paredes, acessos e garagem

Paredes estão representadas, mas sem espessuras cotadas. Portas e janelas não têm dimensões nem alturas; largura da circulação e conflitos de giro não podem ser validados. O banheiro superior direito aparenta acesso pelo dormitório superior direito; confirmar intenção de suíte. Não foi identificado ambiente inequivocamente inacessível apenas pela representação, mas acessibilidade e circulação não foram comprovadas.

A garagem para dois veículos não está desenhada. Sem posição da casa no lote, localização da rua/portão, dimensões dos veículos e recuos aplicáveis, não é possível validar duas vagas e manobra. Não se propôs diminuir cômodos ou ocupar recuos para acomodá-las.

## Ferramentas

- Python 3.12 disponível e usado para registros e verificações aritméticas.
- `pdftotext`: E:/miktex/miktex/bin/x64/pdftotext.exe; extração concluída. Uma primeira exibição no terminal falhou por codificação cp1252, corrigida com saída UTF-8; o PDF permaneceu intacto.
- SketchUp 2016: executável presente em C:/Program Files/SketchUp/SketchUp 2016/SketchUp.exe, versão de arquivo 16.0.19912. Registro de instalação informa 16.1.1449; divergência registrada. Aplicativo não iniciado; licença, salvamento e reabertura ainda não testados.
- AutoCAD 2019: registro de instalação informa versão 23.0.46.0 em D:/sketchup/AutoCad/AutoCAD 2019/. Unidade D: indisponível e executáveis acad.exe/accoreconsole.exe ausentes nesse caminho. Não encontrados no PATH nem nas pastas Autodesk em Program Files, E:/Sketchup e E:/Program Files examinadas. Isso não prova ausência em outros locais.
- E:/Sketchup/SketchUp.exe também existe, mas sem versão de arquivo reportada; não usado como ambiente de referência.

Produzir e abrir DXF/SKP nas versões solicitadas continua pendente; nenhum arquivo substituto foi apresentado como editável validado.

## Solicitação consolidada para prosseguir

Informar em uma resposta, marcando o que ainda não for conhecido:

1. Face do lote voltada à rua, norte, posição pretendida da casa e garagem/portão, dimensões dos dois veículos e se devem estacionar lado a lado ou em fila.
2. Níveis do terreno/piso e unidade desejada para as cotas altimétricas (cm ou m).
3. Se as medidas são internas livres, externas ou entre eixos; espessuras das paredes; confirmação do ressalto inferior e de sua medida; largura da circulação; dimensões/alturas/posição de portas e janelas; confirmação do acesso do banheiro superior pelo dormitório.
4. Identificação cadastral do lote ou parâmetros oficiais da Informação Básica/Geosiurbe que permitam verificar implantação e legislação; confirmação do endereço e dimensões declarados.
5. Local acessível da instalação funcional do AutoCAD 2019, se disponível.
6. Confirmação das dependências propostas: etapa 03 após 01 e 02 revisadas; etapa 04 após 03 aprovada. Essa confirmação não equivale à aprovação da etapa 00.

Gate: ENGINEERING.md, Step by Step / etapa 00, exige validações e aprovação expressa antes do avanço. A emissão dos desenhos está pendente dos dados acima; nenhuma etapa posterior foi executada.
