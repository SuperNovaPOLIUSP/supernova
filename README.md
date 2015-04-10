### TEAM:

Coordenador (Coordinator):

    Giuliano Salcas Olguin

Programadores (Programmers):

    Alan Ferreirós
    Bernardo Mascarenhas C. e Silva
    Caio Cesar di Gesu Janguas
    Diego Rabatone Oliveira
    Fabio Henrique Fabbri
    Felipe "PQI" Cruz Neiva Campos
    Felipe Barker Linero Esteves
    Filipe Vaz Loiola
    Gabriel Souza Victorino Lopes
    Guilherme Henrique Rojas
    Heitor Reis Ribeiro
    Henrique Carvalho Silva
    Juliano Dawid Barboza
    Letícia Li Koga
    Lucas Miller da Fonseca Baldini
    Lucas Pimenta Pereira Ludewigs
    Marcel Henrique G. Sobrinho
    Marcelo Abdala Daher
    Marcelo Pereira Macedo
    Mateus Ojeda
    Sheila Genesine Dada
    Tiago Milagres Miranda
    Vitor Gabriel Rente
    Wellington Felipe Calligaris
    Yan Richard Oliveira
    Yuri Gomes de Abreu

Supernova Installation guide

Software compatibility:
•	Ubuntu 12.04
•	Apache/2.2.22 (Ubuntu)
•	Python 2.7.3
•	MYSQL 5.5.37
•	DJANGO 1.6.2

Auto Multiple Choice 1.2.1
For installation on Ubuntu 04.12, open Linux terminal and type:

sudo add-apt-repository ppa:alexis.bienvenue/amc-stable
sudo apt-get update
sudo apt-get install auto-multiple-choice

Beautiful Soup 3.2.1
For installation on Ubuntu 04.12, open Linux terminal and type:

	sudo pip install BeautifulSoup

If you do not have pip program installed on the server, open Linux terminal and type:
	sudo apt-get install python-pip

MatPlotLib 1.3.1
For installation on Ubuntu 04.12, open Linux terminal and type:

	sudo apt-get install python-matplotlib

PDFLatex 3.14 (2012 or newer)
For installation on Ubuntu 04.12, open Linux terminal and type:

	sudo add-apt-repository ppa:texlive-backports/ppa       
	sudo apt-get update
	sudo apt-get install texlive-full
Install adjmulticol.sty pack (Required for AutoMultipleChoice)
Copy the directory “adjmulticol” to the path
	/usr/share/texmf-texlive/tex/latex/


To copy by the terminal, use the command below on the root of adjmulticol directory:
	cp -ra adjmulticol/ usr/share/texmf-texlive/tex/latex/

Observation: If the server operating system is not Ubuntu, the destination of adjmulticol directory can be another.
Observation: The command Texlive-full will install the pdflatex with many others extra packages, but it is not absolutely necessary and makes the download size much bigger.

Installation steps:
1 – Create a public user on server for the Supernova system, for example:
	adduser supernova

2 – Put the aeSupernova, pulsarInterface and tools directories on the newly created user’s directory, for example:
/home/supernova/aeSupernova
/home/supernova/aeSupernova/pulsarInterface
/home/supernova/aeSupernova/tools

3 – Put django-settings.py on var/”newly created user” directory, for example:
	/var/supernova/.django-settings.py

4 – Create Data Base. After installing MYSQL and copy the supernova.sql and users.sql files to a desired directory on server, type on UBUNTU 12.04 terminal:
mysql -u root -p[root_password] supernova < supernova.sql
mysql -u root -p[root_password] users < users.sql

5 – Change apache settings. Put the file ae_supernova on /etc/apache2/sites-enabled/ making changes related to the server. For example:
<VirtualHost *:80>
    ServerAdmin meunomeeesse@gmail.com
    ServerName 111.111.111.111
    ServerAlias 111.111.111.111
    DocumentRoot /home/supernova/
    LogLevel warn
    WSGIScriptAlias / /home/supernova/aeSupernova/aeSupernova/wsgi.py

    <Directory /home/supernova/>
        Options Indexes FollowSymLinks MultiViews
        Order deny,allow
        Deny from all
    </Directory>
</VirtualHost>

Copy the altered file in the same directory and name it as mysite
Copy the altered file, move it to the directory /etc/apache2/sites-available/ and name it as ae_supernova

6 – Set WSGI. The file aeSupernova.wsgi must be moved to the root directory from the directory aeSupernova and be set according with the structure of server directories. For example:
import sys
import os
import os.path

sys.path.append('/home/supernova/')
sys.path.append('/home/supernova/aeSupernova')
sys.path.append('/home/supernova/aeSupernova/aeSupernova')
sys.path.append('/home/supernova/public')
os.environ['DJANGO_SETTINGS_MODULE'] = 'aeSupernova.aeSupernova.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

7 – Set settings.db. The file is in the directory aeSupernova/aeSupernova and must be set according with the server and with supernova data base user and password. For example:
111.111.111.111
usuariosupernova
senhasupernova
supernova

8 – Set .django-settings.py. The file .django-settings.py is responsible for Supernova system settings and must be altered according with system administrator needs. For exemple:
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('admin', 'admin@gmail.com')
)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '111.111.111.111']

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'users',
        'USER': 'usuario',          
        'PASSWORD': 'senha',     
        'HOST': '111.111.111.111',   
        'PORT': ''                    
    },
    'supernova': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'supernova',                     
        'USER': 'usuario',                      
        'PASSWORD': 'senha',                  
        'HOST': '111.111.111.111',           
        'PORT': '',                     
    }
}

############### VARIABLES ########################

PASTA_TEMPORARIA = '/home/supernova/temp/'
PASTA_RELATORIOS = '/home/supernova/public/relatorios/disciplinas'
TEMPLATE_RELATORIOS = '/home/supernova/aeSupernova/aeSupernova/document/templates/'
PASTA_RELATORIOS_SEPARADO = '/home/supernova/public/relatorios/separado_por_semestres/'
ARQUIVO_CONF_BD = '/home/supernova/aeSupernova/settings.db'
PASTA_SUPERNOVA = '/home/supernova/aeSupernova/'
LOGIN_PAGE = '/aeSupernova/login/'
________________________________________
MEDIA_ROOT = '/home/supernova/public/'







________________________________________
TEMPLATE_DIRS = (
    '/home/supernova/aeSupernova/aeSupernova/opticalSheet/templates',
    '/home/supernova/aeSupernova/aeSupernova/datafile/templates',
    '/home/supernova/aeSupernova/aeSupernova/header/templates',
    '/home/supernova/aeSupernova/aeSupernova/generator/templates',
    '/home/supernova/aeSupernova/aeSupernova/control/templates',
    '/home/supernova/aeSupernova/aeSupernova/encoder/templates',
    '/home/supernova/aeSupernova/aeSupernova/presentation/templates',
    '/home/supernova/aeSupernova/aeSupernova/templates',
    '/home/supernova/aeSupernova/aeSupernova/lerJupiter/templates',
    '/home/supernova/aeSupernova/aeSupernova/algeLin/templates',
    '/home/supernova/aeSupernova/templates/login',
    '/home/supernova/aeSupernova/templates/interface',
)

9 - Ports to be released on the server:
8081 TCP
8000 TCP
3306 TCP
80   TCP

10 – After all settings, create a user to be able to connect to the system is required. To do this, open Linux terminal and go to aeSupernova directory which contains the manage.py file.
	python manage.py shell

This command will initiate a django shell. In this shell type:
from django.contrib.auth.models import User
user = User.objects.create_user('nome', 'nome@gmail.com', 'senha')
user.save()

11 – After user creation, you can connect to the system typing in the browser address bar “your server IP/login”. For example:
	111.111.111.111/login



﻿# Manual de Instalação SUPERNOVA

O sistema é compatível com:
 
- Ubuntu 12.04
- Apache/2.2.22 (Ubuntu)
- Python 2.7.3
- MYSQL 5.5.37
- DJANGO 1.6.2
- Auto Multiple Choice 1.2.1
    
    Para instalação no Ubuntu 12.04, abrir terminal do Linux e digitar:
    
        sudo add-apt-repository ppa:alexis.bienvenue/amc-stable
        sudo apt-get update
        sudo apt-get install auto-multiple-choice

- Beautiful Soup 3.2.1
    
    Para instalação no Ubuntu 12.04, abrir terminal do Linux e digitar:

        sudo pip install BeautifulSoup
    
    Caso não tenha o programa pip instalado no servidor, abrir terminal do Linux e digitar:

        sudo apt-get install python-pip

- MatPlotLib 1.3.1
    
    Para instalação no Ubuntu 12.04, abrir terminal do Linux e digitar:

        sudo apt-get install python-matplotlib

- PDFLatex 3.14 (2012 ou mais novo)
    
    Para instalação no Ubuntu 12.04, abrir terminal do Linux e digitar:

        sudo add-apt-repository ppa:texlive-backports/ppa       
        sudo apt-get update
        sudo apt-get install texlive-full

    Instalar pacote adjmulticol.sty (Necessário para o AutoMultipleChoice)
    
    Copiar pasta adjmulticol para o caminho:

        /usr/share/texmf-texlive/tex/latex/
        
    Para fazer a cópia via terminal, utilize o comando abaixo na raiz do pasta adjmulticol:

        cp -ra adjmulticol/ usr/share/texmf-texlive/tex/latex/

  Observação: Caso o sistema operacional do servidor não seja o Ubuntu, o destino da pasta adjmulticol pode ser outro.

 Observação: O comando texlive-full instalará o pdflatex com muitos pacotes extras, porém isso não é totalmente necessário e torna o tamanho do download muito grande.
    
#### PASSOS PARA INSTALAÇÃO:

1 - Criar um usuário publico no servidor para o sistema Supernova, por exemplo:

    adduser supernova
2 - Descarregar pastas aeSupernova, pulsarInterface e tools na pasta do usuário recém-criado, por exemplo:

    /home/supernova/aeSupernova
    /home/supernova/aeSupernova/pulsarInterface
    /home/supernova/aeSupernova/tools
3 - Descarregar .django-settings.py na pasta var/”usuário recém criado”, por exemplo:

    /var/supernova/.django-settings.py
4 - Criar bancos de dados. Após instalar o MYSQL e copiar os arquivos supernova.sql e users.sql para uma pasta  desejada do servidor, digitar no terminal no Ubuntu 12.04:

    mysql -u root -p[root_password] supernova < supernova.sql
    mysql -u root -p[root_password] users < users.sql
5 - Alterar configurações do apache. Descarregar arquivo ae_supernova em /etc/apache2/sites-enabled/ fazendo as modificações referentes ao servidor. Um exemplo é exibido abaixo.

    <VirtualHost *:80>
        ServerAdmin meunomeeesse@gmail.com
        ServerName 111.111.111.111
        ServerAlias 111.111.111.111
        DocumentRoot /home/supernova/
        LogLevel warn
        WSGIScriptAlias / /home/supernova/aeSupernova/aeSupernova/wsgi.py

        <Directory /home/supernova/>
            Options Indexes FollowSymLinks MultiViews
            Order deny,allow
            Deny from all
        </Directory>
    </VirtualHost>
Faça uma cópia deste arquivo já alterado na mesma pasta e nomeie-o como     mysite.

Faça uma cópia deste arquivo já alterado, mova-o para a pasta   /etc/apache2/sites-available/ e nomeie-o como ae_supernova.

6 - Configurar WSGI. O arquivo aeSupernova.wsgi deverá ser movido para a pasta raiz da pasta aeSupernova e configurado de acordo com a estrutura de pastas do servidor. Um exemplo é exibido abaixo.

    import sys
    import os
    import os.path

    sys.path.append('/home/supernova/')
    sys.path.append('/home/supernova/aeSupernova')
    sys.path.append('/home/supernova/aeSupernova/aeSupernova')
    sys.path.append('/home/supernova/public')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'aeSupernova.aeSupernova.settings'

    from django.core.handlers.wsgi import WSGIHandler
    application = WSGIHandler()

7 - Configurar settings.db. O arquivo está na pasta aeSupernova/aeSupernova e deverá ser configurado de     acordo com o servidor e com usuário e senha do banco de dados supernova. Um exemplo é exibido abaixo.

    111.111.111.111
    usuariosupernova
    senhasupernova
    supernova
8 - Configurar .django-settings.py. O arquivo .django-settings.py é responsável pelas configurações do sistema Supernova e deverá ser alterado de acordo com as necessidades do administrador do sistema.
Um exemplo das opções a serem configuradas é exibido abaixo:

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    ADMINS = (
        ('admin', 'admin@gmail.com')
    )

    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '111.111.111.111']

    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'users',
            'USER': 'usuario',          
            'PASSWORD': 'senha',     
            'HOST': '111.111.111.111',   
            'PORT': ''                    
        },
        'supernova': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'supernova',                     
            'USER': 'usuario',                      
            'PASSWORD': 'senha',                  
            'HOST': '111.111.111.111',           
            'PORT': '',                     
        }
    }

    ############### VARIABLES ########################

    PASTA_TEMPORARIA = '/home/supernova/temp/'
    PASTA_RELATORIOS = '/home/supernova/public/relatorios/disciplinas'
    TEMPLATE_RELATORIOS = '/home/supernova/aeSupernova/aeSupernova/document/templates/'
    PASTA_RELATORIOS_SEPARADO = '/home/supernova/public/relatorios/separado_por_semestres/'
    ARQUIVO_CONF_BD = '/home/supernova/aeSupernova/settings.db'
    PASTA_SUPERNOVA = '/home/supernova/aeSupernova/'
    LOGIN_PAGE = '/aeSupernova/login/'
--------------
    MEDIA_ROOT = '/home/supernova/public/'
----------
    TEMPLATE_DIRS = (
        '/home/supernova/aeSupernova/aeSupernova/opticalSheet/templates',
        '/home/supernova/aeSupernova/aeSupernova/datafile/templates',
        '/home/supernova/aeSupernova/aeSupernova/header/templates',
        '/home/supernova/aeSupernova/aeSupernova/generator/templates',
        '/home/supernova/aeSupernova/aeSupernova/control/templates',
        '/home/supernova/aeSupernova/aeSupernova/encoder/templates',
        '/home/supernova/aeSupernova/aeSupernova/presentation/templates',
        '/home/supernova/aeSupernova/aeSupernova/templates',
        '/home/supernova/aeSupernova/aeSupernova/lerJupiter/templates',
        '/home/supernova/aeSupernova/aeSupernova/algeLin/templates',
        '/home/supernova/aeSupernova/templates/login',
        '/home/supernova/aeSupernova/templates/interface',
    )

9 - Portas a serem liberadas no servidor:

    8081 TCP
    8000 TCP
    3306 TCP
    80   TCP


10 - Após todas as configurações, é necessário a criação de um usuário para conseguir se conectar ao sistema. Para isso, abra o terminal do Linux e vá até a pasta aeSupernova, que contém o arquivo manage.py. Digite os seguintes comandos no terminal:

    python manage.py shell

Este comando irá iniciar um shell do django. Neste shell digite:

    from django.contrib.auth.models import User
    user = User.objects.create_user('nome', 'nome@gmail.com', 'senha')
    user.save()

11 - Após a criação do usuário você poderá se conectar ao sistema digitando na barra de endereços de seu navegador “IP do seu servidor/login”. 

    Ex: 111.111.111.111/login 


