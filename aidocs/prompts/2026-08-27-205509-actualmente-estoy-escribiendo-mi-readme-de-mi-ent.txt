 ▐▛███▛█   Claude Code v2.1.246
▝▜██████▀  Sonnet 5 · Claude Pro
  ▝▝ ▝▝    ~/Cursos UC/2026-2/ARQUISIS-IIC2173/arquisis_e0_unofficial


❯ Actualmente estoy escribiendo mi README de mi entrega de proyecto que me      
  piden a continuación: Una copia del archivo README.md de su repo, con los     
  niveles de logro que ustedes alcanzaron y lo que crean necesario para la      
  revisión. Recuerden que es una sugerencia de revisión, y si determinamos que  
  lograron algo extra será incluido (y viceversa).                              
  Además no olviden indicar el link de su API en el Readme para que podamos     
  acceder a esta junto con la ip de su instancia. Necesito que sigas            
  completando la sección "Para revisión E0" del README de forma resumida pero   
  poniendo todos los puntos importantes (no es necesario explicar ni detallar   
  implementaciones). Considera que complete todos los puntos que se pedían.     
  Enunciado: "C:\Users\david\Downloads\Enunciado E0_v1.pdf"                     

  Listed 2 directories (ctrl+o to expand)

● Encontré el PDF del enunciado. Ahora lo leo junto con el README actual y
  exploro la estructura del repo para entender qué se implementó.

  Read 2 files (ctrl+o to expand)

● El enunciado incluye anotaciones a mano (checkmarks) que parecen ser tu propia
  autoevaluación previa. Voy a verificar cada punto contra el código real del
  repo antes de escribir la sección, para no copiar checkmarks sin confirmar.

  Ran 2 shell commands (ctrl+o to expand)

● Bien, la venv del connector no está trackeada por git (buena señal). Ahora
  reviso el código relevante: docker-compose, Dockerfiles, healthchecks, nginx
  conf, connector (reconexión), y los endpoints de master.

  Read 11 files, ran 7 shell commands (ctrl+o to expand)

● User answered Claude's questions:
  ⎿  · ¿Qué usuario SSH y tipo de instancia EC2 debo poner en el README para el 
     acceso al servidor? → ubuntu / t3.micro

● Todo confirmado contra el código y verificado en vivo (health, docs, SSL,
  history con +159k registros). Ahora actualizo la sección del README.

● Update(README.md)
  ⎿  Added 44 lines, removed 8 lines
       1  # arquisis_e0_unofficial
       2  
       3 -## Para revisión E0:                                           
       3 +## Para revisión E0                                            
       4  
       5 -### URL: api.empanad4z.me                                      
       5 +### Consideraciones generales                                  
       6  
       7 -### Requisitos funcionales:                                    
       8 -- Todos los requisitos funcionales están implementados y funcio
         -nando en cloud. Documentación detallada de API de ```master```:
         - api.empanad4z.me/docs. Por favor ver para probar los filtros d
         -e la manera correcta.                                          
       7 +- **API / dominio:** https://api.empanad4z.me (documentación in
         +teractiva en `/docs`)                                          
       8 +- **IP instancia EC2:** `35.168.184.246` (t3.micro, free tier) 
       9 +- **Acceso SSH:** `ssh -i <archivo>.pem ubuntu@35.168.184.246` 
         +— el `.pem` se entrega por el buzón de Canvas, no está en este 
         +repo.                                                          
      10 +- Prompts de IA usados durante el desarrollo documentados en `a
         +idocs/prompts/`.                                               
      11  
      10 -### Requisitos no funcionales:                                 
      11 -- Todos los requisitos no funcionales están implementados.     
      12 -- Servicio ```connector``` envía datos a través de endpoint POS
         -T de ```master``` dónde esté último mapea y expone los siguient
         -es puertos: ```8080-8081:8000```.                              
      13 -- Db postgresql containerizada.                                
      12 +### Parte mínima                                               
      13  
      14 +**Requisitos funcionales (10p)**                               
      15  
      16 +- RF1 (3p, Esencial) ✅ — `GET /history`: historial completo co
         +n todos los campos recibidos.                                  
      17 +- RF2 (1p) ✅ — `GET /history/{id}`: detalle de un registro, `i
         +d` autogenerado por `master`.                                  
      18 +- RF3 (2p, Esencial) ✅ — Paginación por defecto de 25 registro
         +s vía `page`/`limit`.                                          
      19 +- RF4 (4p, Esencial) ✅ — Filtros por prácticamente todos los c
         +ampos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exa
         +cto o rango, `validUntil` exacto o rango) más orden (`sortBy`, 
         +`order`).                                                      
      20  
      21 +**Requisitos no funcionales (20p)**                            
      22 +                                                               
      23 +- RNF1 (5p, Esencial) ✅ — `connector` corre en container apart
         +e, se conecta al broker por AMQP+SSL y reenvía cada evento a `m
         +aster` por HTTP POST. Reintenta solo (sin intervención manual) 
         +si se pierde la conexión al broker; `master` sigue respondiendo
         + consultas sobre lo ya guardado aunque el broker o `connector` 
         +estén caídos.                                                  
      24 +- RNF2 (4p, Esencial) ✅ — `master` en su propio container, rec
         +ibe eventos de `connector` por POST, misma red docker.         
      25 +- RNF3 (3p) ✅ — nginx como reverse proxy instalado directament
         +e en el host EC2 (no en Docker), config en `nginx/api.empanad4z
         +.me.conf`.                                                     
      26 +- RNF4 (2p) ✅ — dominio `api.empanad4z.me` bajo TLD público `.
         +me`.                                                           
      27 +- RNF5 (2p, Esencial) ✅ — corriendo en EC2 free tier (t3.micro
         +).                                                             
      28 +- RNF6 (2p) ✅ — Postgres containerizado, no expuesto a interne
         +t (solo `127.0.0.1`).                                          
      29 +- RNF7 (2p, Esencial) ✅ — los 3 containers (`postgres`, `maste
         +r`, `connector`) declaran `HEALTHCHECK` en `docker-compose.yaml
         +` (`pg_isready`, chequeo HTTP a `/health`, y file-check respect
         +ivamente).                                                     
      30 +                                                               
      31 +**Docker-Compose (15p)**                                       
      32 +                                                               
      33 +- RNF1 (5p) ✅ — `master` se levanta desde docker compose (con 
         +2 réplicas).                                                   
      34 +- RNF2 (5p) ✅ — `postgres` integrado en el mismo `docker-compo
         +se.yaml`.                                                      
      35 +- RNF3 (5p) ✅ — `connector` se levanta desde docker compose y 
         +queda conectado a `master` por la red interna.                 
      36 +                                                               
      37 +### Parte variable                                             
      38 +                                                               
      39 +Se optó por ambas opciones.                                    
      40 +                                                               
      41 +**HTTPS (25%, 15p)**                                           
      42 +                                                               
      43 +- RNF1 (7p) ✅ — dominio asegurado con SSL de Let's Encrypt.   
      44 +- RNF2 (3p) ✅ — redirección automática HTTP → HTTPS.          
      45 +- RNF3 (5p) ✅ — renovación automática del certificado vía el t
         +imer de systemd que instala certbot por defecto (corre 2 veces 
         +al día).                                                       
      46 +                                                               
      47 +**Balanceo de carga con Nginx (25%, 15p)**                     
      48 +                                                               
      49 +- RF1 (5p) ✅ — `master` replicado en 2 instancias container en
         + paralelo (`deploy.replicas: 2`).                              
      50 +- RF2 (10p) ✅ — cada réplica alcanzable individualmente (`8080
         +-8081:8000`) y balanceadas por nginx vía `upstream` en `nginx/a
         +pi.empanad4z.me.conf`.                                         
      51 +                                                               
      52 +                                                               
      53  Servicios (`docker-compose.yaml`):
      54  
      55  - **postgres** — base de datos Postgres, corriendo como contain
          er propio.

● He completado la sección "Para revisión E0" del README, verificando cada punto
  contra el código real y probando la API en vivo (no solo copiando tus
  checkmarks del enunciado).

  Lo que verifiqué en el proceso:
  - Leí el enunciado (Enunciado E0_v1.pdf) con tus checkmarks a mano como guía
    inicial.
  - Revisé master/app/api/routes/events.py, filters.py, docker-compose.yaml,
    connector/main.py y nginx/api.empanad4z.me.conf para confirmar cada RF/RNF.
  - Probé la API en vivo: https://api.empanad4z.me/health (200), /docs (200),
    redirect HTTP→HTTPS (200 final), y /history?limit=1 — devolvió datos reales
    (159k+ registros), confirmando que el pipeline
    broker→connector→master→Postgres está funcionando en producción.
  - Verifiqué el certificado SSL (Let's Encrypt, válido).
  - Resolví el dominio para obtener la IP de tu instancia EC2 (35.168.184.246).

  Resultado: todos los puntos de la parte mínima (RF1-4, RNF1-7, Docker-Compose)
  y ambas opciones de la parte variable (HTTPS + Balanceo de carga) están
  marcados como logrados, con evidencia real detrás de cada check.

  Un detalle que te falta completar tú: en la sección de acceso SSH dejé ssh -i 
  <archivo>.pem ubuntu@35.168.184.246 — reemplaza <archivo>.pem por el nombre
  real de tu llave antes de entregar.

✻ Sautéed for 3m 12s · done 8:35 PM

※ recap: Estamos completando el README de la entrega E0, verificando cada requisito contra el código y la API en producción; ya quedó la sección lista. Solo falta que reemplaces `<archivo>.pem` por el nombre real de tu llave SSH. (disable recaps in /config)

❯ Cambia todos los emojis de check_mark por: [x]. Además no uses em dash (--).  

  Read 1 file, ran 1 shell command (ctrl+o to expand)

● Update(README.md)
  ⎿  Added 1 line, removed 1 line
      14  
      15  **Requisitos funcionales (10p)**
      16  
      17 -- RF1 (3p, Esencial)  — `GET /history`: historial completo con 
         -todos los campos recibidos.                                    
      17 +- RF1 (3p, Esencial) `GET /history`: historial completo con tod
         +os los campos recibidos.                                       
      18  - RF2 (1p) ✅ — `GET /history/{id}`: detalle de un registro, `i
          d` autogenerado por `master`.
      19  - RF3 (2p, Esencial) ✅ — Paginación por defecto de 25 registro
          s vía `page`/`limit`.
      20  - RF4 (4p, Esencial) ✅ — Filtros por prácticamente todos los c
          ampos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exa
          cto o rango, `validUntil` exacto o rango) más orden (`sortBy`, 
          `order`).

● Update(README.md)
  ⎿  Added 18 lines, removed 18 lines
      15  **Requisitos funcionales (10p)**
      16  
      17  - RF1 (3p, Esencial) `GET /history`: historial completo con tod
          os los campos recibidos.
      18 -- RF2 (1p) ✅ — `GET /history/{id}`: detalle de un registro, `i
         -d` autogenerado por `master`.                                  
      19 -- RF3 (2p, Esencial) ✅ — Paginación por defecto de 25 registro
         -s vía `page`/`limit`.                                          
      20 -- RF4 (4p, Esencial) ✅ — Filtros por prácticamente todos los c
         -ampos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exa
         -cto o rango, `validUntil` exacto o rango) más orden (`sortBy`, 
         -`order`).                                                      
      18 +- RF2 (1p) [x] `GET /history/{id}`: detalle de un registro, `id
         +` autogenerado por `master`.                                   
      19 +- RF3 (2p, Esencial) [x] Paginación por defecto de 25 registros
         + vía `page`/`limit`.                                           
      20 +- RF4 (4p, Esencial) [x] Filtros por prácticamente todos los ca
         +mpos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exac
         +to o rango, `validUntil` exacto o rango) más orden (`sortBy`, `
         +order`).                                                       
      21  
      22  **Requisitos no funcionales (20p)**
      23  
      24 -- RNF1 (5p, Esencial) ✅ — `connector` corre en container apart
         -e, se conecta al broker por AMQP+SSL y reenvía cada evento a `m
         -aster` por HTTP POST. Reintenta solo (sin intervención manual) 
         -si se pierde la conexión al broker; `master` sigue respondiendo
         - consultas sobre lo ya guardado aunque el broker o `connector` 
         -estén caídos.                                                  
      25 -- RNF2 (4p, Esencial) ✅ — `master` en su propio container, rec
         -ibe eventos de `connector` por POST, misma red docker.         
      26 -- RNF3 (3p) ✅ — nginx como reverse proxy instalado directament
         -e en el host EC2 (no en Docker), config (luego de instalar y co
         -nfigurar certbot) en `nginx/api.empanad4z.me.conf`. **Esta conf
         -iguración en EC2 se encuentra en `/etc/nginx/sites-available/ap
         -i.empanad4z.me`**                                              
      27 -- RNF4 (2p) ✅ — dominio `api.empanad4z.me` bajo TLD público `.
         -me`.                                                           
      28 -- RNF5 (2p, Esencial) ✅ — corriendo en EC2 free tier (t3.micro
         -).                                                             
      29 -- RNF6 (2p) ✅ — Postgres containerizado, no expuesto a interne
         -t (solo `127.0.0.1`).                                          
      30 -- RNF7 (2p, Esencial) ✅ — los 3 containers (`postgres`, `maste
         -r`, `connector`) declaran `HEALTHCHECK` en `docker-compose.yaml
         -` (`pg_isready`, chequeo HTTP a `/health`, y file-check respect
         -ivamente).                                                     
      24 +- RNF1 (5p, Esencial) [x] `connector` corre en container aparte
         +, se conecta al broker por AMQP+SSL y reenvía cada evento a `ma
         +ster` por HTTP POST. Reintenta solo (sin intervención manual) s
         +i se pierde la conexión al broker; `master` sigue respondiendo 
         +consultas sobre lo ya guardado aunque el broker o `connector` e
         +stén caídos.                                                   
      25 +- RNF2 (4p, Esencial) [x] `master` en su propio container, reci
         +be eventos de `connector` por POST, misma red docker.          
      26 +- RNF3 (3p) [x] nginx como reverse proxy instalado directamente
         + en el host EC2 (no en Docker), config (luego de instalar y con
         +figurar certbot) en `nginx/api.empanad4z.me.conf`. **Esta confi
         +guración en EC2 se encuentra en `/etc/nginx/sites-available/api
         +.empanad4z.me`**                                               
      27 +- RNF4 (2p) [x] dominio `api.empanad4z.me` bajo TLD público `.m
         +e`.                                                            
      28 +- RNF5 (2p, Esencial) [x] corriendo en EC2 free tier (t3.micro)
         +.                                                              
      29 +- RNF6 (2p) [x] Postgres containerizado, no expuesto a internet
         + (solo `127.0.0.1`).                                           
      30 +- RNF7 (2p, Esencial) [x] los 3 containers (`postgres`, `master
         +`, `connector`) declaran `HEALTHCHECK` en `docker-compose.yaml`
         + (`pg_isready`, chequeo HTTP a `/health`, y file-check respecti
         +vamente).                                                      
      31  
      32  **Docker-Compose (15p)**
      33  
      34 -- RNF1 (5p) ✅ — `master` se levanta desde docker compose (con 
         -2 réplicas).                                                   
      35 -- RNF2 (5p) ✅ — `postgres` integrado en el mismo `docker-compo
         -se.yaml`.                                                      
      36 -- RNF3 (5p) ✅ — `connector` se levanta desde docker compose y 
         -queda conectado a `master` por la red interna.                 
      34 +- RNF1 (5p) [x] `master` se levanta desde docker compose (con 2
         + réplicas).                                                    
      35 +- RNF2 (5p) [x] `postgres` integrado en el mismo `docker-compos
         +e.yaml`.                                                       
      36 +- RNF3 (5p) [x] `connector` se levanta desde docker compose y q
         +ueda conectado a `master` por la red interna.                  
      37  
      38  ### Parte variable
      39  
     ...
      41  
      42  **HTTPS (25%, 15p)**
      43  
      44 -- RNF1 (7p) ✅ — dominio asegurado con SSL de Let's Encrypt.   
      45 -- RNF2 (3p) ✅ — redirección automática HTTP → HTTPS.          
      46 -- RNF3 (5p) ✅ — renovación automática del certificado usando c
         -onfiguración que venia en la instalación oficial en `https://ce
         -rtbot.eff.org/instructions?ws=nginx&os=pip`                    
      44 +- RNF1 (7p) [x] dominio asegurado con SSL de Let's Encrypt.    
      45 +- RNF2 (3p) [x] redirección automática HTTP → HTTPS.           
      46 +- RNF3 (5p) [x] renovación automática del certificado usando co
         +nfiguración que venia en la instalación oficial en `https://cer
         +tbot.eff.org/instructions?ws=nginx&os=pip`                     
      47  
      48  **Balanceo de carga con Nginx (25%, 15p)**
      49  
      50 -- RF1 (5p) ✅ — `master` replicado en 2 instancias container en
         - paralelo (`deploy.replicas: 2`).                              
      51 -- RF2 (10p) ✅ — cada réplica alcanzable individualmente (`8080
         --8081:8000`) y balanceadas por nginx vía `upstream` en `/etc/ng
         -inx/sites-available/api.empanad4z.me`.                         
      50 +- RF1 (5p) [x] `master` replicado en 2 instancias container en 
         +paralelo (`deploy.replicas: 2`).                               
      51 +- RF2 (10p) [x] cada réplica alcanzable individualmente (`8080-
         +8081:8000`) y balanceadas por nginx vía `upstream` en `/etc/ngi
         +nx/sites-available/api.empanad4z.me`.                          
      52  
      53  
      54  Servicios (`docker-compose.yaml`):

● Update(README.md)  ⎿  Added 3 lines, removed 3 lines
      53  
      54  Servicios (`docker-compose.yaml`):
      55  
      56 -- **postgres** — base de datos Postgres, corriendo como contain
         -er propio.                                                     
      57 -- **master** — API FastAPI que recibe eventos y los persiste en
         - Postgres.                                                     
      58 -- **connector** — consumidor de RabbitMQ (broker del curso).   
      56 +- **postgres**: base de datos Postgres, corriendo como containe
         +r propio.                                                      
      57 +- **master**: API FastAPI que recibe eventos y los persiste en 
         +Postgres.                                                      
      58 +- **connector**: consumidor de RabbitMQ (broker del curso).    
      59  
      60  ## Setup
      61  

● Update(README.md)
  ⎿  Added 9 lines, removed 9 lines
      67  
      68  ## Comandos del Makefile
      69  
      70 -- `make up` — `docker compose up --build`. Levanta `postgres`, 
         -`master` y                                                     
      70 +- `make up`: `docker compose up --build`. Levanta `postgres`, `
         +master` y                                                      
      71    `connector`.
      72 -- `make start` / `make stop` — arranca/detiene los containers e
         -xistentes                                                      
      72 +- `make start` / `make stop`: arranca/detiene los containers ex
         +istentes                                                       
      73    sin reconstruirlos.
      74 -- `make down` — baja los containers (conserva el volumen de dat
         -os).                                                           
      75 -- `make reset` — igual, pero además borra el volumen (`-v`): Po
         -stgres                                                         
      74 +- `make down`: baja los containers (conserva el volumen de dato
         +s).                                                            
      75 +- `make reset`: igual, pero además borra el volumen (`-v`): Pos
         +tgres                                                          
      76    completamente limpio en el próximo `make up`.
      77 -- `make logs` — sigue los logs de todos los servicios.         
      78 -- `make ps` — estado de los containers.                        
      79 -- `make migrate` — corre `alembic upgrade head` **dentro** del 
         -container                                                      
      77 +- `make logs`: sigue los logs de todos los servicios.          
      78 +- `make ps`: estado de los containers.                         
      79 +- `make migrate`: corre `alembic upgrade head` **dentro** del c
         +ontainer                                                       
      80    `master` que ya está corriendo, contra `postgres`. Requiere q
          ue `make up`
      81    esté levantado. Es una acción deliberada, no automática.
      82 -- `make revision m="mensaje"` — autogenera una migración de Ale
         -mbic                                                           
      82 +- `make revision m="mensaje"`: autogenera una migración de Alem
         +bic                                                            
      83    comparando los modelos (`master/app/models/*`) contra Postgre
          s. Se corre
      84    en el host (no en Docker) usando `uv`, así no hace falta reco
          nstruir la
      85    imagen cada vez que cambiás un modelo. Requiere que `postgres
          ` esté
      86    arriba (`make up`, al menos el servicio `postgres`).
      87 -- `make db-shell` — abre un `psql` interactivo dentro del conta
         -iner                                                           
      87 +- `make db-shell`: abre un `psql` interactivo dentro del contai
         +ner                                                            
      88    `postgres`.
      89  
      90  ### Flujo típico de un cambio de esquema

● Update(README.md)
  ⎿  Added 5 lines, removed 5 lines
      101  - ORM: **SQLAlchemy 2.0** (async, driver `asyncpg`) + **Alembi
           c** para
      102    migraciones.
      103  - Estructura en `master/app/`:
      104 -  - `models/` — entidades ORM (tablas).                       
      105 -  - `schemas/` — modelos Pydantic de entrada/salida de la API.
      106 -  - `repositories/` — acceso a datos (queries de SQLAlchemy). 
      107 -  - `db/` — `base.py` (declarative base) y `session.py` (engin
          -e + sesión                                                    
      104 +  - `models/`: entidades ORM (tablas).                        
      105 +  - `schemas/`: modelos Pydantic de entrada/salida de la API. 
      106 +  - `repositories/`: acceso a datos (queries de SQLAlchemy).  
      107 +  - `db/`: `base.py` (declarative base) y `session.py` (engine
          + + sesión                                                     
      108      async, dependency `get_db` para FastAPI).
      109 -  - `alembic/` — migraciones (en `master/`, junto al `alembic.
          -ini`).                                                        
      109 +  - `alembic/`: migraciones (en `master/`, junto al `alembic.i
          +ni`).                                                         
      110  
      111  ## Deploy en EC2
      112  

● Update(README.md)
  ⎿  Added 2 lines, removed 2 lines
      112  
      113  En la EC2, nginx corre en el host (no containerizado) y hace d
           e reverse
      114  proxy hacia `master` (ver `nginx/api.empanad4z.me.conf`, publi
           cado en
      115 -`localhost:8080-8081` por `docker-compose.yaml`). El resto del
          - stack —                                                      
      116 -`postgres` incluido — corre con `make up` igual que en cualqui
          -er otra                                                       
      115 +`localhost:8080-8081` por `docker-compose.yaml`). El resto del
          + stack,                                                       
      116 +`postgres` incluido, corre con `make up` igual que en cualquie
          +r otra                                                        
      117  máquina.

  Ran 1 shell command (ctrl+o to expand)

● Listo, ya no quedan emojis ✅ ni em dashes (—) en el README: todos los
  checkmarks pasaron a [x] y las separaciones tipo "label — descripción"
  quedaron con :.

  Una cosa que noté: en la línea de RF1 ya no tenía el ✅ cuando revisé el
  archivo (quedaba un espacio doble donde antes estaba el check), así que ese
  ítem quedó sin marcar [x] — no lo agregué porque no sé si fue intencional
  (¿decidiste que RF1 necesita revisión aparte?) o un borrado accidental al
  editar. Si fue sin querer, dime y lo dejo como los demás.

✻ Baked for 1m 14s · done 8:52 PM

❯ El [x] debe ir luego de cada -                                                

  Read 1 file (ctrl+o to expand)

● Update(README.md)
  ⎿  Added 19 lines, removed 19 lines
      14  
      15  **Requisitos funcionales (10p)**
      16  
      17 -- RF1 (3p, Esencial) `GET /history`: historial completo con tod
         -os los campos recibidos.                                       
      18 -- RF2 (1p) [x] `GET /history/{id}`: detalle de un registro, `id
         -` autogenerado por `master`.                                   
      19 -- RF3 (2p, Esencial) [x] Paginación por defecto de 25 registros
         - vía `page`/`limit`.                                           
      20 -- RF4 (4p, Esencial) [x] Filtros por prácticamente todos los ca
         -mpos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exac
         -to o rango, `validUntil` exacto o rango) más orden (`sortBy`, `
         -order`).                                                       
      17 +- [ ] RF1 (3p, Esencial) `GET /history`: historial completo con
         + todos los campos recibidos.                                   
      18 +- [x] RF2 (1p) `GET /history/{id}`: detalle de un registro, `id
         +` autogenerado por `master`.                                   
      19 +- [x] RF3 (2p, Esencial) Paginación por defecto de 25 registros
         + vía `page`/`limit`.                                           
      20 +- [x] RF4 (4p, Esencial) Filtros por prácticamente todos los ca
         +mpos (`city`, `type`, `unit`, `demand`/rango, `receivedAt` exac
         +to o rango, `validUntil` exacto o rango) más orden (`sortBy`, `
         +order`).                                                       
      21  
      22  **Requisitos no funcionales (20p)**
      23  
      24 -- RNF1 (5p, Esencial) [x] `connector` corre en container aparte
         -, se conecta al broker por AMQP+SSL y reenvía cada evento a `ma
         -ster` por HTTP POST. Reintenta solo (sin intervención manual) s
         -i se pierde la conexión al broker; `master` sigue respondiendo 
         -consultas sobre lo ya guardado aunque el broker o `connector` e
         -stén caídos.                                                   
      25 -- RNF2 (4p, Esencial) [x] `master` en su propio container, reci
         -be eventos de `connector` por POST, misma red docker.          
      26 -- RNF3 (3p) [x] nginx como reverse proxy instalado directamente
         - en el host EC2 (no en Docker), config (luego de instalar y con
         -figurar certbot) en `nginx/api.empanad4z.me.conf`. **Esta confi
         -guración en EC2 se encuentra en `/etc/nginx/sites-available/api
         -.empanad4z.me`**                                               
      27 -- RNF4 (2p) [x] dominio `api.empanad4z.me` bajo TLD público `.m
         -e`.                                                            
      28 -- RNF5 (2p, Esencial) [x] corriendo en EC2 free tier (t3.micro)
         -.                                                              
      29 -- RNF6 (2p) [x] Postgres containerizado, no expuesto a internet
         - (solo `127.0.0.1`).                                           
      30 -- RNF7 (2p, Esencial) [x] los 3 containers (`postgres`, `master
         -`, `connector`) declaran `HEALTHCHECK` en `docker-compose.yaml`
         - (`pg_isready`, chequeo HTTP a `/health`, y file-check respecti
         -vamente).                                                      
      24 +- [x] RNF1 (5p, Esencial) `connector` corre en container aparte
         +, se conecta al broker por AMQP+SSL y reenvía cada evento a `ma
         +ster` por HTTP POST. Reintenta solo (sin intervención manual) s
         +i se pierde la conexión al broker; `master` sigue respondiendo 
         +consultas sobre lo ya guardado aunque el broker o `connector` e
         +stén caídos.                                                   
      25 +- [x] RNF2 (4p, Esencial) `master` en su propio container, reci
         +be eventos de `connector` por POST, misma red docker.          
      26 +- [x] RNF3 (3p) nginx como reverse proxy instalado directamente
         + en el host EC2 (no en Docker), config (luego de instalar y con
         +figurar certbot) en `nginx/api.empanad4z.me.conf`. **Esta confi
         +guración en EC2 se encuentra en `/etc/nginx/sites-available/api
         +.empanad4z.me`**                                               
      27 +- [x] RNF4 (2p) dominio `api.empanad4z.me` bajo TLD público `.m
         +e`.                                                            
      28 +- [x] RNF5 (2p, Esencial) corriendo en EC2 free tier (t3.micro)
         +.                                                              
      29 +- [x] RNF6 (2p) Postgres containerizado, no expuesto a internet
         + (solo `127.0.0.1`).                                           
      30 +- [x] RNF7 (2p, Esencial) los 3 containers (`postgres`, `master
         +`, `connector`) declaran `HEALTHCHECK` en `docker-compose.yaml`
         + (`pg_isready`, chequeo HTTP a `/health`, y file-check respecti
         +vamente).                                                      
      31  
      32  **Docker-Compose (15p)**
      33  
      34 -- RNF1 (5p) [x] `master` se levanta desde docker compose (con 2
         - réplicas).                                                    
      35 -- RNF2 (5p) [x] `postgres` integrado en el mismo `docker-compos
         -e.yaml`.                                                       
      36 -- RNF3 (5p) [x] `connector` se levanta desde docker compose y q
         -ueda conectado a `master` por la red interna.                  
      34 +- [x] RNF1 (5p) `master` se levanta desde docker compose (con 2
         + réplicas).                                                    
      35 +- [x] RNF2 (5p) `postgres` integrado en el mismo `docker-compos
         +e.yaml`.                                                       
      36 +- [x] RNF3 (5p) `connector` se levanta desde docker compose y q
         +ueda conectado a `master` por la red interna.                  
      37  
      38  ### Parte variable
      39  
     ...
      41  
      42  **HTTPS (25%, 15p)**
      43  
      44 -- RNF1 (7p) [x] dominio asegurado con SSL de Let's Encrypt.    
      45 -- RNF2 (3p) [x] redirección automática HTTP → HTTPS.           
      46 -- RNF3 (5p) [x] renovación automática del certificado usando co
         -nfiguración que venia en la instalación oficial en `https://cer
         -tbot.eff.org/instructions?ws=nginx&os=pip`                     
      44 +- [x] RNF1 (7p) dominio asegurado con SSL de Let's Encrypt.    
      45 +- [x] RNF2 (3p) redirección automática HTTP → HTTPS.           
      46 +- [x] RNF3 (5p) renovación automática del certificado usando co
         +nfiguración que venia en la instalación oficial en `https://cer
         +tbot.eff.org/instructions?ws=nginx&os=pip`                     
      47  
      48  **Balanceo de carga con Nginx (25%, 15p)**
      49  
      50 -- RF1 (5p) [x] `master` replicado en 2 instancias container en 
         -paralelo (`deploy.replicas: 2`).                               
      51 -- RF2 (10p) [x] cada réplica alcanzable individualmente (`8080-
         -8081:8000`) y balanceadas por nginx vía `upstream` en `/etc/ngi
         -nx/sites-available/api.empanad4z.me`.                          
      50 +- [x] RF1 (5p) `master` replicado en 2 instancias container en 
         +paralelo (`deploy.replicas: 2`).                               
      51 +- [x] RF2 (10p) cada réplica alcanzable individualmente (`8080-
         +8081:8000`) y balanceadas por nginx vía `upstream` en `/etc/ngi
         +nx/sites-available/api.empanad4z.me`.                          
      52  
      53  
      54  Servicios (`docker-compose.yaml`):

● Movido: ahora cada línea usa el formato estándar de checklist - [x] RFx (Xp) 
  .... Para RF1 (que quedó sin marcar en tu edición anterior) usé - [ ] en vez
  de dejarlo sin corchetes, para que el checklist sea consistente — avísame si
  en realidad sí lo lograste y lo paso a [x].

✻ Worked for 44s · done 8:53 PM