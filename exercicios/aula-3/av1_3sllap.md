# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.**  
Estudante: Samya de Lara Pinheiro — Data: 01/11/2026  

Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: execução própria. Sabotagens na cópia `trabalho/`; suíte existente e mutação em `caso/`, com `calculo.py` refatorado na AV1.2 e `cadastro.py` no estado original (sem as correções do bloco 1, para a suíte existente ficar verde).

| Teste suspeito | Tipo de tautologia | Sabotagem que apliquei (ou raciocínio) | Continuou verde? |
| --- | --- | --- | --- |
| `test_calculo.py::test_cupom_natal_com_flag` | Sem asserção real (só `assertIsNotNone`) | Mutante "NATAL 20% → 50%" (`0.8` → `0.5` na cópia: `trabalho/miniloja/calculo.py`) - qualquer número passa | Sim (sobreviveu) |
| `test_pedidos.py::test_fluxo_chama_colaboradores` | Afirma o mock: estoque, gateway e repositório são `MagicMock` e o teste só confere `.called` | Na cópia `trabalho/miniloja/pedidos.py`: `self.gateway.cobrar(total, token)` → `self.gateway.cobrar(0, token)`. O pedido é "cobrado" por R$ 0,00 e o teste não percebe, porque só confere `.called`, sem argumentos nem retorno | Sim (`test_fluxo_chama_colaboradores ... ok`) |
| `test_calculo.py::test_retorna_numero` | Sem asserção real (só verifica o tipo `float`) | Na cópia `trabalho/miniloja/calculo.py`: `return 0.0` como primeira linha de `calcular_total`. O cálculo inteiro quebra e a suíte acusa 7 falhas nos testes com valor literal, mas este continua verde, porque só confere o tipo. Deveria conferir o valor pelo contrato, ex.: 10,00 SP → (10,00 + 19,90) × 1,07 = 31,993 → 31,99 | Sim (`test_retorna_numero ... ok`; suíte com 7 falhas) |

| Mutante sobrevivente | Por que sobreviveu | Teste que o mataria (ou "equivalente", com justificativa) |
| --- | --- | --- |
| `calculo.py`: NATAL 20% → 21% | O único teste de NATAL só faz `assertIsNotNone` | Proposto: `test_natal_com_campanha_ativa` (`assertEqual` com entrada fixa e esperado literal do contrato): 50,00 SP NATAL com flag → 40,00 + 19,90 = 59,90 × 1,07 = 64,093 → **64,09**. Com 21%: 39,50 + 19,90 = 59,40 × 1,07 = 63,558 → 63,56 → falha |
| `calculo.py`: frete RJ (21.5 → 22.5) | O único teste de RJ usa `FRETEGRATIS`, então o frete de RJ nunca é somado | Proposto: `test_rj_frete_e_taxa` (`assertEqual` com entrada fixa, RJ **sem** cupom, e esperado literal): 40,00 RJ → 40,00 + 21,50 = 61,50 × 1,06 = **65,19**. Com 22,50: 62,50 × 1,06 = 66,25 → falha |

Equivalente identificado: `calculo.py`: `desconto_aplicado = True → False`. A variável só leva a um `pass` (já reportado como código sem efeito na AV1.2) e nenhuma saída depende dela, então nenhum teste consegue matá-lo. Excluído, o escore real de `calculo.py` é 15/17.

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão) | Observado no código | Decisão |
| --- | --- | --- | --- |
| Fronteira R1.3: 100,00 × 2 (preço x qtd), PE, sem cupom | 200,00 ≥ 200 → frete 0; 200,00 × 1,05 = esperado **210,00** | 223,55 (cobra frete: `> 200`) | Código errado (R1.3 diz "maior ou igual"). Mantido e registrado no ADR-001 |
| Arredondamento R1.5: 2,00, PE, sem cupom | 2,00 + 12,90 = 14,90 × 1,05 = 15,645 → esperado **15,65** (meio para cima) | 15,64 (`round` sobre float: 15,6449999…) | Código errado (R1.5 dá o próprio exemplo 15,645 → 15,65). Mantido e registrado no ADR-001 |
| Ordem R1.6: 215,00, PROMO10, PE | 215,00 × 0,90 = 193,50 (< 200, paga frete); + 12,90 = 206,40 × 1,05 = esperado **216,72**. Na ordem inversa (taxa, frete, desconto): 215,00 × 1,05 = 225,75 (≥ 200, frete grátis); × 0,90 = 203,175 → 203,18, isto é, R$ 13,54 a menos, porque o desconto deixa de derrubar o total abaixo de 200 antes do frete | 216,72 | Código de acordo com o contrato |

### **ADR curto (ADR-001):** 
#### Contexto: casos derivados do contrato mostram que a fronteira exata de R$ 200,00 paga frete (223,55 em vez de 210,00, R1.3) e que 15,645 vira 15,64 em vez de 15,65 (R1.5). A suíte existente não percebe: o snapshot `test_cenarios_gravados` grava `limite_200: 223.55` e falha justamente se alguém corrigir o limite;
#### Decisão: o contrato vale, então o código está errado nos dois pontos. A correção fica fora desta atividade, que é de testes, e o código acabou de ser refatorado sob golden master (AV1.2), que preserva esses erros. Os testes com o valor do contrato (210,00 e 15,65) entram como `expectedFailure`, sem ajustar o esperado ao código;
#### Consequências: o código segue fora do contrato, mas a divergência fica documentada e visível na suíte; quando alguém corrigir, esses testes viram `unexpected success`, e o snapshot e o golden falham, sinalizando que precisam ser regerados de propósito;
#### Alternativa descartada: corrigir agora com `>= 200` e `Decimal` com `ROUND_HALF_UP`, o que muda o comportamento e exige regerar o golden da AV1.2 e o snapshot `test_cenarios_gravados`, sem escopo declarado para isso.

**Trecho essencial de evidência:**
```
$ python -B testes/test_miniloja.py --codigo caso --existentes     # linha de base
Ran 26 tests ... OK
$ $env:MINILOJA_TEST_CMD="python -B testes/test_miniloja.py --existentes --codigo caso -x"
$ python -B testes/mutacao_manual.py
Mutantes: 31 | mortos: 23 | sobreviventes: 8 | escore: 74%
$ python -B testes/mutacao_manual.py calculo.py
Mutantes: 18 | mortos: 15 | sobreviventes: 3 | escore: 83%   (NATAL, frete RJ, variável sem efeito)
# observado no código para os três casos do contrato (200,00 PE; 2,00 PE; 215,00 PROMO10 PE)
$ python -B -c "import sys; sys.path.insert(0,'caso'); from miniloja.calculo import calcular_total as t; print(t([{'preco':100.0,'qtd':2}],None,'PE'), t([{'preco':2.0,'qtd':1}],None,'PE'), t([{'preco':215.0,'qtd':1}],'PROMO10','PE'))"
223.55 15.64 216.72
```

**Limite do que a suíte garante e condição para rever a decisão:** os testes propostos foram calculados à mão e não executados; não medi a mutação com eles. Mesmo que sejam incluídos, a suíte cobre R1 só em casos pontuais: não cobre vários itens com preços quebrados, quantidade zero ou valores negativos, e a mutação usa só as 31 falhas do script, não todas as possíveis. Os outros sobreviventes da mutação completa (VIP15 em `descontos.py`, limite exato do estoque, e-mail obrigatório, total formatado, relatório) não foram tratados aqui, e nenhum teste exercita R2.2 (falha de estoque no meio do pedido sem deixar reserva). Segundo o material do curso, a cobertura de linhas da suíte é de ~90% (não medi); com escore de 74%, linha executada não é linha verificada. Rever o ADR-001 quando houver uma mudança separada, com escopo próprio, para alinhar R1.3/R1.5; nesse caso o golden e o snapshot precisam ser regerados de propósito.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code (Opus 5.5); tarefa delegada e contexto: com o README da AV1.3, o contrato e meu registro da AV1.2, pedi explicação do exercício, rascunho de partes do registro e apoio na execução da mutação; trecho aproveitado: rascunho das tabelas e textos; minha verificação/intervenção: execução das três sabotagens na cópia `trabalho/`, execução da mutação, conferência dos cálculos à mão contra R1, escolha dos testes e casos, revisão dos textos. O raciocínio e a decisão registrados são meus.

**Revisão:** [X] três testes; [X] dois mutantes; [X] três casos do contrato; [X] ADR; [X] até uma página.
