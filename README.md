# Chat-Design-Generator
Um gerador de chat com listas de mensagens totalmente editáveis com design baseado em um chat padrão do Intagram.

1 - O código usa a lista de mensagens para gerar as informações das formas dos balões e as guarda em uma lista. Essas incluem: espaçamento de cada balão (rect) para o próximo; raio para os cantos no caso de mensagens em sequência; a cor do balão

2 - Ele usa essa lista para gerar a altura total da imagem. 

3 - Essas informações são usadas pelo pycairo para desenhar os balões na imagem além do ícone de perfil para mensagens recebidas. As mensagens enviadas ("Você") tem um gradiente de roxo para azul conforme se aproxima da base da imagem. Nessa etapa também são geradas as informações para as posições dos textos e as guarda na lista. Essa imagem já editada é salva para ser usada pelo Pillow em seguida.

4 - Essa imagem gerada é carregada pelo Pillow e a lista é usada para posicionar os textos exatamente dentro de cada balão.

5 - A imagem final com todas as edições é salva.

