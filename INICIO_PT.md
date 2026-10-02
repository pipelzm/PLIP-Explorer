# PLIP Explorer — Início rápido

## Instalar 0.1.0a4

Instale dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl com toolshed install no ChimeraX. Encerre completamente o ChimeraX e abra-o novamente. Abra Tools → Structure Analysis → PLIP Explorer ou execute: ui tool show "PLIP Explorer".

## Idioma

Escolha Português no seletor Idioma. A preferência é salva. A troca de idioma preserva o relatório, o sítio selecionado, os filtros, as cores e a câmera. Os identificadores científicos e campos exportados permanecem inalterados. Os diálogos nativos e mensagens externas do PLIP/Open Babel/ChimeraX podem usar seu próprio idioma.

## Testar sem instalar o PLIP

Selecione Exemplo → 1VSN → Carregar exemplo. O relatório pré-calculado incluído contém 13 interações em NFT:A:283: 4 contatos hidrofóbicos, 7 ligações de hidrogênio e 2 ligações de halogênio. Desmarque Ligação de hidrogênio: devem permanecer 6 linhas visíveis. Marque novamente e clique em uma linha para centralizar e rotular seus resíduos. Ative Distâncias 3D e clique em Aplicar estilo para testar os rótulos de distância.

## Segundo exemplo

Carregue 1EVE e selecione E20:A:2001. São esperadas 10 interações: 5 contatos hidrofóbicos, 1 ligação de hidrogênio, 1 ponte de água, 2 empilhamentos π–π e 1 interação cátion–π. As pontes de água usam dois segmentos; as interações aromáticas usam centros dos grupos. Outros sítios de ligantes também aparecem neste relatório. Cada exemplo abre uma estrutura separada; oculte o modelo anterior se houver sobreposição.

## Verificar exportação e sessões

Exportar CSV deve produzir 13 linhas de dados mais o cabeçalho para o sítio do 1VSN. O CSV inclui as categorias ocultas. Salve uma sessão de teste .cxs, abra-a novamente e confira a estrutura, a tabela e os filtros. A restauração de sessões e a representação gráfica ainda precisam ser testadas no ChimeraX.

## Analisar seu complexo

Configure Motor PLIP com o executável Python de um ambiente separado que contenha PLIP e Open Babel. Obtenha o caminho com: python -c "import sys; print(sys.executable)". Consulte README_ES.md para configurar o ambiente. Abra um único modelo compatível com PDB contendo proteína e ligante, clique em Atualizar, selecione o complexo e clique em Analisar complexo. Uma nova pasta deve conter report.xml, plip.log e run.json, com status complete e a versão do PLIP em run.json.

## O que o teste comprova

Os exemplos verificam importação e visualização; carregá-los não executa o PLIP. As contagens são exatas para os XML incluídos. Novas análises podem variar com protonação, preparação ou versão do motor. O painel utiliza dados do PLIP e gráficos nativos do ChimeraX; não importa arquivos PSE ou PML do PyMOL. O usuário confirmou a abertura do painel 0.1.0a2 no ChimeraX 1.12/macOS M1. A nova interface e os gráficos da versão 0.1.0a4 ainda precisam ser testados nesse ambiente.
