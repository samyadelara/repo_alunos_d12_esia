# Roteiro AV1.5: revisar o PR "Adiciona exportação de vendas em CSV"

## Contexto
Você vai revisar o PR que um agente escreveu ([DESCRICAO-DO-PR.md](../../apoio/pr-bloco5/DESCRICAO-DO-PR.md) e o arquivo `.patch`) e preencher o seu registro em `exercicios/aula-5/av1_5sllap.md`. Por enquanto o patch está só no arquivo `.patch`: ele **ainda não foi aplicado** ao código (a branch atual é `bloco5_pr` e não existe `caso/miniloja/exportacao.py`). A regra do exercício é: **o texto do PR é uma alegação**. Você só escreve no registro o que você mesmo viu rodando ou lendo o código.

O roteiro aponta **onde olhar** e **que perguntas fazer**. As conclusões e o texto final ficam com você.

### Legenda: quem faz o quê
- 🖐️ **MANUAL:** você faz sozinha(o). Isso inclui tudo que **produz evidência** (rodar comandos, ler o diff, consultar o PyPI) e tudo que é **decisão** (severidade, merge, o texto do registro).
- 🤖 **IA ajuda:** a IA explica conceitos, lê o código com você, sugere casos de borda ou rascunha um teste. **O que ela responder é hipótese**: só vira achado depois que você confirma rodando ou lendo.
- ⛔ **Nunca pela IA:** dizer se um pacote existe, dizer se os testes passam, decidir bloqueia/comenta, decidir o merge. A IA pode inventar um pacote ou um resultado de teste, e a responsabilidade pelo parecer é de quem aprova.

---

## Etapa 0: preparar o terreno e aplicar o patch, cerca de 5 min · 🖐️ MANUAL
Em PowerShell, na raiz do repositório. **A ordem importa:** primeiro as fotos ANTES, depois o patch.

**0a. Fotos ANTES (sem o patch):**
```powershell
git switch -c revisao-pr5                      # branch só para a revisão (se já existir: git switch revisao-pr5)
python -B testes/test_miniloja.py --codigo caso --existentes   # FOTO "ANTES" da suíte existente
python -B testes/test_miniloja.py --codigo caso                # FOTO "ANTES" das 11 verificações
```
Anote: **quantos testes rodaram, quantos passaram e quantos falharam** em cada comando. A esperança é 26 existentes e 8 de 11 verificações passando, mas registre o que você observar, não o que espera. Isso serve para confirmar ou refutar "não há mudanças de comportamento", comparando o **antes** com o **depois**.

**0b. Aplicar o patch:** o `.patch` é só um **arquivo de texto** que descreve mudanças. Enquanto ele não é aplicado, o código do PR **não existe** na sua pasta e não há o que rodar nas Etapas 2b e 3. Nenhuma branch, local ou remota, tem esse código pronto.
```powershell
git branch --show-current                       # confirme: revisao-pr5
git apply --check apoio/pr-bloco5/0001-Adiciona-exporta-o-de-vendas-em-CSV.patch   # só testa se aplica sem erro (não muda nada)
git apply apoio/pr-bloco5/0001-Adiciona-exporta-o-de-vendas-em-CSV.patch           # agora os arquivos do PR existem na pasta
git status                                      # esperado: 2 arquivos novos (exportacao.py, test_exportacao.py) e 2 modificados (handlers.py, requirements.txt)
```
O `git apply` só altera os arquivos da pasta, **sem commit**: o código do PR não fica gravado no histórico de nenhuma branch. A Etapa 1 (ler a descrição) e a Etapa 2 (ler o diff) não dependem disso, mas o que se **roda** depende.

---

## Etapa 1: ler a descrição e listar as alegações, 5 min · 🖐️ MANUAL
Leia `apoio/pr-bloco5/DESCRICAO-DO-PR.md` e copie cada frase que **afirma algo verificável**. Há pelo menos 5:
1. "Todos os testes passam" / "27 testes passam"
2. "Não há mudanças de comportamento no código existente"
3. "Código revisado e seguro"
4. "`csv-export-helper` [é usado] para formatar o CSV"
5. O arquivo `exportacao.py` "gera o CSV de vendas" (de quem? de todos ou do usuário?)

Cada alegação vira uma linha na 2ª tabela do registro.

---

## Etapa 2: ler o patch com o funil, 10 min · 🖐️ MANUAL (leia primeiro sozinha(o); use 🤖 só para entender trechos que não ficaram claros)
Abra `apoio/pr-bloco5/0001-Adiciona-exporta-o-de-vendas-em-CSV.patch`. Linhas começando com `+` são o que foi adicionado. Para cada etapa do funil, faça a pergunta e olhe o ponto indicado:

| Funil | Pergunta | Onde olhar |
|---|---|---|
| Intenção/escopo | O PR mexe só no que diz? | Lista de arquivos no topo do patch (4 arquivos, 50 linhas). |
| Testes primeiro | O teste novo **falharia** se o código estivesse errado? | `test_exportacao.py`: o que ele verifica (`assertEqual`)? O que ele **não** verifica? O que faz o `patch.object(handlers, "_repo")` (mock)? Ele escreve um arquivo de verdade em disco? |
| Contratos (regras.md) | A função respeita a **R4** ("um usuário só pode ver os próprios pedidos")? | `exportar_vendas(usuario_id, ...)`: o parâmetro `usuario_id` é **usado** em algum lugar? O que `_repo.todos()` devolve (veja `caso/miniloja/repositorio.py`)? |
| Segurança | O usuário controla o nome do arquivo. O que acontece com `nome_arquivo = "../../algo.csv"` ou um caminho absoluto? | `os.path.join(EXPORT_DIR, nome_arquivo)`, sem nenhuma validação. |
| Segurança/erros | O que acontece se a escrita falhar? | `except Exception: pass` seguido de `return 200`. A função responde "sucesso" mesmo quando nada foi gravado? |
| Dependências | A biblioteca nova é usada? Ela existe? | `caso/requirements.txt` (a linha 1 diz "sem dependências externas"). Procure `csv_export_helper` em algum `import` do patch. |
| Estrutura/manutenção | Já existe algo igual no projeto? | `_br()` comparada com `formatar_moeda` em `caso/miniloja/formatacao.py`. Também `exportacao` usa `handlers._repo` (atributo "privado", com `_`) e `handlers` importa `exportacao` (dependência circular, resolvida com import dentro da função). `EXPORT_DIR = "exports"` é relativo à pasta de onde você roda o comando. |

Anote cada suspeita com o **arquivo e a linha do patch**.

---

## Etapa 2b: aplicar o checklist v0 da turma
**Pré-requisito:** o patch já aplicado (Etapa 0b). Os comandos da coluna "Manual" estão na **Etapa 3**: na prática, você faz a 2b e a 3 juntas, eixo por eixo.

O **funil** (tabela acima) define a **ordem** em que você olha o PR. O **checklist** define as **perguntas** que você responde em cada etapa. Para cada eixo, responda **Sim / Não / Não se aplica**, sempre com a evidência. Na coluna "Bloqueia?" está a **regra** combinada no esqueleto. Ajuste com a turma e decida você em cada caso.

| Eixo (etapa do funil) | Pergunta do checklist | O que conferir **neste PR** | 🖐️ Manual (evidência) | 🤖 IA ajuda em |
|---|---|---|---|---|
| **Escopo** (intenção e escopo) | O diff cumpre o plano? Algum arquivo ou mudança fora do pedido? | Os 4 arquivos do topo do patch batem com a lista "Mudanças" da descrição? A mudança em `requirements.txt` é necessária para exportar CSV? | Comparar o cabeçalho do patch (linhas 11 a 17) com a descrição. | Nada: é só comparar duas listas. |
| **Correção** (contratos) | O comportamento mudou onde não deveria? Casos de borda tratados? | Antes e depois das 11 verificações; o que `exportar_vendas` faz com `usuario_id`; borda: sem pedidos, nome vazio, pasta inexistente, falha de escrita. | Rodar as fotos ANTES e DEPOIS (Etapas 0 e 3) e os scripts de reprodução. | Prompt: "Liste casos de borda para esta função [cole]". **Você testa cada um.** |
| **Testes** (testes primeiro) | Algum teste falharia sem a mudança? Algum teste existente foi alterado ou removido? As asserções são reais? | `test_exportacao.py` usa mock e confere só `status` e `linhas`. Ele detectaria o bug da R4? Existe algum `-` (remoção) em `testes_existentes/`? | Contar os testes antes e depois; procurar no patch linhas `-` em arquivos de teste; perguntar-se "se eu exportasse pedidos de todo mundo, este teste falharia?". | Prompt: "Que defeitos este teste NÃO detectaria? [cole]". Prompt 4 da Etapa 4 para rascunhar o teste que falta. **Você roda o teste e confirma que ele falha hoje.** |
| **Segurança** (segurança) | Entrada externa validada? Quem pode acessar o quê? Há segredos? Consultas parametrizadas? | `nome_arquivo` sem validação (path traversal); R4 (acesso a pedidos de outros); segredos: procurar senha/token no diff; consultas: não há banco de dados, então provavelmente "não se aplica" (justifique). | Rodar os scripts da R4 e do `../fora_da_pasta.csv`; ler o diff à procura de segredos. | Prompts 2 e 3 da Etapa 4 (explicar path traversal e `except: pass`); pedir sugestões de validação do nome de arquivo. |
| **Dependências** (segurança e dependências) | Há algo novo? Existe, é mantido, é necessário, a versão está fixada? | `csv-export-helper==0.4.2`: a versão está fixada (`==`). Existe? Quem mantém? Algum `import` usa o pacote? O projeto permite só a biblioteca padrão (`CLAUDE.md`, `requirements.txt` linha 1). | `Select-String` por `csv_export_helper`; `pip index versions` ou pypi.org (**não instalar**). | ⛔ Não pergunte à IA se o pacote existe. Use só o prompt 6 (como avaliar um pacote). |
| **Estrutura** (estrutura e manutenção) | Duplica algo que já existe? Quebra regra de camada? Muda API pública? | `_br` comparada com `formatar_moeda` (`formatacao.py`); `exportacao` acessando `handlers._repo` (a regra de negócio dependendo da camada HTTP, e de um atributo privado) e o import circular; nova função pública `get_exportacao` em `handlers.py`. | Abrir `formatacao.py` e comparar as duas funções; ler os imports dos dois arquivos. | Prompt: "O que é um import circular e por que acessar `_repo` de outro módulo é um problema de camadas?" |
| **Desempenho e escala** (estrutura) | Consulta dentro de laço, laço aninhado, falta de paginação? Foi medido com volume realista? | `_repo.todos()` carrega todos os pedidos de uma vez, sem filtro nem paginação. Ninguém mediu. | Ler o laço `for p in pedidos`; registrar "não medido" em **Limite da revisão**. | Prompt: "O que acontece com esta função com 1 milhão de pedidos?" (resposta conceitual; não é evidência). |
| **Manutenção** (estrutura e manutenção) | Alguém do time consegue explicar? Há decisão que merece um registro? | Tente explicar `exportar_vendas` em 2 frases. O `except Exception: pass` esconde erros de quem for manter. Onde os arquivos vão parar (`EXPORT_DIR` relativo) é uma decisão sem registro. | Escrever a sua explicação em 2 frases; se não conseguir, isso é um achado. | Prompt 1 da Etapa 4 (explicar linha a linha) **depois** que você tentou sozinha(o). |
| **Processo** (execução independente) | A participação de IA está declarada? Os comandos do PR são reproduzíveis? | A descrição diz "escrito pelo agente" (declarado). O comando de "Como testar" dá mesmo 27 testes passando? "Revisado e seguro": por quem, com que evidência? | Rodar **exatamente** o comando da descrição e anotar a saída. | Nada: aqui a evidência tem que ser a sua execução. |

**Como transformar o checklist em achados:** toda resposta "sim, há problema" vira uma linha da tabela de achados do registro (Etapa 6), com o arquivo, o impacto, a severidade e o teste. As respostas "não" e "não se aplica" não viram achado, mas ajudam a sustentar a decisão e o **limite da revisão**.

---

## Etapa 3: caixa de ferramentas da execução (use **durante** a 2b), 10 min · 🖐️ MANUAL (a IA pode explicar uma saída de erro, mas quem roda é você)
Pré-requisito: o patch aplicado (Etapa 0b). Os comandos abaixo são as evidências que a coluna "Manual" da 2b pede: rode cada um quando chegar ao eixo correspondente.

```powershell
python -B testes/test_miniloja.py --codigo caso --existentes   # FOTO "DEPOIS": são 27? Todos passam?  (eixos Testes e Processo)
python -B testes/test_miniloja.py --codigo caso                # Mudou algo em relação ao ANTES?       (eixo Correção)
```

**Como testar um caso de borda** (vale para os scripts abaixo e para os casos que a IA sugerir):
1. Escreva o **esperado antes de rodar**, a partir do `regras.md` ou do bom senso, nunca do código.
2. Rode a função com essa entrada.
3. Compare o esperado com o observado. Se forem iguais, anote "ok". Se forem diferentes, é um achado.
4. Registre a entrada, o esperado, o observado e o comando.

**Reproduzir a R4** (salve como script no scratchpad ou rode com `python -B -c`):
```python
import sys, csv; sys.path.insert(0, "caso")
from miniloja import handlers
handlers.post_pedidos(1, {"itens": [{"sku": "BOLA-01", "preco": 50.0, "qtd": 1}]})
handlers.post_pedidos(2, {"itens": [{"sku": "BOLA-01", "preco": 80.0, "qtd": 1}]})
print(handlers.get_exportacao(1, "r4.csv"))
print(open("exports/r4.csv", encoding="utf-8").read())   # aparecem pedidos do usuário 2?
```
**Reproduzir o caminho** (veja onde o arquivo foi parar, sem apagar nada):
```python
print(handlers.get_exportacao(1, "../fora_da_pasta.csv"))  # foi criado fora de exports/?
```
**Reproduzir o erro engolido:**
```python
print(handlers.get_exportacao(1, "pasta_inexistente/x.csv"))  # status 200, mas o arquivo existe?
```
**Dependência** (só consultar, **não instale**):
```powershell
Select-String -Path caso\miniloja\*.py -Pattern "csv_export_helper"   # algum import?
pip index versions csv-export-helper                                   # existe no PyPI? (ou abra pypi.org/project/csv-export-helper)
```
Se o pacote existir, veja no PyPI quem mantém, a data e o repositório. Se não existir, isso é um sinal clássico de pacote "alucinado" pela IA, e alguém poderia registrar esse nome com código malicioso.

**Ao final de tudo (desfazer o patch):** `git status` mostra o que o patch e os seus testes criaram (a pasta `exports/` e o arquivo `fora_da_pasta.csv`).
```powershell
git checkout -- caso          # desfaz as modificações em handlers.py e requirements.txt
git clean -n caso exports     # SÓ LISTA os arquivos novos que seriam apagados nessas pastas
git clean -f caso exports     # apaga, depois de conferir a lista
git status                    # confira se sobrou algo, como o fora_da_pasta.csv (apague à mão depois de anotar onde ele foi parar)
```
⚠️ Não rode `git clean -f` sem indicar as pastas: o seu `av1_5sllap.md` e este roteiro também não estão commitados e seriam apagados.

---

## Etapa 4: prompts para usar IA sem terceirizar o parecer · 🤖 IA ajuda
Use a IA como **tutora**, não como revisora. Bons prompts:

1. *Entender:* "Explique linha a linha o que faz `exportar_vendas` neste diff, sem dizer se há bugs. [cole o trecho]"
2. *Conceito:* "O que é *path traversal* e por que `os.path.join('exports', nome)` pode ser perigoso quando `nome` vem do usuário? Mostre um exemplo em Python."
3. *Conceito:* "Por que `except Exception: pass` é considerado má prática? Qual o impacto em uma função que devolve status HTTP?"
4. *Teste:* "Escreva um teste `unittest` que **falhe** se `exportar_vendas(1, ...)` incluir pedidos de outro usuário. Use o repositório real, sem mock."
5. *Desafio:* "Eu acho que [seu achado]. Que argumento contra essa conclusão você daria?"
6. *Dependência:* "Como eu verifico se um pacote do PyPI é legítimo? Quais sinais de alerta procurar?"

**Como refletir sobre cada resposta da IA:**
- Ela afirmou um fato sobre o código? **Rode ou leia para confirmar.** Se não conseguir reproduzir, não vai para o registro.
- O teste que ela escreveu **falha hoje** (com o bug) e **passaria** com a correção? Se não falha, ele não prova nada (e seria o mesmo defeito do teste do PR).
- A severidade que ela sugere bate com o contrato (`regras.md`) e com o impacto real? A decisão é sua.
- Anote o que foi da IA e o que você verificou, para o campo "Procedência/IA".

---

## Etapa 5: decidir a severidade · 🖐️ MANUAL (⛔ não delegue)
Regra prática:
- **Bloqueia:** viola o contrato (`regras.md`), cria um risco de segurança, faz a função mentir sobre o resultado, ou adiciona uma dependência não verificada que contraria a restrição do projeto.
- **Comenta:** não quebra regra nem segurança, mas piora a manutenção (duplicação, acesso a atributo privado, import circular, pasta relativa).

Pergunte a si mesma(o): "se isso for para produção, alguém é prejudicado?" Se a resposta for sim, bloqueia.

---

## Etapa 6: preencher o registro (`exercicios/aula-5/av1_5sllap.md`), 5 min · 🖐️ MANUAL (🤖 só para revisar a clareza do texto ou encurtá-lo para caber em uma página, sem mudar o conteúdo)
**Cabeçalho:** nome, data 24/10/2026, modalidade = **execução própria** (se rodou a Etapa 3).

**Tabela de achados:** escolha seus 4 a 6 achados mais fortes. Coloque os bloqueantes primeiro. Modelo de linha, usando um achado do tipo "comenta":

> | 5 | `caso/miniloja/exportacao.py` (`_br`) | Duplica `formatar_moeda` de `formatacao.py`; duas fontes da verdade para formato de moeda podem divergir. | Comenta | Usar `formatar_moeda`; teste: `assertEqual(linha_csv[2], formatar_moeda(10.0))`. |

Cada achado bloqueante precisa de: **impacto concreto** (quem é prejudicado e como) e um **teste que falharia** (nome e o que ele afirma), como o da reprodução da Etapa 3.

**Tabela de alegações:** para cada frase da Etapa 1, marque Confirmada ou Refutada, com a **evidência**: o comando que você rodou e o resultado (ex.: "rodei X; saída: 27 OK") ou o trecho de código (ex.: "`usuario_id` não é usado; `_repo.todos()`"). Atenção: "testes passam" pode ser **confirmada** e ainda assim insuficiente. Explique que o teste usa mock e só confere `status` e `linhas`.

**Dependência nova:** nome e versão, se existe (resultado do `pip index` ou do PyPI), quem mantém, e se é necessária (algum import?). Lembre a restrição de "somente biblioteca padrão".

**Decisão:** por exemplo, "Rejeito / peço mudanças. Aprovo se: (1)... (2)... cada um com o teste correspondente passando". Diga também que **quem aprova responde pelo merge** (isso vale ponto na rubrica).

**Limite da revisão:** o que você **não** fez, por exemplo: não rodei análise estática nem testes de abuso automatizados, não testei em Linux ou outro sistema operacional, não auditei o código do pacote externo, e a revisão foi feita sobre o patch, não em um ambiente real.

**Procedência/IA:** ferramenta e modelo, quais prompts da Etapa 4 você usou, o que aproveitou e o que você verificou rodando.

**Checagem final (rubrica):** cada bloqueante tem impacto e teste? A decisão se sustenta **sem** ler a descrição do PR? Cabe em uma página? Se a tabela ficar longa, encurte as frases e não corte as evidências.

---

## Verificação deste roteiro
- Etapas 0 e 3 produzem as evidências (saídas de comando) que entram nas tabelas.
- O critério de conclusão do README: outra pessoa consegue reproduzir cada achado com o comando ou teste que você escreveu.
