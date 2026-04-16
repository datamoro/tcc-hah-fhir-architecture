# Spec-Driven Design (SDD) — Diretrizes Reta Final do TCC

A metodologia **Spec-Driven Design** estabelece que o comportamento, os limites e os artefatos de um projeto devem nascer obrigatoriamente de uma **Especificação prévia e validada** antes da produção final. 

Abaixo estão as regras estruturais e de engenharia adotadas para lapidar nossos códigos e relatorias:

## 1. Padrões Ágeis para Desenvolvimento de Código
Qualquer refatoração, inserção ou debug de código (`Python`/infra) deve respeitar a esteira estrita abaixo:
- **Design-First (O Contrato)**: Nenhuma função será escrita com lógica comercial de antemão. O design da assinatura (`def function_name(args: Type) -> ReturnType:`), os *docstrings* (explicando os parâmetros e o que ela resolve) e os limites da Pydantic class DEVEM ser definidos e aprovados antes de qualquer linha condicional.
- **PEP 8 Estrito**: O código deve aderir impreterivelmente à PEP8. Uso massivo de *Type Hints* (tipagem de dados estática `-> str`, `Optional[int]`) para a clareza máxima e integração com IDEs. Limite de 79-88 caracteres verticais para comentários.
- **Clean Code & Modularização (SOLID)**: Funções devem ter escopo unitário funcional (SRP - Princípio da Responsabilidade Única). Se uma transformação do Worker ficar excessivamente grande, seu encapsulamento será forçado em arquivos contíguos (ex: métodos de parsing isolados em `utils/`). Funções não devem possuir "efeitos colaterais" misteriosos ("side effects").
- **Garantia de Esquema FHIR**: Mapeamentos como LOINC deverão ser declarados em variáveis constantes globais no topo ou originadas de dicionários preexistentes unificando a edição.

## 2. Produção da Monografia (Spec-Driven Writing)
O Word final passa a ser tratado como um "Software de Produção". Não redigiremos parágrafos longos diretamente na nuvem de ideias; passaremos a tratar o bloco literário como um bloco unitário de código a ser coberto:
- **Passo A (Construção da Interface/Célula)**: Estabelecimento dos Requisitos Lógicos de um trecho (E.g.: O parágrafo DA Seção X DEVE citar a ferramenta Y e o Autor Z).
- **Passo B (Validação Semântica)**: A checagem sistêmica nossa do que precisa obrigatoriamente estar contido para passar no crivo da Banca.
- **Passo C (Deploy Literário)**: Apenas com o contexto "Interface" validado nós partimos para a escrita dos parágrafos de alta coesão e acoplamento temático perfeito na estrutura ABNT.

## 3. Rastreabilidade Bibliográfica de Sistemas Restritos
- **Dependência Simultânea**: O levantamento do artefato que inspirou a lógica textual tem de obedecer um carregamento estrito (*Strict Tracking*). Se escrevermos sobre *FastAPI*, a citação de seu framework original DEVE compor as anotações do sistema. Nada é jogado impunemente para o final como "débito bibliográfico técnico".
