#
# Conditional build:
# _without_cups	- without CUPS support
# _with_ldap	- with LDAP-based auth (instead of smbpasswd)
# _with_ipv6    - with IPv6 support
#
%define		vscan_version 0.3.2b
Summary:	SMB server
Summary(cs):	Server SMB
Summary(da):	SMB server
Summary(de):	SMB-Server
Summary(es):	El servidor SMB
Summary(fi):	SMB-palvelin
Summary(fr):	Serveur SMB
Summary(it):	Server SMB
Summary(ja):	Samba SMB ╔╣║╪╔п║╪
Summary(ko):	╩О╧ы SMB ╪╜╧Ж
Summary(pl):	Serwer SMB
Summary(pt_BR):	Cliente e servidor SMB
Summary(ru):	SMB клиент и сервер
Summary(tr):	SMB sunucusu
Summary(uk):	SMB кл╕╓нт та сервер
Summary(zh_CN):	Samba ©м╩╖╤к╨м╥ЧнЯфВ
Name:		samba
Version:	2.2.8a
Release:	1.4
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.samba.org/samba/ftp/%{name}-%{version}.tar.bz2
# Source0-md5:	51466fdd7b7125a5bd41608a76e8e7c8
Source1:	smb.init
Source2:	%{name}.pamd
Source3:	swat.inetd
Source4:	%{name}.sysconfig
Source5:	%{name}.logrotate
Source6:	smb.conf
Source7:	http://dl.sourceforge.net/openantivirus/samba-vscan-%{vscan_version}.tar.bz2
# Source7-md5:	cacc32f21812494993e32be558b91bdd
Patch1:		%{name}-config.patch
Patch2:		%{name}-DESTDIR.patch
Patch3:		%{name}-manpages_PLD_fixes.patch
Patch4:		%{name}-smbprint.patch
Patch5:		%{name}-autoconf.patch
Patch6:		%{name}-smbadduser.patch
Patch7:		%{name}-nmbd_socket.patch
Patch8:		%{name}-vfs.patch
Patch9:		%{name}-quota.patch
Patch10:	http://v6web.litech.org/samba/%{name}-2.2.4+IPv6-20020609.diff
Patch11:	%{name}-DESTDIR-fix.patch
Patch12:	%{name}-CIFS-extensions.patch
URL:		http://www.samba.org/
BuildRequires:	autoconf
%{!?_without_cups:BuildRequires:	cups-devel}
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	readline-devel >= 4.2
BuildRequires:	pam-devel > 0.66
%{?_with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	pam >= 0.66
Requires:	samba-common = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/samba
%define		_reallibdir	/usr/lib
%define		_libdir		%{_sysconfdir}
%define		_localstatedir	%{_var}/log/samba
%if 0%{!?_without_cups:1}
%define		cups_serverbin	%(cups-config --serverbin)
%endif

%description
Samba provides an SMB server which can be used to provide network
services to SMB (sometimes called "Lan Manager") clients, including
various versions of MS Windows, OS/2, and other Linux machines. Samba
also provides some SMB clients, which complement the built-in SMB
filesystem in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame) protocol.

This release is known as the "Locking Update" and has full support for
Opportunistic File Locking. In addition this update includes native
support for Microsoft encrypted passwords, improved browse list and
WINS database management.

Please refer to the WHATSNEW.txt document for fixup information. This
binary release includes encrypted password support. Please read the
smb.conf file and ENCRYPTION.txt in the docs directory for
implementation details.

%description -l cs
Samba poskytuje server SMB, kterЩ lze pou╬Мt pro poskytovАnМ sМ╩ovЩch
slu╬eb klientЫm SMB (nЛkdy nazЩvanЩch klienti "LAN mana╬er") vХetnЛ
klientЫ rЫznЩch verzМ MS Windows, OS/2 a dal╧Мch linuxovЩch strojЫ.
Samba tИ╬ poskytuje nЛkterИ klienty SMB, kteЬМ komplementujМ vestavЛnЩ
souborovЩ systИm SMB v Linuxu. Samba pou╬МvА protokoly NetBIOS pЬes
TCP/IP (NetBT) a NEpotЬebuje protokol NetBEUI (neformАtovanЩ rАmec
NetBIOS od spoleХnosti Microsoft.

%description -l da
Samba tilbyder en SMB server som kan bruges til at tilbyde netvФrk
services til SMB (ogsЕ kaldet "Lan Manager") klienter, incl.
forskellige versioner af MS Windows, OS/2, og andre Linux maskiner.
Samba tilbyder ogsЕ SMB klienter, som udbygger det indbyggede SMB
filsystem i Linux. Samba benytter NetBIOS over TCP/IP (NetBT)
protocolen og krФver ikke NetBEUI (Microsoft Raw NetBIOS frame)
protokollen.

%description -l de
Samba stellt einen SMB-Server zum Anbieten von Netzwerkdiensten fЭr
SMB-Clients (auch "Lan Manager" genannt) zur VerfЭgung, darunter
verschiedenen Versionen von MS Windows-, OS/2- und anderen
Linux-Rechnern. Samba enthДlt auъerdem einige SMB-Clients, die das in
Linux integrierte SMB-Dateisystem ergДnzen. Samba benutzt
NetBIOS-Эber-TCP/IP (NetBT)-Protokolle und benЖtigt KEIN NetBEUI
(Microsoft Raw NetBIOS frame)-Protokoll.

%description -l es
Samba provee un servidor SMB que se puede usar para ofrecer servicios
de red a clientes SMB (algunas veces se le llama de "Lan Manager"),
incluyendo varias versiones de MS Windows, OS/2, y otras mАquinas
Linux. Samba tambiИn ofrece algunos clientes SMB, que complementan el
sistema de archivos SMB de Linux. Samba usa el protocolo NetBIOS sobre
TCP/IP (NetBT) y no necesita del protocolo NetBEUI (Microsoft Raw
NetBIOS frame).

%description -l fi
Samba on SMB-palvelin, jota voidaan kДyttДД SMB-asiakasohjelmien
verkkopalvelujen tarjoajana. SMB-protokollaa kutsutaan joskus "Lan
Manager" protokollaksi ja asiakasohjelmat toimivat dosissa,
Windowseissa, OS/2:ssa ja toisissa Linux-koneissa. Samban mukana on
myЖs joitakin SMB-asiakasohjelmia, jotka tДydentДvДt Linuxin
kernelissД olevaa SMB-tiedostojДrjestelmДn tukea. Samba vaatii NetBIOS
over TCP/IP (NetBT) protokollaa eikД tarvitse tai pysty kДyttДmДДn
NetBEUI-protokollaa.

%description -l it
Samba fornisce un server SMB che puo` essere usato per fornire servizi
di rete ai client SMB, incluse le versioni MS Windows, OS/2 e per
altre macchine Linux. Samba fornisce anche i client SMB. Samba usa
NetBIOS sopra TCP/IP e non ha bisogno del protocollo NetBEUI.

%description -l ja
Samba ╓о MS Windows ╓нмм║╧╓й╔п║╪╔╦╔Г╔С║╒OS/2 ╓╫╓╥╓фб╬╓н Linux ╔ч╔╥╔С
╓Р╢ч╓Ю SMB (╓©╓ч╓к "Lan Manager" ╓х╦ф╓п╓Л╓К)
╔╞╔И╔╓╔╒╔С╔х╓к╔м╔ц╔х╔О║╪╔╞ ╔╣║╪╔с╔╧╓РдС╤║╓╧╓К╓©╓А╓к╩хмя╓╣╓Л╓К SMB
╔╣║╪╔п╓РдС╤║╓╥╓ч╓╧║ёSamba ╓о NetBIOS over TCP/IP (NetBT)
╔в╔М╔х╔Ё╔К╓Р╩хмя╓╥║╒ NetBEUI(Microsoft Raw NetBIOS frame)
╔в╔М╔х╔Ё╔К╓ои╛мв╓╒╓Й╓ч╓╩╓С║ё

Samba ╓ш╓х╓С╓иф╟╨Н╓╧╓К NT ╔и╔А╔╓╔С╔Ё╔С╔х╔М║╪╔К╓н╣║г╫╓Рфцд╖╓х╓╥║╒
╧╔╓╜╓й╔ж╔И╔╕╔╤╓Р╩х╓ц╓ф samba ╓н smb.conf ╔у╔║╔╓╔К╓Р╔Й╔Б║╪╔х╢имЩ╓╧╓К
©╥╓╥╓╓ SWAT (Samba Web Administration Tool) ╓Р╢ч╓ъ╓ч╓╧║ё
лэ╡╪╓н╓х╓Ё╓М╓Ё╓Л╓о inetd ╓Рдл╓╥╓ф TCP ╔щ║╪╔х 901 ╓гм╜╦З╓к╓й╓Й╓ч╓╧║ё

%description -l ko
╩О╧ы╢б MS Windows, OS/2, х╓ю╨ ╢ы╦╔ ╦╝╢╙╫╨ ╦с╫ею╩ фВгтго╢б SMB(х╓ю╨
"Lan Manager"╤С╟М╣╣ ╨р╦╡) е╛╤Сюл╬Пф╝╦╕ Ёвф╝©Же╘ ╪╜╨Я╫╨ ю╖гь ╩Г©Кгр ╪Ж
юж╢б SMB ╪╜╧Ж╦╕ а╕╟Ьгя╢ы. ╩О╧ы╢б TCP/IP га╥неДдщю╩ еКгь NetBIOS╦╕
╩Г©Кго╟М NetBEUI (Microsoft Raw NetBIOS га╥╧юс) га╥неДдщю╨ гй©ДгоаЖ
╬й╢ы.

╩О╧ы-2.2 юг ф╞б║ю╨ NT ╣╣╦чюн даф╝╥яюг ╪╨╢ию╦╥н юш╬Вю╩ го╟М, ╩У╥н©Н
SWAT(Samba Web Administration Tool)╥н ю╔╨Й╤С©ЛюЗ╦╕ ╩Г©Кго©╘ ©Ь╟щаЖ©║╪╜
╩О╧ыюг smb.conf фдюою╩ ╟Э╦╝го╣╣╥о гя╢ы. юл╥╞гя ╟Ф©Л inetd ╣╔╦Сю╩ еКгь
TCP 901 фВф╝╦╕ ╩Г©Кго╟т ╣х╢ы.

цж╠ы а╓╨╦╥н WHATSNEW.txt фдюоюг ╧╝╪╜╦╕ бЭ╟Мго╣╣╥о гя╢ы. ╧ыюлЁй╦╝юг
╦╠╦╝аН╢б ╬охёх╜╣х фп╫╨©Ж╣Е╦╕ а╕╟Ьгя╢ы. ╠╦гЖ©║ ╢Кгя юз╪╪гя а╓╨╦╦╕ ╬Р╠Б
ю╖гь docs ╣П╥╨еД╦╝Ё╩©║ юж╢б smb.conf фдюо╟З ENCRYPTION.txt фдюою╩
юп╬Н╨╩╢ы.

%description -l pl
Samba udostЙpnia serwer SMB, ktСry mo©e byФ u©yty w celu dostarczenia
usЁug sieciowych (potocznie zwanych "Lan Manager"), dla klientСw
takich jak MS Windows, OS/2 a tak©e maszyn linuksowych. W pakiecie
znajduje siЙ rСwnie© oprogramowanie klienckie. Samba u©ywa protokoЁu
NetBIOS po TCP/IP (NetBT) i nie wymaga protokoЁu NetBEUI. Ta wersja ma
peЁne wsparcie dla blokowania plikСw, a tak©e wsparcie dla kodowania
haseЁ w standardzie MS i zarzadzania baz╠ WINS.

%description -l pt_BR
O Samba provЙ um servidor SMB que pode ser usado para oferecer
serviГos de rede a clientes SMB (algumas vezes chamado de "Lan
Manager"), incluindo vАrias versУes de MS Windows, OS/2, e outras
mАquinas Linux. O Samba tambИm fornece alguns clientes SMB, que
complementam o sistema de arquivos SMB do Linux. O Samba usa o
protocolo NetBIOS sobre TCP/IP (NetBT) e nЦo necessita do protocolo
NetBEUI (Microsoft Raw NetBIOS frame).

O Samba inclui a maioria das caracterМsticas de um servidor de
Controle de DomМnios NT e o SWAT (Samba Web Administration Tool), que
permite que o arquivo smb.conf seja gerenciado remotamente atravИs de
um navegador. Atualmente isto estА sendo habilitado na porta TCP 901
via inetd.

%description -l ru
Samba предоставляет SMB-сервер, который может быть использован для
предоставления сетевых сервисов SMB (иногда называемым "Lan Manager")
клиентам, включая разнообразные версии MS Windows, OS/2, и другие
Linux-машины. Samba также предоставляет SMB-клиентов, которые работают
со встроенной в Linux файловой системой SMB.

Samba использует протокол NetBIOS over TCP/IP (NetBT) и не нуждается в
протоколе NetBEUI (Microsoft Raw NetBIOS frame).

Samba содержит практически работающую реализацию NT Domain Control и
включает новый SWAT (Samba Web Administration Tool), который позволяет
удаленно управлять конфигурационным файлом smb.conf при помощи вашего
любимого WEB-броузера. Пока что он разрешен через inetd на TCP-порту
901.

%description -l uk
Samba нада╓ SMB-сервер, що може бути використаний для надання
мережевих серв╕с╕в SMB (що ╖х ╕нод╕ називають "Lan Manager") кл╕╓нтам,
включаючи р╕зноман╕тн╕ верс╕╖ MS Windows, OS/2, та ╕нш╕ Linux-машини.
Samba також нада╓ SMB-кл╕╓нт╕в, що працюють з вбудованою в Linux
файловою системою SMB.

Samba використову╓ протокол NetBIOS over TCP/IP (NetBT) та не потребу╓
протоколу NetBEUI (Microsoft Raw NetBIOS frame).

Samba м╕стить майже працюючу реализац╕ю NT Domain Control та новый
SWAT (Samba Web Administration Tool), котрий дозволя╓ в╕ддалено
керувати конф╕гурац╕йним файлом smb.conf за допомогою вашого
улюбленого WEB-броузера. Поки що в╕н дозволений через inetd на
TCP-порту 901.

%package -n swat
Summary:	Samba Web Administration Tool
Summary(es):	Samba SWAT and Web documentation
Summary(pl):	NarzЙdzie administracyjne serwisu Samba
Summary(pt_BR):	Samba SWAT e documentaГЦo Web
Summary(ru):	Программа конфигурации SMB-сервера Samba
Summary(uk):	Програма конфигурац╕╖ SMB-сервера Samba
Group:		Networking/Admin
Requires:	%{name}
Requires:	rc-inetd >= 0.8.2
Requires:	inetdaemon
Provides:	samba-swat
Obsoletes:	samba-swat

%description -n swat
swat allows a Samba administrator to configure the complex smb.conf
file via a Web browser. In addition, a swat configuration page has
help links to all the configurable options in the smb.conf file
allowing an administrator to easily look up the effects of any change.

%description -n swat -l pl
swat pozwala na kompleksow╠ konfiguracjЙ smb.conf przy pomocy
przegl╠darki WWW.

%description -n swat -l pt_BR
SWAT - ferramentada Web de configuraГЦo do Samba.

%description -n swat -l ru
Пакет samba-swat включает новый SWAT (Samba Web Administration Tool),
для удаленного администрирования файла smb.conf при помощи вашего
любимого Web-браузера.

%description -n swat -l uk
Пакет samba-swat м╕стить новий SWAT (Samba Web Administration Tool),
для дистанц╕йного адм╕н╕стрування файлу smb.conf за допомогою вашого
улюбленого Web-браузеру.

%package client
Summary:	Samba client programs
Summary(es):	Cliente SMB de Samba
Summary(ja):	Samba (SMB) ╔╞╔И╔╓╔╒╔С╔х╔в╔М╔╟╔И╔Ю
Summary(pl):	Klienci serwera Samba
Summary(pt_BR):	Cliente SMB do samba
Summary(ru):	Клиентские программы Samba (SMB)
Summary(uk):	Кл╕╓нтськ╕ програми Samba (SMB)
Group:		Applications/Networking
Requires:	samba-common = %{version}
Obsoletes:	smbfs

%description client
Samba-client provides some SMB clients, which complement the build-in
SMB filesystem in Linux. These allow accessing of SMB shares and
printing to SMB printers.

%description client -l pt_BR
O pacote samba-clientes prove alguns clientes SMB, que complementam o
sistema de arquivos SMB do Linux. Eles permitem o acesso a shares SMB,
e tambИm, Ю impressoras SMB.

%description client -l es
Cliente SMB de Samba.

%description client -l ja
Samba-client ╓о Linux ╬Е╓к╢ч╓ч╓Л╓ф╓╓╓К SMB ╔у╔║╔╓╔К╔╥╔╧╔ф╔Ю╓РйД╓╕ SMB
╔╞╔И╔╓╔╒╔С╔х╓РдС╤║╓╥╓ч╓╧║ё╓Ё╓Л╓И╓о SMB ╤╕м╜╓н╔╒╔╞╔╩╔╧╓х SMB
╔в╔Й╔С╔©╓ь╓н╟У╨Ч╓Р╣Ж╡д╓╥╓ч╓╧║ё

%description client -l pl
Samba-client dostarcza pewne programy ktСre uzupeЁniaj╠ system plikСw
SMB zawarty w j╠drze. Pozwala na wspСЁdzielenie i drukowanie w sieci
SMB.

%description client -l pt_BR
O pacote samba-clientes prove alguns clientes SMB, que complementam o
sistema de arquivos SMB do Linux. Eles permitem o acesso a shares SMB,
e tambИm, Ю impressoras SMB.

%description client -l ru
Пакет samba-client предоставляет некоторые клиенты SMB для работы со
встроенной файловой системой SMB в Linux. Эти клиенты позволяют
получать доступ к разделяемым каталогам SMB и печать на SMB-принтеры.

%description client -l uk
Пакет samba-client нада╓ деяк╕ кл╕╓нти SMB для роботи з╕ вбудованою
файловою системою SMB в Linux. Ц╕ кл╕╓нти дозволяють отримувати доступ
до каталог╕в сп╕льного використання SMB та друк на SMB-пр╕нтери.

%package common
Summary:	Files used by both Samba servers and clients
Summary(es):	Common files between samba and samba-clients
Summary(ja):	Samba ╔╣║╪╔п║╪╓х╔╞╔И╔╓╔╒╔С╔х╓г╩хмя╓╣╓Л╓К╔в╔М╔╟╔И╔Ю
Summary(pl):	Pliki u©ywane przez serwer i klientСw Samba
Summary(pt_BR):	Arquivos em comum entre samba e samba-clients
Summary(ru):	Файлы, используемые как сервером, так и клиентом Samba
Summary(uk):	Файли, що використовуються як сервером, так ╕ кл╕╓нтом Samba
Group:		Networking/Daemons

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description common -l ja
Samba-common ╓о Samba ╓н╔╣║╪╔п╓х╔╞╔И╔╓╔╒╔С╔х╓нн╬йЩ╓н╔я╔ц╔╠║╪╔╦╓г
╩хмя╓╣╓Л╓К╔у╔║╔╓╔К╓РдС╤║╓╥╓ч╓╧║ё

%description common -l pl
Samba-common dostarcza pliki niezbЙdne zarСwno dla serwera jak i
klientСw Samba.

%description common -l pt_BR
Arquivos em comum entre os pacotes samba e samba-clients.

%description common -l ru
Samba-common содержит файлы, необходимые для работы как клиента, так и
сервера Samba.

%description common -l uk
Samba-common м╕стить файли, необх╕дн╕ для роботи як кл╕╓нта, так ╕
сервера Samba.

%package -n pam-pam_smbpass
Summary:	PAM Samba Password Module
Summary(pl):	ModuЁ PAM smbpass
Group:		Base
Obsoletes:	pam_smbpass

%description -n pam-pam_smbpass
PAM module which can be used on conforming systems to keep the
smbpasswd (Samba password) database in sync with the unix password
file.

%description -n pam-pam_smbpass -l pl
ModuЁ PAMa, ktСry mo©e byФ u©ywany do trzymania pliku smbpasswd (hasЁa
Samby) zsynchronizowanego z hasЁami unixowymi.

%package -n libsmbclient
Summary:	libsmbclient - samba client library
Summary(pl):	libsmbclient - biblioteka klienta samby
Group:		Libraries

%description -n libsmbclient
libsmbclient - library that allows to use samba clients functions.

%description -n libsmbclient -l pl
libsmbclient - biblioteka pozwalaj╠ca korzystaФ z funcji klienta
samby.

%package -n libsmbclient-devel
Summary:	libsmbclient - samba client library
Summary(pl):	libsmbclient - biblioteka klienta samby
Summary(pt_BR):	Ferramentas de desenvolvimento para clientes samba
Group:		Development/Libraries
Requires:	libsmbclient = %{version}

%description -n libsmbclient-devel
Header files for libsmbclient.

%description -n libsmbclient-devel
Pliki nagЁСwkowe dla libsmbclient.

%description -n libsmbclient-devel -l pt_BR
Arquivos de inclusЦo, bibliotecas e documentaГЦo necessАrios para
desenvolver aplicativos clientes para o samba.

%package -n cups-backend-smb
Summary:	CUPS backend for printing to SMB printers
Summary(pl):	Backend CUPS-a drukuj╠cy na drukarkach SMB
Group:		Applications/Printing
Requires:	cups
Requires:	samba-client = %{version}

%description -n cups-backend-smb
CUPS backend for printing to SMB printers.

%description -n cups-backend-smb -l pl
Backend CUPS-a drukuj╠cy na drukarkach SMB.

%package vfs-audit
Summary:        VFS module to audit file access
Summary(pl):    ModuЁ VFS do monitorowania operacji na plikach
Group:          Networking/Daemons
Requires:       samba-client = %{version}

%description vfs-audit
A simple module to audit file access to the syslog facility.  The following
operations are logged: share connect/disconnect, directory opens/create/remove,
file open/close/rename/unlink/chmod.

%description vfs-audit -l pl
Prosty moduЁ do monitorowania dostЙpu do plikСw do sysloga. Monitorowane s╠
nastЙpuj╠ce operacje: podЁ╠czone/odЁ╠czenie do zasobu,
otwarcie/utworzenie/zmiana nazwy katalogu, otwarcie/zamknЙcie/zmiana
nazwy/skasowania/zmiana praw plikСw.

%package vfs-block
Summary:        VFS module to block access to files
Summary(pl):    ModuЁy VFS do blokowania dostЙpu do plikСw
Group:          Networking/Daemons
Requires:       samba-client = %{version}

%description vfs-block
Sample module by Ronald Kuetemeier <ronald@kuetemeier.com> to block named
symbolic link following.  Note: Config file is in /etc/samba/samba-block.conf

%description vfs-block -l pl
PrzykЁadowy moduЁ stworzony przez Ronald Kuetemeier <ronald@kuetemeier.com> do
blokowania dostЙpu do plikСw wskazywanych przez linki symboliczne. Plik
konfiguracyjny w /etc/samba/samba-block.conf

%package vfs-recycle
Summary:        VFS module to add recycle bin facility to a samba share
Summary(pl):    ModuЁ VFS dodaj╠cy mo©liwo╤Ф kosza do zasobu samby
Group:          Networking/Daemons
Requires:       samba-client = %{version}

%description vfs-recycle
VFS module to add recycle bin facility to a samba share

%description vfs-block -l pl
ModuЁ VFS dodaj╠cy mo©liwo╤Ф kosza do zasobu samby

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p2
%patch7 -p1
#%patch8 -p1
#%patch9 -p1
%{?_with_ipv6:%patch10 -p1}
%patch11 -p1
#%patch12 -p1

cd examples/VFS
tar xjf %{SOURCE7}

%build
cd source
%{__autoconf}
%configure \
	--with-acl-support \
	--with-automount \
	--with-libsmbclient \
	--with-lockdir=/var/lock/samba \
	--with-mmap \
	--with-msdfs \
	--with-netatalk \
	--without-smbwrapper \
	--with-pam \
	--with-piddir=/var/run \
	--with-privatedir=%{_libdir} \
	--with-quotas \
	--with-readline \
	--with-smbmount \
	--with-ssl \
	--with-sslinc=%{_prefix} \
	--with-swatdir=%{_datadir}/swat \
	--with-syslog \
	--with-utmp \
	--with-vfs \
	%{?_with_ipv6:--with-ipv6} \
	%{?_with_ldap:--with-ldapsam}

#	--with-acl-support \
mv Makefile Makefile.old
sed -e "s#-symbolic##g" Makefile.old > Makefile

%{__make} everything pam_smbpass

cd ../examples/VFS
%{__autoconf}
%configure
%{__make}
mv README{,.vfs}

cd samba-vscan-%{vscan_version}
# note - kaspersky mks don't compile yet
for i in fprot icap openantivirus sophos trend; do
cd $i;
%{__make} "LIBTOOL=libtool --tag=CC"
cd ..
done;

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d,security,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/{var/{lock,log,log/archiv,spool},home/services,%{_reallibdir}}/%{name} \
	$RPM_BUILD_ROOT/{sbin,lib/security,%{_libdir},%{_includedir}}

cd source
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install script/mksmbpasswd.sh /$RPM_BUILD_ROOT%{_sbindir}
cd ..

ln -sf %{_bindir}/smbmount $RPM_BUILD_ROOT/sbin/mount.smbfs

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smb
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/samba
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/swat
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/samba
install %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/samba
install %{SOURCE6} $RPM_BUILD_ROOT%{_libdir}/smb.conf

install source/nsswitch/libnss_winbind.so	$RPM_BUILD_ROOT/lib/libnss_winbind.so.2
install source/nsswitch/pam_winbind.so	$RPM_BUILD_ROOT/lib/security/
install source/bin/pam_smbpass.so	$RPM_BUILD_ROOT/lib/security/
install source/bin/wbinfo		$RPM_BUILD_ROOT%{_bindir}

install source/bin/libsmbclient.so $RPM_BUILD_ROOT/lib/libsmbclient.so.0
ln -s libsmbclient.so.0 $RPM_BUILD_ROOT/lib/libsmbclient.so

install source/include/libsmbclient.h $RPM_BUILD_ROOT%{_includedir}

install examples/VFS/{*.so,block/*.so,recycle/*.so} $RPM_BUILD_ROOT/%{_reallibdir}/%{name}
install examples/VFS/block/samba-block.conf examples/VFS/recycle/recycle.conf  $RPM_BUILD_ROOT/%{_sysconfdir}

touch $RPM_BUILD_ROOT/var/lock/samba/{STATUS..LCK,wins.dat,browse.dat}

echo 127.0.0.1 localhost > $RPM_BUILD_ROOT%{_libdir}/lmhosts

%if 0%{!?_without_cups:1}
install -d $RPM_BUILD_ROOT%{cups_serverbin}/backend
ln -s %{_bindir}/smbspool $RPM_BUILD_ROOT%{cups_serverbin}/backend/smb
%endif

> $RPM_BUILD_ROOT%{_libdir}/smbusers
> $RPM_BUILD_ROOT/etc/security/blacklist.samba

rm -f docs/faq/*.{sgml,txt}
rm -f docs/htmldocs/*.[0-9].html

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smb
if [ -r /var/lock/subsys/smb ]; then
	/etc/rc.d/init.d/smb restart >&2
else
	echo "Run \"/etc/rc.d/init.d/smb start\" to start Samba daemons."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/smb ]; then
		/etc/rc.d/init.d/smb stop >&2
	fi
	/sbin/chkconfig --del smb
fi

%post -n swat
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun -n swat
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%triggerpostun -- samba < 1.9.18p7
if [ "$1" != "0" ]; then
	/sbin/chkconfig --add smb
fi

%triggerpostun -- samba < 2.0.5a-3
if [ "$1" != "0" ]; then
	[ ! -d /var/lock/samba ] && mkdir -m 0755 /var/lock/samba
	[ ! -d /var/spool/samba ] && mkdir -m 1777 /var/spool/samba
fi

%files
%defattr(644,root,root,755)
%doc source/nsswitch/README examples/VFS/README.vfs
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/smbd
%attr(755,root,root) %{_sbindir}/winbindd
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_bindir}/smbpasswd
%attr(755,root,root) %{_bindir}/smbcontrol
%attr(755,root,root) %{_bindir}/tdbbackup

%attr(755,root,root) /lib/libnss_*
%attr(755,root,root) /lib/security/pam_winbind.so

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_libdir}/smbusers
%attr(754,root,root) /etc/rc.d/init.d/smb
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/samba
%attr(640,root,root) /etc/logrotate.d/samba
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/samba
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.samba
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/winbindd.8*

%dir /home/services/samba
%dir /var/lock/samba
%ghost /var/lock/samba/*

%attr(0750,root,root) %dir /var/log/samba
%attr(0750,root,root) %dir /var/log/archiv/samba
%attr(1777,root,root) %dir /var/spool/samba

%files client
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/mount.smbfs
%attr(755,root,root) %{_bindir}/smbmount
%attr(755,root,root) %{_bindir}/smbmnt
%attr(755,root,root) %{_bindir}/smbumount
%{_mandir}/man8/smbmnt.8*
%{_mandir}/man8/smbmount.8*
%{_mandir}/man8/smbumount.8*
%attr(755,root,root) %{_bindir}/nmblookup
%attr(755,root,root) %{_bindir}/smbclient
%attr(755,root,root) %{_bindir}/smbtar
%attr(755,root,root) %{_bindir}/smbcacls
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbsh.1*
%attr(755,root,root) %{_bindir}/rpcclient
%{_mandir}/man1/rpcclient.1*
%attr(755,root,root) %{_bindir}/wbinfo
%{_mandir}/man1/wbinfo.1*
%attr(755,root,root) %{_bindir}/findsmb
%{_mandir}/man1/findsmb.1*

%files common
%defattr(644,root,root,755)
%doc README Manifest WHATSNEW.txt
%doc Roadmap docs/faq docs/Registry/*
%doc docs/textdocs/* docs/htmldocs/*.* docs/{history,announce,THANKS}
%dir %{_libdir}
%config(noreplace) %verify(not size mtime md5) %{_libdir}/smb.conf
%config(noreplace) %verify(not size mtime md5) %{_libdir}/lmhosts
%attr(755,root,root) %{_bindir}/make_smbcodepage
%attr(755,root,root) %{_bindir}/make_unicodemap
%attr(755,root,root) %{_bindir}/testparm
%attr(755,root,root) %{_bindir}/testprns
%attr(755,root,root) %{_bindir}/make_printerdef
%{_libdir}/codepages
%{_mandir}/man1/make_smbcodepage.1*
%{_mandir}/man1/make_unicodemap.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man1/testprns.1*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/lmhosts.5*

%files -n swat
%defattr(644,root,root,755)
%doc swat/README* swat/help/*
%attr(755,root,root) %{_sbindir}/swat
%{_datadir}/swat
%{_mandir}/man8/swat.8*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/swat

%files -n pam-pam_smbpass
%defattr(644,root,root,755)
%doc source/pam_smbpass/{CHAN*,README,TODO} source/pam_smbpass/samples
%attr(755,root,root) /lib/security/pam_smbpass.so

%files -n libsmbclient
%defattr(644,root,root,755)
%attr(755,root,root) /lib/libsmbclient.so.*

%files -n libsmbclient-devel
%defattr(644,root,root,755)
%{_includedir}/libsmbclient.h
%attr(755,root,root) /lib/libsmbclient.so

%if 0%{!?_without_cups:1}
%files -n cups-backend-smb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smbspool
%attr(755,root,root) %{cups_serverbin}/backend/smb
%{_mandir}/man8/smbspool.8*
%endif

%files vfs-block
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba-block.conf
%attr(755,root,root) %{_reallibdir}/%{name}/block.so

%files vfs-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{_reallibdir}/%{name}/audit.so

%files vfs-recycle
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/recycle.conf
%attr(755,root,root) %{_reallibdir}/%{name}/recycle.so
%doc examples/VFS/recycle/README
