# Registro individual — AV1.4

**Limite: uma página, incluindo evidências essenciais.**  
Estudante: Samya de Lara Pinheiro — Data: 23/10/2026  
Origem: repositório desconhecido liberado no bloco; modalidade: execução/leitura própria.  

| # | Afirmação | Trecho (arquivo:linha) | Contraevidência buscada | Status |
| --- | --- | --- | --- | --- |
| 1 | A ingestão começa de fato na função `run()` de `ingest.py`. Ela busca argumentos de configuração, abre o banco, busca conceito e grava conceito. `ingest.run` é disparada pela CLI `python -m cienciometria.jobs`, por dois comandos: `ingest` (chama direto) e refresh (via `refresh_diario()`, só do ano anterior ao atual). O `scripts/rodar_tudo.sh` executa os dois.| `ingest.py:43` (começa) chamada a partir de `jobs.py (23 e 10)`; `ingest.py:44-46` (config); `ingest.py:47` (abre banco); `ingest.py:48-49` (busca e grava conceito)<br>`rodar_tudo.sh:6 e :11`| Busca no repo todo por: ingest e run( (só jobs.py e rodar_tudo.sh:6); despacho dinâmico getattr|importlib|__import__|eval|exec|subprocess (só relatorios.py:44, que não chega à ingestão); agendador cron|schedul|systemd (só comentário em rodar_tudo.sh:2); outros gatilhos (Makefile, setup.py, *.yml, .bat): nenhum. Apenas 2 caminhos. | Confirmada (2 caminhos); Incerta (agendamento: cron só em comentário) |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Resposta do assistente que parecia certa e estava errada:** ___ **Como refutei:** ___

**Caracterização antes de mudar (comando e saída gravada):** ___

| Fatia do plano | Mudança | Mecânica (codemod) ou decisão humana? | Verificação da fatia |
| --- | --- | --- | --- |
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

**Limite da leitura e condição para reabrir uma resposta:** Um cron externo ao repositório pode rodar o rodar_tudo.sh às 03:00. O código não mostra isso, só o comentário. Reabrir se aparecer configuração de cron, CI ou de outro sistema que chame jobs.py.

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: ___; tarefa delegada e contexto: ___; trecho aproveitado: ___; minha verificação/intervenção: ___. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [ ] cinco respostas com trecho; [ ] uma refutação; [ ] caracterização; [ ] plano em fatias; [ ] até uma página.
