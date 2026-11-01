# Roteiro AV1.6: medir e escolher o que automatizar (30 min)

Guia pessoal para preencher [av1_6sllap.md](av1_6sllap.md). Fontes: [README](README.md), [template](template-registro.md), slides do Bloco 6 e meus registros [AV1.1](../aula-1/av1_1sllap.md) e [AV1.2](../aula-2/av1_2sllap.md).

**Regra de ouro:** eu escrevo o rascunho primeiro; a IA só revisa e aponta lacunas. O raciocínio e a decisão precisam ser meus (campo Procedência/IA).

---

## Cronograma

| Min | Passo | Saída |
| --- | --- | --- |
| 0–3 | Ler a tabela "Meu baseline" abaixo | Saber que números tenho |
| 3–5 | Ler as pistas do contexto escolhido (legado) | Saber o que cada campo pede |
| 5–17 | Rascunhar a 1ª tabela (medição) + contramedida | 8 linhas + 1 frase |
| 17–25 | Rascunhar a 2ª tabela (automação) | 1 linha completa |
| 25–28 | Limite/condição de interromper + revisão pela rubrica (com IA) | Ajustes |
| 28–30 | Procedência/IA e checkboxes | Entrega |

---

## 1. Meu baseline em miniatura (0–3 min)

| Origem | Situação | Tempo até 1ª versão / até verificado | Outros números |
| --- | --- | --- | --- |
| AV1.1 T1 | Modo planejamento | 4 min / 10 min | 60% corrigido à mão; defeito CPF ausente escapou |
| AV1.1 T1 | Modo agente | 2 min / 5 min | 0% à mão; **mesmo** defeito CPF ausente escapou |
| AV1.1 T2 | Modo agente | 2 min / 5 min | 1% à mão; regex de e-mail aceita `a@.b.c` |
| AV1.2 R1 | Refatoração sem escopo | revisão 5 min | +30/−63; removeu código "morto" fora do pedido; golden 29/29 |
| AV1.2 R2 | Refatoração com escopo e plano revisado | revisão 5 min | +26/−14; só `calculo.py`; golden 29/29 |

**O que não tenho:** a AV1.3 (escore de mutação). Não invento esse número: declaro como limite ("sem medida de qualidade dos testes").

**Por que isso é só uma "miniatura":** uma pessoa, poucas tarefas, fictícias, uma rodada cada. O slide 20 pede baseline de 4 a 8 semanas num time real. Isso entra no campo de limite.

---

## 2. Contexto de time: definido ✔

**Meu contexto:** time de manutenção de sistema legado, que mantém o sistema MiniLoja, com pouca documentação e comportamento que ninguém quer quebrar. O time quer usar IA com **escopo declarado**.

O que esse contexto puxa para os próximos campos (pistas, não respostas):

| Aspecto | Pista para o meu contexto | Origem |
| --- | --- | --- |
| Problema que o escopo resolve | Agente sem escopo mexe no que não foi pedido (R1 removeu código "morto": +30/−63) | AV1.2 |
| Baseline principal | R1 sem escopo × R2 com escopo e plano revisado (+26/−14, só `calculo.py`) | AV1.2 |
| Guardrail natural | Golden master igual (29/29) + nenhum arquivo fora do escopo no `git diff --stat` | AV1.2 |
| Zona de risco | Amarela: lógica de negócio → revisão de par e checklist | Slide 23 |
| Gamificação provável | Regenerar o golden master para "passar"; diff pequeno que deixa o trabalho para depois | AV1.2 (AGENTS.md), slide 21 |
| Confundidor forte | Familiaridade: na R2 eu já conhecia o `calculo.py` | Slide 13 |
| Limite conhecido | Golden master preserva o comportamento atual, **inclusive os erros**; sem escore de mutação (sem AV1.3) | AV1.2 |
| Frase do curso que ajuda | "Em legado, a IA acelera a leitura e não substitui a conferência." | Slide 37 |

---

## 3. Rascunhar a medição (5–17 min)

Para cada linha do template: responda à pergunta-gatilho com **suas** palavras e confira se não caiu no erro comum.

| Campo | Pergunta-gatilho | Erro comum | Slide |
| --- | --- | --- | --- |
| Pergunta | O que eu quero saber, numa frase, com "sem piorar X"? | Perguntar algo vago ("a IA ajuda?") | 16, 34 |
| Decisão | Se a resposta for sim/não, o que o time faz? (continuar, expandir, restringir) | Pergunta que não muda nada | 20, 34 |
| Métrica primária | Qual número responde à pergunta? | Usar métrica de **uso** (sugestões aceitas, % de código por IA) | 17 |
| Guardrail | O que não pode piorar enquanto a primária melhora? | Esquecer a qualidade | 2, 19, 22 |
| Baseline | De onde vem o "antes" e de que período? | Não ter baseline ("existe impressão") | 20 |
| Período e método | Por quanto tempo e como comparo: antes/depois, escalonada ou por tarefa? | Comparar tarefas diferentes como se fossem iguais | 20 |
| Confundidores | O que além da IA pode mudar o número? | Listar só um | 13 |
| Gamificação | Como alguém faria o número melhorar sem melhorar o trabalho? | Não declarar | 21, 22 |

**Confundidores para considerar (slide 13):** tamanho e fechamento da tarefa · familiaridade com o código (na 2ª rodada eu já conhecia o `calculo.py`) · maturidade do repositório · qualidade dos testes (sem AV1.3 não sei) · custo de revisão · versão da ferramenta e habilidade · como se mede · seleção de tarefas.

**Exemplos de gamificação (slide 21):** PRs minúsculos · testes tautológicos (a suíte existente tem alguns de propósito) · "verificado" significar só "os testes pedidos passaram" · regenerar o golden master para "passar".

**Contramedida (slide 22), escolha 1 ou 2 e explique:** pares de métricas (velocidade **e** qualidade) · medir times, não pessoas · misturar com avaliação qualitativa · declarar de antemão a gamificação.

---

## 4. Rascunhar a automação (17–25 min)

### 4.1 Escolher a tarefa: passe pelo filtro do slide 28

- [ ] **Frequência:** acontece toda semana?
- [ ] **Custo atual:** quanto tempo leva hoje?
- [ ] **Verificabilidade:** dá para checar a saída de forma barata e determinística?
- [ ] **Variabilidade:** os casos são parecidos entre si?
- [ ] **Raio de impacto:** o que quebra se sair errado? (precisa ser baixo)
- [ ] **Custo de manter:** quem conserta quando mudar?

Fora da zona vermelha (slide 23: autenticação, pagamentos, migrações, infra, segredos).

### 4.2 Duas candidatas que combinam com a MiniLoja (slide 29)

**Triagem de falhas de CI**
- O agente lê a saída de `python -B testes/test_miniloja.py --codigo caso` e propõe um resumo: quais testes falharam e qual regra de `caso/regras.md` cada um cobre.
- Verificação determinística possível: os nomes de testes no resumo batem exatamente com as linhas `FAIL:` da saída real, e o código de saída (0 ou 1) é o mesmo.

**Descrição de PR a partir do diff**
- O agente lê o diff e propõe o texto do PR.
- Verificação determinística possível: os arquivos citados batem com `git diff --stat`, e a saída dos testes vai anexada, não "resumida pela IA".

### 4.3 Preencher as colunas (slides 30–32)

| Coluna | O que escrever |
| --- | --- |
| Frequência e custo atual | Com que frequência acontece e quanto tempo leva à mão (estimativa genérica) |
| Verificação da saída | A checagem determinística + "saída é **proposta**, uma pessoa decide" |
| Permissões mínimas e orçamento | Só leitura; sem segredos; não roda em PR de fork; job que lê separado do job que publica; limite de custo e tempo-limite |
| Responsável | Um papel (ex.: "quem está de plantão no CI"), não um nome real |

---

## 5. Limite e condição para interromper (25–26 min)

- **Limite:** um entre "baseline de uma pessoa, poucas tarefas fictícias", "sem escore de mutação (AV1.3 não feita)" ou "tarefas diferentes entre rodadas".
- **Condição para interromper ou rever:** quando eu paro ou revejo? Exemplo de formato: *"Se o guardrail piorar por N semanas seguidas, ..."* ou *"Se perceberem que a métrica virou meta, ..."*.

---

## 6. Como usar a IA (prompts prontos)

Use **depois** de escrever o seu rascunho. Peça para apontar, não reescrever.

1. **Revisar uma linha:**
   > Leia meu rascunho do campo "[campo]" em exercicios/aula-6/av1_6sllap.md. Compare com o slide [N] do Bloco 6 e o README da aula 6. Aponte o que falta ou está vago. Não reescreva.
2. **Confundidores:**
   > Para a pergunta "[minha pergunta]", quais dos oito moderadores do slide 13 eu não considerei? Responda só com a lista e uma frase por item.
3. **Gamificação:**
   > Como a métrica "[minha métrica]" poderia ser gamificada no contexto que descrevi? A contramedida que escrevi cobre isso?
4. **Automação:**
   > Minha tarefa candidata é "[tarefa]". Ela passa nos seis critérios do slide 28? A verificação que escrevi é determinística? Falta algo do slide 30?
5. **Revisão final (25–28 min):**
   > Confira meu registro contra o checklist e a rubrica do README da aula 6. Liste o que está faltando. Confira também se cabe em uma página.

**Para o campo Procedência/IA, anote enquanto usa:** ferramenta e modelo · o que pedi (quais prompts acima) · o que aproveitei · o que eu verifiquei ou mudei.

---

## 7. Checklist final (28–30 min)

Do README:
- [ ] Pergunta, decisão, métrica primária, guardrail, baseline, período e método, confundidores
- [ ] Risco de manipulação declarado + contramedida
- [ ] Tarefa recorrente + verificação (determinística, permissões, orçamento, responsável)
- [ ] Um limite da medição + uma condição para interromper
- [ ] Procedência/IA preenchida
- [ ] Até uma página

Rubrica:
- **Aplicação/decisão (30%):** a pergunta está ligada a uma decisão? A tarefa passou pelo filtro (frequência, verificabilidade, raio de impacto)?
- **Evidência (40%):** o baseline está identificado (os números da AV1.1/AV1.2)? Há guardrail? A verificação da automação está descrita?
- **Limites/alternativa (30%):** risco de a métrica virar meta, confundidores, condição para interromper?

**Critério de conclusão:** outra pessoa lê e entende como eu saberia se houve ganho e como a automação seria verificada antes de agir.
