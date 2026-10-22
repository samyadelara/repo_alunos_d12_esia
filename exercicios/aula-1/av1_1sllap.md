# Registro individual — AV1.1

**Limite: uma página, incluindo evidências essenciais.**  
Estudante: Samya de Lara Pinheiro — Data: 20/10/2026  

Origem: tarefas T1–T3 fictícias do enunciado; modalidade: execução própria.

| Tarefa | Modo | Tempo até 1ª versão | Tempo até pronto e verificado | Idas e vindas | % corrigido à mão | O que a IA errou | Como verifiquei |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A: modo planejamento | 4min | 10min | Validação do plano, implementação em modo manual | 60% de cadastro.py (14 linhas adicionadas)
 | CPF ausente ainda é aceito mesmo a obrigatoriedade sendo requisito registrado no contrato| Rodei os testes novamente e solicitei para a IA um caso de CPF ausente e eu rodei. |
| T1 | B: modo agente | 2min | 5min | Solicitei para o agente fazer a validação, como foco em fazer passar os dois testes em questão. | 0% | CPF ausente ainda é aceito mesmo a obrigatoriedade sendo requisito registrado no contrato | Rodei os testes novamente e solicitei para a IA um caso de CPF ausente e eu rodei. |
| T2 | modo agente | 2min | 5min | Solicitei para o agente fazer a validação, como foco em fazer passar o v10. Ele concluiu a necessidade de para passar v10 , v08 e v09 precisavam passar. | 1% (ajuste de doc string). | A regex de e-mail aceita casos estranhos, como a@.b.c, porque [^@\s]+ também casa pontos. | Inspeção da expressão regex e consulta à IA por chat. |

**Trecho essencial de evidência (comando e saída que sustentam "verificado"):**

    python -B testes/test_miniloja.py --codigo caso`  
    T1 - FAIL: test_v10_payload_invalido_lista_todos_os_erros (__main__.TestMiniLoja.test_v10_payload_invalido_lista_todos_os_erros)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "C:\Users\sllap\OneDrive\Documents\Study_Sllap\CESARschool\M2\repo_alunos_d12_esia\testes\test_miniloja.py", line 81, in test_v10_payload_invalido_lista_todos_os_erros
        self.assertEqual(status, 422)
        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
    AssertionError: 400 != 422
    ----------------------------------------------------------------------
    Ran 11 tests in 0.007s
    FAILED (failures=1)

    T2 - ----------------------------------------------------------------------
    Ran 11 tests in 0.008s

    OK

**T3 (hipotética): raio de impacto - Sistema em Produção com risco de alterações indevidas tornar o serviço indisponível; oráculo disponível - O enunciado reporta logs e métricas, logo não temos um golden master registrado, mas podemos fazer uma avaliação do que pode ser considerado "normal" para o sistema a a partir disso quantificar a lentidão, mepear em que operações e funcionalidades estão sendo geradas etc.; permissões que concederia - Somente Leitura devido ao alto risco e raio de impacto; modo e por quê - Modo Planejamento, para conversar e ter o apoio da IA na investigação e diagnóstico. Assim mitigo o risco de alteração do código não validada e podemos implementar os ajustes manualmente com maior controle e plano de rollback.**

**Alternativa para T3:**  agente autônomo, com permissão para executar comandos e reiniciar o serviço. **Comparação com minha escolha (restrição e consequência):** O raio de impacto é alto, pois estamos em produção. Logo essa alternativa seria muito arriscada. Trabalhar apenas em modo planejamento e consulta acaba sendo mais seguro, mesmo que mais lento. **Limite da comparação e condição para rever a escolha:** Se tivesse disponível oráculo e testes de desempenho, além de ambiente de dsv e/ou hmg para testar as alterações antes.

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: Claude Code (Opus 5.5); tarefa delegada e contexto: uso o README.md de documentação de miniloja para solicitar explicação sobre o exercício atraves de agente em modo planejamento, com apoio na construção de rascunhos de respostas, que revisei, ajustei e registrei; trecho aproveitado: detalhamento dos enunciados e rascunhos de respostas; minha verificação/intervenção: rodar testes, inspecionar código, revisão de textos. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [X] dois modos em T1; [X] evidência localizada; [X] T3 decidida; [X] alternativa e limite; [X] até uma página.
