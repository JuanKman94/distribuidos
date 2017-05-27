# Proyecto de sistemas distribuidos

El objetivo del proyecto es crear un sistema _middleware_ que sea capaz de
funcionar apropiadamente a través de distintas maquinas.

El sistema debe ser autosuficiente y autocorregible de errores no críticos,
lo que incluye, pero no se limita, a:
1. Si uno de los nodos se desconecta, debe seguir funcionando
2. Si el nodo maestro se cae, uno de los nodos servidores debe asumir el rol
3. Si hay dos nodos maestros a la vez, deben resolver el conflicto
