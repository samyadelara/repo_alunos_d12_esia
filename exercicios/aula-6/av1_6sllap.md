# Registro individual — AV1.6

**Limite: uma página, incluindo evidências essenciais.**  
Estudante: Samya de Lara Pinheiro — Data: 24/10/2026
Origem: meus registros AV1.1, AV1.2 e ~~AV1.3~~ e um contexto de time descrito de forma genérica (Time de manutenção de sistema legado - mantém o sistema MiniLoja, com pouca documentação e comportamento que ninguém quer quebrar).

| Campo da medição | Meu desenho |
| --- | --- |
| Pergunta (uma frase) | Declarar o escopo e revisar o plano antes de o agente executar reduz as alterações fora do escopo nas manutenções da MiniLoja, sem quebrar o golden master nem aumentar o tempo de revisão? |
| Decisão que depende da resposta | Se as alterações fora do escopo caírem sem quebrar o golden master nem aumentar o tempo de revisão: tornar o escopo declarado e o plano revisado obrigatórios no processo do time de manutenção. Se não caírem, ou se um guardrail piorar: rever o modelo de escopo ou restringir o uso do agente. |
| Métrica primária | Número de alterações fora do escopo |
| Guardrail de qualidade | Golden master 29/29 iguais e Tempo de revisão ≤ 5 min (baseline AV1.2) |
| Baseline (de onde vem, que período) | Meus registros AV1.2 (20/10/2026): tempos semelhantes até a primeira versão revisada (mas o case é bem pequeno e limitado) [Refatoração sem escopo] = [+30/−63; removeu código "morto" fora do pedido; golden 29/29]; [Refatoração com escopo e plano revisado] = [+26/−14; só `calculo.py`; golden 29/29] |
| Período e método de comparação | 2 semanas, comparação por tarefa: 10 trechos refatoráveis (grupo X e Y), participantes de júnior a sênior sorteados em 2 grupos (com escopo + plano revisado × sem escopo), com inversão dos grupos na 2ª semana; cada tarefa é verificada pelo golden master e o tempo de revisão vem do log da ferramenta; resultado comparado por grupo, não por pessoa. |
| Confundidores previstos | Qualidade dos testes e do golden master (caso miniatura e cobertura limitada); Senioridade e habilidade com a ferramenta; Familiaridade com o código |
| Como a métrica poderia ser gamificada | Fazer menos que o pedido; Fugir da estrutura de escopo ou deixá-lo amplo demais. |

**Contramedida contra a manipulação:** Monitorar tamanho da alteração (para inspecionar casos com diff muito pequeno) e conferir se a tarefa cumpriu o critério "pronto quando" do escopo; obrigar todos os participantes a usar o template de declaração de escopo (com diretrizes claras de preenchimento), com revisão do escopo por um par antes da execução (zona amarela); usar pares de métricas: alteração fora do escopo sempre lida junto com golden master e critério de pronto.

| Tarefa recorrente candidata | Frequência e custo atual | Verificação da saída (determinística) | Permissões mínimas e orçamento | Responsável |
| --- | --- | --- | --- | --- |
| Descrição de PR a partir do diff | Acontece mais de 5x ao dia em um time de manutenção pequeno hipotético - com custo/tempo baixo de execução mas alto de revisão pela falta de padronização (há casos que descrevem PR de forma muito vaga, e outros que detalham muito) | os arquivos citados batem com git diff --stat, e a saída dos testes vai anexada, não "resumida pela IA" (no exercício 1.5, experenciamos um caso de PR de IA e fiz verificações como estas) | Job que lê: só leitura, sem segredos; job que publica: só comenta no PR; a descrição é uma proposta, e o autor do PR aprova ou edita; não roda em PR de fork; job que lê separado do job que publica com execução registrada em log; teto de custo por execução e tempo-limite de 5 min; se estourar, a execução para e nada é publicado. | (Time de manutenção) - autor do PR aprova o texto; dev da automação em si, dá manutenção e acompanha o log |

**Limite da medição e condição para interromper ou rever:** Baseline em miniatura: uma pessoa, uma tarefa fictícia por rodada (AV1.2), sem escore de mutação (AV1.3 não realizada), e período de 2 semanas, menor que as 4 a 8 recomendadas. O golden master só garante o comportamento atual, inclusive os erros, e apenas nas 29 entradas gravadas. A contagem de "fora do escopo" depende do julgamento de quem revisa. Interromper se o golden master quebrar em alguma tarefa ou se o tempo de revisão passar de 5 min de forma recorrente; rever se a versão da ferramenta mudar durante o período ou se os escopos começarem a ficar amplos demais (sinal de que a métrica virou meta).

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: Claude Code (Opus 5.5); tarefa delegada e contexto: explicação do exercício com base no README, registros AV1.1 e AV1.2, slides do bloco 6, e criação um roteiro de apoio com exemplos de outros casos, revisão de respostas minhas; trecho aproveitado: roteiro, sugestões de ajuste; minha verificação/intervenção: Escolha do contexto de time e da tarefa, escrita dos rascunhos, adequação das sugestões e conferência dos números com AV1.1/AV1.2. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [X] medição completa; [X] risco de manipulação; [X] automação com verificação; [X] limite; [X] até uma página.
