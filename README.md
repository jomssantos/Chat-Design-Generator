# Chat-Design-Generator
Um gerador de chat com listas de mensagens totalmente editáveis com design baseado em um chat padrão do Intagram.

1 - O código usa a lista de mensagens para gerar as informações das formas dos balões e as guarda em uma lista. Essas incluem: espaçamento de cada balão (rect) para o próximo; raio para os cantos no caso de mensagens em sequência; a cor do balão

2 - Ele usa essa lista para gerar a altura total da imagem. 

3 - Essas informações são usadas pelo pycairo para desenhar os balões na imagem além do ícone de perfil para mensagens recebidas. As mensagens enviadas ("Você") tem um gradiente de roxo para azul conforme se aproxima da base da imagem. Nessa etapa também são geradas as informações para as posições dos textos e depois são guardadas em uma lista. Essa imagem já editada é salva para ser usada pelo Pillow em seguida.

<div align="center">
<img src="https://github.com/user-attachments/assets/24064cce-d397-4f95-b866-fd2a06b1b6d5" width="400px" />
</div>

4 - Essa imagem gerada é carregada pelo Pillow para que ele coloque os textos das mensagens usando a lista para posicioná-los exatamente dentro de cada balão.

<div align="center">
<img src="https://github.com/user-attachments/assets/719a575c-95b5-4686-a6e2-3895083691e5" width="400px" />
</div>

5 - A imagem final com todas as edições é salva.
