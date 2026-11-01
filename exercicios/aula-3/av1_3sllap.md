# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.**  
Estudante: Samya de Lara Pinheiro — Data: 25/10/2026
Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: execução própria (mutação de `calculo.py` e suíte derivada do contrato, feitas na AV2) + transcrição (mutação completa de 31 falhas, `apoio/resultado-textual.md`).

| Teste suspeito | Tipo de tautologia | Sabotagem que apliquei (ou raciocínio) | Continuou verde? |
| --- | --- | --- | --- |
| `test_calculo.py::test_cupom_natal_com_flag` | Sem asserção real (só `assertIsNotNone`) | Mutante "NATAL 20% → 21%" (`0.8` → `0.79`): qualquer número passa | Sim (sobreviveu) |
| `test_calculo.py::test_cenarios_gravados` | Snapshot do próprio código (`limite_200: 223.55`, `vazio: 13.54`) | Mutante `> 200` → `>= 200`, que deixa o código **de acordo** com R1.3: o teste falha. Ele protege o bug, não o contrato | Não, falhou pelo motivo errado |
| `test_calculo.py::test_retorna_numero` | Sem asserção real (só verifica o tipo `float`) | Raciocínio: trocar o corpo de `calcular_total` por `return 0.0` mantém o teste verde, porque nenhum valor é conferido | Sim (por raciocínio, não executado) |

| Mutante sobrevivente | Por que sobreviveu | Teste que o mataria (ou "equivalente", com justificativa) |
| --- | --- | --- |
| `calculo.py`: NATAL 20% → 21% | O único teste de NATAL só faz `assertIsNotNone` | `test_natal_com_campanha_ativa`: 50,00 SP NATAL com flag → 40,00 + 19,90 = 59,90 × 1,07 = 64,093 → **64,09**. Com 21%: 39,50 + 19,90 = 59,40 × 1,07 = 63,558 → 63,56 → falha |
| `calculo.py`: frete RJ (21.5 → 22.5) | O único teste de RJ usa `FRETEGRATIS`, então o frete de RJ nunca é somado | `test_rj_frete_e_taxa`: 40,00 RJ → 40,00 + 21,50 = 61,50 × 1,06 = **65,19**. Com 22,50: 62,50 × 1,06 = 66,25 → falha |

Equivalente identificado: `calculo.py`: `desconto_aplicado = True → False`. A variável só leva a um `pass` e nenhuma saída depende dela, então nenhum teste consegue matá-lo.

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão) | Observado no código | Decisão |
| --- | --- | --- | --- |
| Fronteira R1.3: 100,00 × 2, PE, sem cupom | 200,00 ≥ 200 → frete 0; 200,00 × 1,05 = **210,00** | 223,55 (cobra frete: `> 200`) | Código errado (R1.3 diz "maior ou igual"). Mantido e registrado no ADR-001 |
| Arredondamento R1.5: 2,00, PE, sem cupom | 2,00 + 12,90 = 14,90 × 1,05 = 15,645 → **15,65** (meio para cima) | 15,64 (`round` sobre float: 15,6449999…) | Código errado (R1.5 dá o próprio exemplo 15,645 → 15,65). Mantido e registrado no ADR-001 |
| Ordem R1.6: 215,00, PROMO10, PE | 215,00 × 0,90 = 193,50 (< 200, paga frete); + 12,90 = 206,40 × 1,05 = **216,72** | 216,72 | Código de acordo com o contrato |

**ADR curto (ADR-001):** contexto: casos derivados do contrato mostram que a fronteira exata de R$ 200,00 paga frete (223,55 em vez de 210,00) e que 15,645 vira 15,64 em vez de 15,65; decisão: manter o comportamento atual, porque a entrega era uma refatoração pura protegida por golden master, e marcar os dois testes como `expectedFailure`; consequências: o código segue fora do contrato nesses dois pontos, mas a divergência fica documentada e a suíte avisa com `unexpected success` quando alguém corrigir; alternativa descartada: corrigir agora com `>= 200` e `Decimal` com `ROUND_HALF_UP`, o que exigiria regerar o golden e o snapshot `test_cenarios_gravados` dentro de uma entrega que não tinha esse escopo.

**Trecho essencial de evidência:**
```
$ python -B testes/test_miniloja.py --codigo caso --existentes     # suíte existente: 26 OK
$ python -B testes/mutacao_manual.py calculo.py                     # suíte existente
Mutantes: 18 | mortos: 15 | sobreviventes: 3   (NATAL, frete RJ, variável sem efeito)
$ MINILOJA_TEST_CMD="python -B avaliacoes/av2/test_contrato_calculo.py --codigo caso" python -B testes/mutacao_manual.py calculo.py
Mutantes: 18 | mortos: 17 | sobreviventes: 1 | escore: 94%   (só o equivalente)
# sabotagem numa cópia: if total > 200: -> if total >= 200:
test_fronteira_exata_200_tem_frete_gratis ... unexpected success
```

**Limite do que a suíte garante e condição para rever a decisão:** mesmo com os novos testes, a suíte cobre R1 só em casos pontuais; não cobre vários itens com preços quebrados, quantidade zero ou valores negativos, e a mutação usa só as falhas do script, não todas as possíveis. Os outros sobreviventes da transcrição (VIP15 em `descontos.py`, limite exato do estoque, e-mail obrigatório, total formatado, relatório) não foram tratados aqui. A cobertura de linhas de ~90% com escore de 74% mostra que linha executada não é linha verificada. Rever o ADR-001 quando houver uma mudança separada, com escopo próprio, para alinhar R1.3/R1.5; nesse caso o golden e o snapshot precisam ser regerados de propósito.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code (Opus 5.5); tarefa delegada e contexto: com o README da AV1.3, o contrato e meus registros da AV1.2 e da AV2, pedi um rascunho deste registro reaproveitando os testes, a mutação e o ADR-001 da AV2; trecho aproveitado: rascunho das tabelas e textos; minha verificação/intervenção: ___. O raciocínio e a decisão registrados são meus.

**Revisão:** [ ] três testes; [ ] dois mutantes; [ ] três casos do contrato; [ ] ADR; [ ] até uma página.
