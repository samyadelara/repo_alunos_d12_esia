# Registro individual — AV2

**Limite: duas páginas de análise + anexo técnico curto.** 
Estudante: Samya de Lara Pinheiro — Data: 21/10/2026 — Caminho: B (MiniLoja)

**Escopo (seis campos):** objetivo refatorar `calcular_total` separando desconto, frete e taxa em funções específicas, e cobrir a função com testes que partem do contrato; pode tocar `caso/miniloja/calculo.py` (refatoração e docstring) e criar testes novos `avaliacoes/av2/test_contrato_calculo.py`; não pode tocar assinatura pública `calcular_total(itens, cupom=None, uf="PE")`, `testes/`, `caso/regras.md`, golden master nem outros arquivos do caso; invariantes golden master exato (29/29) e verificações iguais à linha de base; pronto quando golden 29/29, verificações e suíte nova verdes e mutação de `calculo.py` só com sobrevivente equivalente; pare e pergunte se achar algo que pareça bug, ela reporta, não corrige.

**Plano do agente: o que cortei ou corrigi:** o plano da refatoração é o do bloco 2 (rodar linha de base, extrair `_aplicar_desconto`, `_calcular_frete`, `_aplicar_taxa`, manter a assinatura, rodar golden e verificações, reportar sem corrigir). Usei a versão do agente com escopo (+26/−14). Na AV2 o agente ofereceu duas opções para as divergências com o contrato: (a) manter a refatoração pura e registrar, ou (b) corrigir `>= 200` e o meio para cima com `Decimal`. Cortei a (b), porque mudaria o comportamento e o golden master numa entrega que é de refatoração. Também não deixei corrigir `test_cadastro.py` nem o `mutacao_manual.py`, que estão fora do escopo.

**Comportamento preservado:** método golden master do bloco 2 (`gerar.py`/`comparar.py`), com comparação exata de valor e tipo; entradas 29 casos gravados a partir do código original (UFs, cupons, flag NATAL, fronteira de 200, carrinho vazio); resultado `python -B exercicios/aula-2/golden_master/comparar.py --codigo caso` → `29/29 casos iguais; 0 diferente(s).`, saída 0, antes e depois da docstring. Verificações `python -B testes/test_miniloja.py --codigo caso` → 11/11 OK (as v08–v10 passam por causa das tarefas do bloco 1).

| Teste (derivado de qual regra do contrato) | Como provei que falharia (sabotagem, mutação ou diferencial) | Resultado |
| --- | --- | --- |
| `test_rj_frete_e_taxa` (R1.3/R1.4): 40,00 RJ → 40 + 21,50 = 61,50 × 1,06 = **65,19** | Mutação "frete RJ" (21.5 → 22.5) **sobrevivia** na suíte existente, porque o único teste de RJ usa FRETEGRATIS. Na suíte nova ele morre | Passa no código; mata frete RJ e taxa RJ |
| `test_natal_com_campanha_ativa` (R1.2): 50,00 SP NATAL com flag → 40 + 19,90 = 59,90 × 1,07 = 64,093 → **64,09** | Mutação "NATAL 20% → 21%" **sobrevivia**, porque o teste existente só faz `assertIsNotNone`. Na suíte nova ele morre | Passa no código; mata NATAL |
| `test_fronteira_exata_200_tem_frete_gratis` (R1.3 "maior ou igual"): 100,00 × 2 PE → frete 0; 200 × 1,05 = **210,00** | Código devolve 223,55, por isso fica como `expectedFailure` (ADR-001). Sabotagem `> 200` → `>= 200` numa cópia: vira `unexpected success` e a suíte fica vermelha | Divergência registrada; detecta se alguém mexer no limite |
| `test_arredondamento_meio_para_cima` (R1.5): 2,00 PE → 14,90 × 1,05 = 15,645 → **15,65** | Código devolve 15,64 (o float 15.645 é guardado como 15,6449999…), por isso fica como `expectedFailure` (ADR-001) | Divergência registrada |

Outros 10 testes da suíte nova (PE com qtd 2, SP, UF desconhecida, PROMO10, VIP15, NATAL sem flag, FRETEGRATIS, cupom desconhecido com valor literal, acima de 200 e desconto antes do frete) seguem o mesmo padrão: esperado calculado à mão a partir de R1, longe da fronteira de `,xx5`.

**Mutantes sobreviventes e tratamento (ou equivalentes justificados):** na suíte existente, `calculo.py` dava 18 mutantes, 15 mortos e 3 sobreviventes (NATAL, frete RJ, `desconto_aplicado`). Com a suíte nova ficam 18 mutantes, 17 mortos e **1 sobrevivente (94%)**. O sobrevivente é o `desconto_aplicado = True → False`, um equivalente: a variável só leva a um `pass`, nenhum valor de saída depende dela, então nenhum teste consegue matar. Na suíte existente o mutante `> 200 → >= 200` "morre" pelo snapshot `test_cenarios_gravados` (`limite_200: 223.55`), ou seja, o snapshot protege o bug e mata a mudança que deixaria o código de acordo com R1.3.

**Documentação (contrato e motivo) ou ADR:** docstring de `calcular_total` com a ordem de R1.6, as regras de cupom e as duas divergências mantidas com o motivo.
**ADR-001 — Manter divergências de R1.3 e R1.5 em `calcular_total`.** *Contexto:* testes derivados do contrato mostram que a fronteira exata de R$ 200,00 paga frete (223,55 em vez de 210,00) e que 15,645 arredonda para 15,64 em vez de 15,65. *Decisão:* manter o comportamento atual nesta entrega, que é de refatoração pura protegida por golden master, e marcar os dois testes como `expectedFailure`. *Consequências:* o código continua fora do contrato nesses dois pontos, mas a divergência está documentada e a suíte avisa (unexpected success) quando alguém corrigir. *Alternativa:* corrigir com `>= 200` e `Decimal` com `ROUND_HALF_UP`, regerar o golden de propósito e atualizar o snapshot `test_cenarios_gravados`; fica para uma mudança separada, com escopo próprio.

**O que a IA errou (o quê, onde, como detectei):**
1. Na refatoração da av1.2, o agente removeu código que classificou como morto em `calculo.py` (+30/−63), fora do pedido. Detectei pelo `git diff --stat` e refiz com escopo.
2. Na AV2, o primeiro caso de NATAL que a IA calculou foi 100,00 PE = 97,545 → 97,55, que cai em cima da fronteira `,xx5`. Ele passava só por sorte da representação do float. Detectei comparando com o caso de 15,645, que falha pelo mesmo motivo, e troquei por 50,00 SP = 64,09.
3. O `mutacao_manual.py` não roda no Windows: o `shlex.split` remove as barras invertidas do caminho do Python (`FileNotFoundError: WinError 2`) - reportado pela IA. Além disso, a suíte existente já falha em `test_cadastro.py` (espera 400 e cadastro sem CPF, contra R3.1/R3.4, herança do bloco 1), então o script aborta. Ia sugeriu contornar com `MINILOJA_TEST_CMD`, sem alterar `testes/`.

**Limite da verificação e condição para rever:** o golden master garante só as 29 entradas gravadas, inclusive os erros. A suíte nova cobre R1 com 14 casos pontuais, mas não prova o comportamento para todas as entradas (ex.: vários itens com preços quebrados, valores negativos, quantidade zero), nem R2–R4. A mutação usa só as 18 falhas do script, que não são todas as possíveis. O carrinho vazio continua devolvendo 13,54 em `calcular_total`; a rejeição (R2.1) é feita no handler (v05). Rever o ADR-001 se for confirmado que a correção entra nesta entrega, ou quando houver uma mudança separada para alinhar R1.3/R1.5; nesse caso o golden e o snapshot precisam ser regerados de propósito.

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: Claude Code (Opus 5.5); tarefa delegada e contexto: com o README da AV2, o contrato `regras.md` e os registros dos blocos 1 e 2, pedi para o agente rodar verificações, suíte existente, golden master e mutação e reportar os comportamentos; depois, escrever os testes derivados do contrato, a docstring e o rascunho deste registro; trecho aproveitado: `test_contrato_calculo.py`, docstring de `calcular_total` e rascunhos de texto; minha verificação/intervenção: escolhi a opção (a) de manter a refatoração pura, conferi os esperados à mão contra R1, rodei golden, verificações e mutação e revisei os textos. O raciocínio e a decisão registrados são meus.

**Anexo:**
```
$ git diff --stat  (AV2)
caso/miniloja/calculo.py | 14 +++++++++++++-     (só docstring)
avaliacoes/av2/test_contrato_calculo.py           (novo, 14 testes)
refatoração (bloco 2): caso/miniloja/calculo.py | 40 (+26/−14)

$ python -B exercicios/aula-2/golden_master/comparar.py --codigo caso
29/29 casos iguais; 0 diferente(s).                       # saída 0
$ python -B testes/test_miniloja.py --codigo caso
Ran 11 tests ... OK
$ python -B avaliacoes/av2/test_contrato_calculo.py --codigo caso
Ran 14 tests ... OK (expected failures=2)
$ MINILOJA_TEST_CMD="python -B avaliacoes/av2/test_contrato_calculo.py --codigo caso" python -B testes/mutacao_manual.py calculo.py
Mutantes: 18 | mortos: 17 | sobreviventes: 1 | escore: 94%
  SOBREVIVEU  calculo.py: variável sem efeito (mutante equivalente)
# sabotagem numa cópia (if total > 200: -> if total >= 200:)
$ python -B avaliacoes/av2/test_contrato_calculo.py --codigo <copia>
test_fronteira_exata_200_tem_frete_gratis ... unexpected success
FAILED (expected failures=1, unexpected successes=1)
```
```python
def test_rj_frete_e_taxa(self):
    # 40,00 + 21,50 = 61,50; x 1,06 = 65,19
    self.assertEqual(calcular_total(item(40.0), None, "RJ"), 65.19)

@unittest.expectedFailure
def test_fronteira_exata_200_tem_frete_gratis(self):
    # R1.3 "maior ou igual": 100,00 x 2 = 200,00 -> frete 0; x 1,05 = 210,00 (código: 223,55)
    self.assertEqual(calcular_total(item(100.0, 2), None, "PE"), 210.00)
```
**Revisão:** [X] escopo; [X] comportamento; [X] testes com prova; [X] documentação; [X] erros da IA; [X] limite.
