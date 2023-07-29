# Comandos

Para empezar a trabajar, se debe activar el env de python, ingresar a la carpeta env, 
correr el siguiente comando:
- sudo bin/activate

Para correr la api y tener hot reload activado:
- uvicorn main:app --reload

# Preguntas

Las ordenes de tipo market se ejecutan instantaneamente, en cambio las de tipo limit
se ejecutan cuando se alcanza un determinado precio, dado por el parametro price, el 
cual calculamos previamente utilzando un threshold.

- Cual es el punto de crear ordenes de compra escalonadas?

Que mientras mas baje el precio y luego se recupere mas profit vamos a sacar,
si compramos todas las ordenes en el instante con el precio del mercado estamos perdiendo
un profit potencial.

Como crear las ordenes verdaderas?

- buyOrder = commandService.create_buy_order_limit(quantity, buyLimitPrice)
- sellOrder = commandService.create_sell_order_limit(quantity, sellLimitPrice)
