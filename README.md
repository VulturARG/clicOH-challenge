# Prueba de conocimiento con Django Rest Framework

## Prueba lógica
Crear una API REST utilizando DJANGO REST FRAMEWORK, que brinde la siguiente funcionalidad básica y acotada de un
Ecommerce.

Ver los [requerimientos del desafío](documentacion/instrucciones_desafio.md).

## Repositorio
El código de este desafío se encuentra fue en el siguiente [repositorio de GitHub](https://github.com/VulturARG/clicOH-challenge/tree/development) en la rama `development`. 

## Implementación
Ver las [instrucciones de implementación](documentacion/instrucciones_implementacion.md).

## Servidor de producción
```
luisbriones.pythonanywhere.com
```
## Criterio de diseño
Se tomó como criterio de diseño separar la lógica de negocio del framework implementado. En este caso, Django Rest Framework.

Para ello se usó el concepto de arquitectura hexagonal o de puertos y adaptadores.

La misma consiste en tener toda la lógica de negocios en un dominio que no dependa de nada externo al mismo. 
La lógica de negocios se encuentra en los diferentes servicios dentro del dominio. 
La comunicación con el exterior se hace mediante puertos, que son clases abstractas. Comúnmente se llaman repositorios.
Dichos puertos se implementan en adaptadores dentro del framework, logrando así una inversión de la dependencia.

Esto permite, entre otras ventajas, testear la lógica de negocios sin tener que depender de una implementación externa.
Se pueden crear Mocks de las distintas clases sin inconvenientes.

### Esquema de la arquitectura hexagonal.

![](imgs/arquitectura_hexagonal.png)