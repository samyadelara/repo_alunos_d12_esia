# Registro individual — AV1.2

**Limite: uma página, incluindo evidências essenciais.**  
Estudante: Samya de Lara Pinheiro — Data: 20/10/2026  

Origem: `caso/miniloja/calculo.py` fictício; modalidade: execução própria.

**Golden master:** 29 entradas; gerado por script Python (gerar.py) a partir do código original com assistência da IA; comparação exata por script Python (comparar.py) que compara não apenas valores mas tipagem para garantir igualdade exata com assistência da IA. Resultado: Rodada 1 = 29/29 iguais; Rodada 2 = 29/29 iguais  

| Medida | Rodada 1 (sem escopo) | Rodada 2 (com escopo) |
| --- | --- | --- |
| Linhas adicionadas/removidas | +30/-63 | +26/−14 |
| Arquivos alterados (e quais estavam fora do esperado) | calculo.py (criação de funções e remoção de código que classificou como morto) | calculo.py |
| Mudou comportamento? (golden master) | Não (manteve erros que o código original tem, que não estão de acordo com o contrato) | Não (manteve erros que o código original tem, que não estão de acordo com o contrato) |
| Tempo de revisão | 5min | 5min |
| Idas e vindas | one shot | o plano foi revisado antes de executar, depois uma execução |

**Escopo da rodada 2:** objetivo refatorar a função calculo_total, separando descontro, frete e taxa em funçõe específicas; pode tocar calculo.py; não pode tocar assinatura pública nem outros arquivos, não tocar em testes e golden master; invariantes golden master exato; pronto quando passar em todas as verificações definidas e verde para golden master; pare e pergunte se achar algo que pareça bug, ela reporta, não corrige.  

**Plano do agente:**  
0. Rodar as verificações antes de mexer para gravar a linha de base
1. Extrair _aplicar_desconto(total, cupom), mantendo os mesmos if/elif e multiplicadores.  
2. Extrair _calcular_frete(total, cupom, uf), com o mesmo > 200 e os mesmos valores por UF.  
3. Extrair _aplicar_taxa(total, uf), com os mesmos valores por UF.  
4. Manter calcular_total com a mesma assinatura, chamando as três em ordem (desconto → frete → taxa).  
5. Rodar o golden master e as verificações, que devem bater com a linha de base, e conferir com git diff --stat que só calculo.py mudou.  
6. Reportar, sem corrigir, qualquer divergência com o contrato. Se aparecer uma suspeita nova, parar e perguntar.  

**O que eu cortei ou corrigi antes de executar:** Reforcei para não mexer em testes, nem mudar comportamento fora do escopo, como o problema que o agente detectou sobre o arredondamento.  

**Algo que parecia bug e eu apenas reportei:**  
1. O frete grátis usa total > 200, mas o contrato R1.3 diz "maior ou igual a R$ 200,00".
2. round(total, 2) arredonda o número decimal do Python e não segue o "meio para cima" pedido em R1.5.
3. FRETE_POR_UF e TAXA_POR_UF estão declarados mas não são usados.
4. desconto_aplicado não tem efeito: só leva a um pass.
5. Carrinho vazio devolve um valor em vez de ser rejeitado (R2.1). Pode ser que isso seja validado em pedidos.py, que está fora do escopo.  
**`AGENTS.md` mínimo:** 
  >  # AGENTS.md — MiniLoja (refatoração de calculo.py)
    - Verificar: `python -B testes/test_miniloja.py --codigo caso` (linha de base: 8/11; v08–v10 de CPF falham e estão fora do escopo) e `--existentes` (26/26).
    - Golden master: `python -B exercicios/aula-2/golden_master/comparar.py --codigo caso` precisa dar 29/29 e saída 0.
    - Pode tocar só em `caso/miniloja/calculo.py`, sem mudar a assinatura de `calcular_total(itens, cupom=None, uf="PE")`.
    - Não tocar em `testes/`, `caso/regras.md` nem no golden master; nunca regenerar `golden.json` para "passar".
    - O contrato `caso/regras.md` vale mais que o código, mas o golden preserva o comportamento atual, inclusive os erros.
    - Achou algo que parece bug (ex.: `> 200` contra o "≥ 200" de R1.3)? Pare e reporte; não corrija numa refatoração.
    - Convenção não óbvia: `testes/mutacao_manual.py` procura trechos literais de `calculo.py`; mantenha os `if/elif` e a indentação.


**Trecho essencial de evidência:**
```
$ python -B exercicios/aula-2/golden_master/comparar.py --codigo caso
29/29 casos iguais; 0 diferente(s).        # saída 0
$ python -B testes/test_miniloja.py --codigo caso
Ran 11 tests ... FAILED (failures=3)       # v08–v10 (CPF), iguais à linha de base, fora do escopo
$ python -B testes/test_miniloja.py --codigo caso --existentes
Ran 26 tests ... OK
$ git diff --stat -- caso
caso/miniloja/calculo.py | 40 ++++++++++++++++++++++++--------------   (+26/−14)
```

**Limite e condição para rever o escopo:** o golden master só garante que o comportamento atual se manteve, inclusive os erros (`> 200` contra R1.3, `round` contra R1.5), e só nas 29 entradas gravadas. Ele não prova que o código segue o contrato nem cobre entradas fora dessas classes. Para corrigir os erros reportados, rever o comportamento do codigo original e contrstar com o contrato.

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: ___; tarefa delegada e contexto: ___; trecho aproveitado: ___; minha verificação/intervenção: ___. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [X] golden master; [X] duas rodadas com números; [X] seis campos; [X] AGENTS.md; [X] até uma página.
