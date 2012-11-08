Instalação
===========

Instruções para instalar e configurar o neb2activemq em ambiente CentOS. Todos os comandos devem ser executados como usuário root.

# 1) Requisitos

## 1.1) Requisitos para instalação:
* Nagios
* Python2.6 (incluído no instalador caso não esteja instalado)
* Bibliotecas do python Chardet, Sys-V IPC e Stomppy (instaladas automaticamente caso não existam)

## 1.2) Requisitos para funcionamento:
* ActiveMQ local ou remoto (necessário para receber os eventos enviados pelo ipc2activemq)

# 2) Preparação do ambiente

* Configure os parâmetros do IPC requeridos pelo neb2activemq, incluindo as seguintes variáveis do kernel no arquivo `/etc/sysctl.conf`:
```
    # Controls the default maxmimum size of a message queue
    kernel.msgmnb = 134217728

    # Controls the maximum size of a message, in bytes
    kernel.msgmax = 65536

    # Controls the maximum shared segment size, in bytes
    kernel.shmmax = 68719476736

    # Controls the maximum number of shared memory segments, in pages
    kernel.shmall = 4294967296
```

* Aplique as configurações:
```
    /sbin/sysctl -p /etc/sysctl.conf
```

# 3) Procedimento de instalação

* Descompacte o pacote de instalação em `/opt/intelie`
```
    mkdir -p /opt/intelie
    cd /opt/intelie
    tar xzvf neb2activemq-1.1.6.tar.gz
```

* Rode o instalador:
```
    cd /opt/intelie/neb2activemq/scripts
    ./install.sh
```

O instalador realiza os seguintes passos:
  * compila neb2ipc.o e copia para /usr/bin
  * adiciona a linha "broker_module=/usr/bin/neb2ipc.o" ao arquivo de configuração do Nagios (/etc/nagios/nagios.cfg)
  * reinicia o daemon do Nagios
  * verifica se a fila do IPC foi criada pelo Nagios
  * verifica instalação do python2.6 e o instala (se necessário)
  * instala dependências do python (stomp, sysv_ipc, chardet)
  * instala daemon do ipc2activemq (nebpublisher)

Obs: se os valores padrão dos diretórios do Nagios não correspondem ao seu ambiente, estes podem ser configurados no arquivo `/opt/intelie/neb2activemq/neb2ipc/scripts/install.sh`

# 4) Procedimento de configuração

* Configure o servidor do ActiveMQ para o qual serão enviados os eventos alterando a seguinte linha no arquivo `/opt/intelie/neb2activemq/ipc2activemq/src/nebpublisher/conf/prod/settings.py`:
```
    BROKER = [('localhost', 61613)] # Message Broker Target
```

* Configure os checks e as expressões regulares no arquivo `/opt/intelie/neb2activemq/ipc2activemq/src/nebpublisher/conf/prod/topics.py`

# 5) Procedimento para iniciar ou parar o serviço

* Para iniciar o ipc2activemq:
```
    cd /opt/intelie/neb2activemq/ipc2activemq/src/nebpublisher && ./nebpublisher.sh start
```

* Para parar o ipc2activemq:
```
    cd /opt/intelie/neb2activemq/ipc2activemq/src/nebpublisher && ./nebpublisher.sh force-stop
```

# 6) Procedimento de validação da instalação

* Caso o neb2ipc esteja rodando, aparecerão linhas como estas abaixo no log do Nagios (`/var/log/nagios.log`):
```
    [1334254198] neb2ipc: Copyright (c) 2009 Intelie
    [1334254198] neb2ipc: Created message queue 491520.
    [1334254198] Event broker module '/usr/bin/neb2ipc.o' initialized successfully.
```

* Verifique a fila do IPC criada pelo neb2ipc:
```
    ipcs -q

    ------ Message Queues --------
    key        msqid      owner      perms      used-bytes   messages
    0x0001e240 32768      nagios     600        0            0

```

* Caso o ipc2activemq esteja rodando corretamente, aparecerão linhas como estas abaixo no terminal:
```
    Starting nebpublisher daemon: ipc2activemq.py \n
    configuring log from log.ini
    Running nebpublisher.
    Environment: prod
    Running as daemon: True
    Pidfile: /var/run/nagios/nebpublisher.pid
    Running with profiler: False
```

* Verifique no arquivo de log `/var/log/nagios/nebpublisher.log` se o ipc2activemq se conectou ao ActiveMQ:
```
  2012-04-12 15:25:08,175 misc.py(17) run_as_daemon MainThread: INFO Running as deamon
  2012-04-12 15:25:08,243 stomp.py(645) __attempt_connection MainThread: INFO Established connection to host localhost, port 61613
```

Caso o ActiveMQ esteja inacessível, aparecerá uma linha de log como esta:
```
    2012-04-12 15:28:47,263 stomp.py(655) __attempt_connection MainThread: WARNING Could not connect to host localhost, port 61613: [Errno 111] Connection refused
```

