#
# TODO:
# - fix Summary and Description for python-samba package
# - look into other distro specs for valid %descriptions for samba 3
# - review configure options
# - fix broken --without ldap, test functionality with other bconds
# - new package with McAfee vscan - I dunno what to do with daemon
#
# Conditional build:
%bcond_without	cups		# without CUPS support
%bcond_without	mysql		# without MySQL support
%bcond_with	ldapsam		# with LDAP SAM 2.2 based auth (instead of smbpasswd)
#%bcond_with	ipv6		# with IPv6 support
%bcond_without	ldap		# without LDAP support
%bcond_without	krb5		# without Kerberos5/Heimdal support
%bcond_without	python		# without python libs/utils
#
%define		vscan_version 0.3.5
Summary:	SMB server
Summary(cs):	Server SMB
Summary(da):	SMB server
Summary(de):	SMB-Server
Summary(es):	El servidor SMB
Summary(fi):	SMB-palvelin
Summary(fr):	Serveur SMB
Summary(it):	Server SMB
Summary(ja):	Samba SMB ¥µ¡¼¥Ð¡¼
Summary(ko):	»ï¹Ù SMB ¼­¹ö
Summary(pl):	Serwer SMB
Summary(pt_BR):	Cliente e servidor SMB
Summary(ru):	SMB ËÌÉÅÎÔ É ÓÅÒ×ÅÒ
Summary(tr):	SMB sunucusu
Summary(uk):	SMB ËÌ¦¤ÎÔ ÔÁ ÓÅÒ×ÅÒ
Summary(zh_CN):	Samba ¿Í»§¶ËºÍ·þÎñÆ÷
Name:		samba
Version:	3.0.7
Release:	1
Epoch:		1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://us1.samba.org/samba/ftp/%{name}-%{version}.tar.gz
# Source0-md5:	5906341429e64214909865a4be92e4ab
Source1:	smb.init
Source2:	%{name}.pamd
Source3:	swat.inetd
Source4:	%{name}.sysconfig
Source5:	%{name}.logrotate
Source6:	smb.conf
Source7:	http://dl.sourceforge.net/openantivirus/%{name}-vscan-%{vscan_version}.tar.bz2
# Source7-md5:	5f173d549014985d681478897135915b
Source8:	winbind.init
Source9:	winbind.sysconfig
Patch0:		%{name}-statfs-workaround.patch
Patch1:		%{name}-lib64.patch
#Patch2:	http://v6web.litech.org/samba/%{name}-2.2.4+IPv6-20020609.diff
Patch3:		%{name}-setup-python.patch
URL:		http://www.samba.org/
BuildRequires:	acl-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_cups:BuildRequires:	cups-devel}
%{?with_krb5:BuildRequires:	heimdal-devel}
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	libxml2-devel
%if %{with mysql}
BuildRequires:	mysql-devel
BuildRequires:	mysql-extras
%endif
BuildRequires:	ncurses-devel >= 5.2
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel > 0.66
BuildRequires:	popt-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	xfsprogs-devel
%{?with_python:BuildRequires:	python-devel}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	logrotate
Requires:	pam >= 0.66
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_vfsdir		%{_libdir}/%{name}/vfs
%define		_sambahome	/home/services/samba
%if %{with cups}
%define		cups_serverbin	%{_libdir}/cups
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
Samba poskytuje server SMB, který lze pou¾ít pro poskytování sí»ových
slu¾eb klientùm SMB (nìkdy nazývaných klienti "LAN mana¾er") vèetnì
klientù rùzných verzí MS Windows, OS/2 a dal¹ích linuxových strojù.
Samba té¾ poskytuje nìkteré klienty SMB, kteøí komplementují vestavìný
souborový systém SMB v Linuxu. Samba pou¾ívá protokoly NetBIOS pøes
TCP/IP (NetBT) a NEpotøebuje protokol NetBEUI (neformátovaný rámec
NetBIOS od spoleènosti Microsoft.

%description -l da
Samba tilbyder en SMB server som kan bruges til at tilbyde netværk
services til SMB (også kaldet "Lan Manager") klienter, incl.
forskellige versioner af MS Windows, OS/2, og andre Linux maskiner.
Samba tilbyder også SMB klienter, som udbygger det indbyggede SMB
filsystem i Linux. Samba benytter NetBIOS over TCP/IP (NetBT)
protocolen og kræver ikke NetBEUI (Microsoft Raw NetBIOS frame)
protokollen.

%description -l de
Samba stellt einen SMB-Server zum Anbieten von Netzwerkdiensten für
SMB-Clients (auch "Lan Manager" genannt) zur Verfügung, darunter
verschiedenen Versionen von MS Windows-, OS/2- und anderen
Linux-Rechnern. Samba enthält außerdem einige SMB-Clients, die das in
Linux integrierte SMB-Dateisystem ergänzen. Samba benutzt
NetBIOS-über-TCP/IP (NetBT)-Protokolle und benötigt KEIN NetBEUI
(Microsoft Raw NetBIOS frame)-Protokoll.

%description -l es
Samba provee un servidor SMB que se puede usar para ofrecer servicios
de red a clientes SMB (algunas veces se le llama de "Lan Manager"),
incluyendo varias versiones de MS Windows, OS/2, y otras máquinas
Linux. Samba también ofrece algunos clientes SMB, que complementan el
sistema de archivos SMB de Linux. Samba usa el protocolo NetBIOS sobre
TCP/IP (NetBT) y no necesita del protocolo NetBEUI (Microsoft Raw
NetBIOS frame).

%description -l fi
Samba on SMB-palvelin, jota voidaan käyttää SMB-asiakasohjelmien
verkkopalvelujen tarjoajana. SMB-protokollaa kutsutaan joskus "Lan
Manager" protokollaksi ja asiakasohjelmat toimivat dosissa,
Windowseissa, OS/2:ssa ja toisissa Linux-koneissa. Samban mukana on
myös joitakin SMB-asiakasohjelmia, jotka täydentävät Linuxin
kernelissä olevaa SMB-tiedostojärjestelmän tukea. Samba vaatii NetBIOS
over TCP/IP (NetBT) protokollaa eikä tarvitse tai pysty käyttämään
NetBEUI-protokollaa.

%description -l it
Samba fornisce un server SMB che puo` essere usato per fornire servizi
di rete ai client SMB, incluse le versioni MS Windows, OS/2 e per
altre macchine Linux. Samba fornisce anche i client SMB. Samba usa
NetBIOS sopra TCP/IP e non ha bisogno del protocollo NetBEUI.

%description -l ja
Samba ¤Ï MS Windows ¤ÎÍÍ¡¹¤Ê¥Ð¡¼¥¸¥ç¥ó¡¢OS/2 ¤½¤·¤ÆÂ¾¤Î Linux ¥Þ¥·¥ó
¤ò´Þ¤à SMB (¤¿¤Þ¤Ë "Lan Manager" ¤È¸Æ¤Ð¤ì¤ë)
¥¯¥é¥¤¥¢¥ó¥È¤Ë¥Í¥Ã¥È¥ï¡¼¥¯ ¥µ¡¼¥Ó¥¹¤òÄó¶¡¤¹¤ë¤¿¤á¤Ë»ÈÍÑ¤µ¤ì¤ë SMB
¥µ¡¼¥Ð¤òÄó¶¡¤·¤Þ¤¹¡£Samba ¤Ï NetBIOS over TCP/IP (NetBT)
¥×¥í¥È¥³¥ë¤ò»ÈÍÑ¤·¡¢ NetBEUI(Microsoft Raw NetBIOS frame)
¥×¥í¥È¥³¥ë¤ÏÉ¬Í×¤¢¤ê¤Þ¤»¤ó¡£

Samba ¤Û¤È¤ó¤ÉÆ°ºî¤¹¤ë NT ¥É¥á¥¤¥ó¥³¥ó¥È¥í¡¼¥ë¤Îµ¡Ç½¤òÆÃÄ§¤È¤·¡¢
¹¥¤­¤Ê¥Ö¥é¥¦¥¶¤ò»È¤Ã¤Æ samba ¤Î smb.conf ¥Õ¥¡¥¤¥ë¤ò¥ê¥â¡¼¥È´ÉÍý¤¹¤ë
¿·¤·¤¤ SWAT (Samba Web Administration Tool) ¤ò´Þ¤ß¤Þ¤¹¡£
ÌÜ²¼¤Î¤È¤³¤í¤³¤ì¤Ï inetd ¤òÄÌ¤·¤Æ TCP ¥Ý¡¼¥È 901 ¤ÇÍ­¸ú¤Ë¤Ê¤ê¤Þ¤¹¡£

%description -l ko
»ï¹Ù´Â MS Windows, OS/2, È¤Àº ´Ù¸¥ ¸®´ª½º ¸Ó½ÅÀ» Æ÷ÇÔÇÏ´Â SMB(È¤Àº
"Lan Manager"¶ó°íµµ ºÒ¸²) Å¬¶óÀÌ¾ðÆ®¸¦ ³×Æ®¿öÅ© ¼­ºñ½º À§ÇØ »ç¿ëÇÒ ¼ö
ÀÖ´Â SMB ¼­¹ö¸¦ Á¦°øÇÑ´Ù. »ï¹Ù´Â TCP/IP ÇÁ·ÎÅäÄÝÀ» ÅëÇØ NetBIOS¸¦
»ç¿ëÇÏ°í NetBEUI (Microsoft Raw NetBIOS ÇÁ·¹ÀÓ) ÇÁ·ÎÅäÄÝÀº ÇÊ¿äÇÏÁö
¾Ê´Ù.

»ï¹Ù-2.2 ÀÇ Æ¯Â¡Àº NT µµ¸ÞÀÎ ÄÁÆ®·ÑÀÇ ¼º´ÉÀ¸·Î ÀÛ¾÷À» ÇÏ°í, »õ·Î¿î
SWAT(Samba Web Administration Tool)·Î À¥ºê¶ó¿ìÀú¸¦ »ç¿ëÇÏ¿© ¿ø°ÝÁö¿¡¼­
»ï¹ÙÀÇ smb.conf ÆÄÀÏÀ» °ü¸®ÇÏµµ·Ï ÇÑ´Ù. ÀÌ·¯ÇÑ °æ¿ì inetd µ¥¸óÀ» ÅëÇØ
TCP 901 Æ÷Æ®¸¦ »ç¿ëÇÏ°Ô µÈ´Ù.

ÃÖ±Ù Á¤º¸·Î WHATSNEW.txt ÆÄÀÏÀÇ ¹®¼­¸¦ Âü°íÇÏµµ·Ï ÇÑ´Ù. ¹ÙÀÌ³Ê¸®ÀÇ
¸±¸®Áî´Â ¾ÏÈ£È­µÈ ÆÐ½º¿öµå¸¦ Á¦°øÇÑ´Ù. ±¸Çö¿¡ ´ëÇÑ ÀÚ¼¼ÇÑ Á¤º¸¸¦ ¾ò±â
À§ÇØ docs µð·ºÅä¸®³»¿¡ ÀÖ´Â smb.conf ÆÄÀÏ°ú ENCRYPTION.txt ÆÄÀÏÀ»
ÀÐ¾îº»´Ù.

%description -l pl
Samba udostêpnia serwer SMB, który mo¿e byæ u¿yty w celu dostarczenia
us³ug sieciowych (potocznie zwanych "Lan Manager"), dla klientów
takich jak MS Windows, OS/2 a tak¿e maszyn linuksowych. W pakiecie
znajduje siê równie¿ oprogramowanie klienckie. Samba u¿ywa protoko³u
NetBIOS po TCP/IP (NetBT) i nie wymaga protoko³u NetBEUI. Ta wersja ma
pe³ne wsparcie dla blokowania plików, a tak¿e wsparcie dla kodowania
hase³ w standardzie MS i zarz±dzania baz± WINS.

%description -l pt_BR
O Samba provê um servidor SMB que pode ser usado para oferecer
serviços de rede a clientes SMB (algumas vezes chamado de "Lan
Manager"), incluindo várias versões de MS Windows, OS/2, e outras
máquinas Linux. O Samba também fornece alguns clientes SMB, que
complementam o sistema de arquivos SMB do Linux. O Samba usa o
protocolo NetBIOS sobre TCP/IP (NetBT) e não necessita do protocolo
NetBEUI (Microsoft Raw NetBIOS frame).

O Samba inclui a maioria das características de um servidor de
Controle de Domínios NT e o SWAT (Samba Web Administration Tool), que
permite que o arquivo smb.conf seja gerenciado remotamente através de
um navegador. Atualmente isto está sendo habilitado na porta TCP 901
via inetd.

%description -l ru
Samba ÐÒÅÄÏÓÔÁ×ÌÑÅÔ SMB-ÓÅÒ×ÅÒ, ËÏÔÏÒÙÊ ÍÏÖÅÔ ÂÙÔØ ÉÓÐÏÌØÚÏ×ÁÎ ÄÌÑ
ÐÒÅÄÏÓÔÁ×ÌÅÎÉÑ ÓÅÔÅ×ÙÈ ÓÅÒ×ÉÓÏ× SMB (ÉÎÏÇÄÁ ÎÁÚÙ×ÁÅÍÙÍ "Lan Manager")
ËÌÉÅÎÔÁÍ, ×ËÌÀÞÁÑ ÒÁÚÎÏÏÂÒÁÚÎÙÅ ×ÅÒÓÉÉ MS Windows, OS/2, É ÄÒÕÇÉÅ
Linux-ÍÁÛÉÎÙ. Samba ÔÁËÖÅ ÐÒÅÄÏÓÔÁ×ÌÑÅÔ SMB-ËÌÉÅÎÔÏ×, ËÏÔÏÒÙÅ ÒÁÂÏÔÁÀÔ
ÓÏ ×ÓÔÒÏÅÎÎÏÊ × Linux ÆÁÊÌÏ×ÏÊ ÓÉÓÔÅÍÏÊ SMB.

Samba ÉÓÐÏÌØÚÕÅÔ ÐÒÏÔÏËÏÌ NetBIOS over TCP/IP (NetBT) É ÎÅ ÎÕÖÄÁÅÔÓÑ ×
ÐÒÏÔÏËÏÌÅ NetBEUI (Microsoft Raw NetBIOS frame).

Samba ÓÏÄÅÒÖÉÔ ÐÒÁËÔÉÞÅÓËÉ ÒÁÂÏÔÁÀÝÕÀ ÒÅÁÌÉÚÁÃÉÀ NT Domain Control É
×ËÌÀÞÁÅÔ ÎÏ×ÙÊ SWAT (Samba Web Administration Tool), ËÏÔÏÒÙÊ ÐÏÚ×ÏÌÑÅÔ
ÕÄÁÌÅÎÎÏ ÕÐÒÁ×ÌÑÔØ ËÏÎÆÉÇÕÒÁÃÉÏÎÎÙÍ ÆÁÊÌÏÍ smb.conf ÐÒÉ ÐÏÍÏÝÉ ×ÁÛÅÇÏ
ÌÀÂÉÍÏÇÏ WEB-ÂÒÏÕÚÅÒÁ. ðÏËÁ ÞÔÏ ÏÎ ÒÁÚÒÅÛÅÎ ÞÅÒÅÚ inetd ÎÁ TCP-ÐÏÒÔÕ
901.

%description -l uk
Samba ÎÁÄÁ¤ SMB-ÓÅÒ×ÅÒ, ÝÏ ÍÏÖÅ ÂÕÔÉ ×ÉËÏÒÉÓÔÁÎÉÊ ÄÌÑ ÎÁÄÁÎÎÑ
ÍÅÒÅÖÅ×ÉÈ ÓÅÒ×¦Ó¦× SMB (ÝÏ §È ¦ÎÏÄ¦ ÎÁÚÉ×ÁÀÔØ "Lan Manager") ËÌ¦¤ÎÔÁÍ,
×ËÌÀÞÁÀÞÉ Ò¦ÚÎÏÍÁÎ¦ÔÎ¦ ×ÅÒÓ¦§ MS Windows, OS/2, ÔÁ ¦ÎÛ¦ Linux-ÍÁÛÉÎÉ.
Samba ÔÁËÏÖ ÎÁÄÁ¤ SMB-ËÌ¦¤ÎÔ¦×, ÝÏ ÐÒÁÃÀÀÔØ Ú ×ÂÕÄÏ×ÁÎÏÀ × Linux
ÆÁÊÌÏ×ÏÀ ÓÉÓÔÅÍÏÀ SMB.

Samba ×ÉËÏÒÉÓÔÏ×Õ¤ ÐÒÏÔÏËÏÌ NetBIOS over TCP/IP (NetBT) ÔÁ ÎÅ ÐÏÔÒÅÂÕ¤
ÐÒÏÔÏËÏÌÕ NetBEUI (Microsoft Raw NetBIOS frame).

Samba Í¦ÓÔÉÔØ ÍÁÊÖÅ ÐÒÁÃÀÀÞÕ ÒÅÁÌÉÚÁÃ¦À NT Domain Control ÔÁ ÎÏ×ÙÊ
SWAT (Samba Web Administration Tool), ËÏÔÒÉÊ ÄÏÚ×ÏÌÑ¤ ×¦ÄÄÁÌÅÎÏ
ËÅÒÕ×ÁÔÉ ËÏÎÆ¦ÇÕÒÁÃ¦ÊÎÉÍ ÆÁÊÌÏÍ smb.conf ÚÁ ÄÏÐÏÍÏÇÏÀ ×ÁÛÏÇÏ
ÕÌÀÂÌÅÎÏÇÏ WEB-ÂÒÏÕÚÅÒÁ. ðÏËÉ ÝÏ ×¦Î ÄÏÚ×ÏÌÅÎÉÊ ÞÅÒÅÚ inetd ÎÁ
TCP-ÐÏÒÔÕ 901.

%package swat
Summary:	Samba Web Administration Tool
Summary(es):	Samba SWAT and Web documentation
Summary(pl):	Narzêdzie administracyjne serwisu Samba
Summary(pt_BR):	Samba SWAT e documentação Web
Summary(ru):	ðÒÏÇÒÁÍÍÁ ËÏÎÆÉÇÕÒÁÃÉÉ SMB-ÓÅÒ×ÅÒÁ Samba
Summary(uk):	ðÒÏÇÒÁÍÁ ËÏÎÆÉÇÕÒÁÃ¦§ SMB-ÓÅÒ×ÅÒÁ Samba
Group:		Networking/Admin
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	inetdaemon
Requires:	rc-inetd >= 0.8.2
Obsoletes:	swat

%description swat
swat allows a Samba administrator to configure the complex smb.conf
file via a Web browser. In addition, a swat configuration page has
help links to all the configurable options in the smb.conf file
allowing an administrator to easily look up the effects of any change.

%description swat -l pl
swat pozwala na kompleksow± konfiguracjê smb.conf przy pomocy
przegl±darki WWW.

%description swat -l pt_BR
SWAT - ferramentada Web de configuração do Samba.

%description swat -l ru
ðÁËÅÔ samba-swat ×ËÌÀÞÁÅÔ ÎÏ×ÙÊ SWAT (Samba Web Administration Tool),
ÄÌÑ ÕÄÁÌÅÎÎÏÇÏ ÁÄÍÉÎÉÓÔÒÉÒÏ×ÁÎÉÑ ÆÁÊÌÁ smb.conf ÐÒÉ ÐÏÍÏÝÉ ×ÁÛÅÇÏ
ÌÀÂÉÍÏÇÏ Web-ÂÒÁÕÚÅÒÁ.

%description swat -l uk
ðÁËÅÔ samba-swat Í¦ÓÔÉÔØ ÎÏ×ÉÊ SWAT (Samba Web Administration Tool),
ÄÌÑ ÄÉÓÔÁÎÃ¦ÊÎÏÇÏ ÁÄÍ¦Î¦ÓÔÒÕ×ÁÎÎÑ ÆÁÊÌÕ smb.conf ÚÁ ÄÏÐÏÍÏÇÏÀ ×ÁÛÏÇÏ
ÕÌÀÂÌÅÎÏÇÏ Web-ÂÒÁÕÚÅÒÕ.

%package pdb-mysql
Summary:	Samba MySQL password database plugin
Summary(pl):	Wtyczka Samby do przechowywania hase³ w bazie MySQL
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description pdb-mysql
Samba MySQL password database plugin.

%description pdb-mysql -l pl
Wtyczka Samby do przechowywania hase³ w bazie MySQL.

%package pdb-xml
Summary:	Samba XML password database plugin
Summary(pl):	Wtyczka Samby do przechowywania hase³ w bazie XML
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description pdb-xml
Samba XML password database plugin.

%description pdb-xml -l pl
Wtyczka Samby do przechowywania hase³ w bazie XML.

%package client
Summary:	Samba client programs
Summary(es):	Cliente SMB de Samba
Summary(ja):	Samba (SMB) ¥¯¥é¥¤¥¢¥ó¥È¥×¥í¥°¥é¥à
Summary(pl):	Klienci serwera Samba
Summary(pt_BR):	Cliente SMB do samba
Summary(ru):	ëÌÉÅÎÔÓËÉÅ ÐÒÏÇÒÁÍÍÙ Samba (SMB)
Summary(uk):	ëÌ¦¤ÎÔÓØË¦ ÐÒÏÇÒÁÍÉ Samba (SMB)
Group:		Applications/Networking
Requires:	samba-common = %{epoch}:%{version}-%{release}
Obsoletes:	smbfs
Obsoletes:	mount-cifs

%description client
Samba-client provides some SMB clients, which complement the build-in
SMB filesystem in Linux. These allow accessing of SMB shares and
printing to SMB printers.

%description client -l pt_BR
O pacote samba-clientes prove alguns clientes SMB, que complementam o
sistema de arquivos SMB do Linux. Eles permitem o acesso a shares SMB,
e também, à impressoras SMB.

%description client -l es
Cliente SMB de Samba.

%description client -l ja
Samba-client ¤Ï Linux ¾å¤Ë´Þ¤Þ¤ì¤Æ¤¤¤ë SMB ¥Õ¥¡¥¤¥ë¥·¥¹¥Æ¥à¤òÊä¤¦ SMB
¥¯¥é¥¤¥¢¥ó¥È¤òÄó¶¡¤·¤Þ¤¹¡£¤³¤ì¤é¤Ï SMB ¶¦Í­¤Î¥¢¥¯¥»¥¹¤È SMB
¥×¥ê¥ó¥¿¤Ø¤Î°õºþ¤òµö²Ä¤·¤Þ¤¹¡£

%description client -l pl
Samba-client dostarcza programy uzupe³niaj±ce obs³ugê systemu plików
SMB zawart± w j±drze. Pozwalaj± one na wspó³dzielenie zasobów SMB i
drukowanie w sieci SMB.

%description client -l pt_BR
O pacote samba-clientes prove alguns clientes SMB, que complementam o
sistema de arquivos SMB do Linux. Eles permitem o acesso a shares SMB,
e também, à impressoras SMB.

%description client -l ru
ðÁËÅÔ samba-client ÐÒÅÄÏÓÔÁ×ÌÑÅÔ ÎÅËÏÔÏÒÙÅ ËÌÉÅÎÔÙ SMB ÄÌÑ ÒÁÂÏÔÙ ÓÏ
×ÓÔÒÏÅÎÎÏÊ ÆÁÊÌÏ×ÏÊ ÓÉÓÔÅÍÏÊ SMB × Linux. üÔÉ ËÌÉÅÎÔÙ ÐÏÚ×ÏÌÑÀÔ
ÐÏÌÕÞÁÔØ ÄÏÓÔÕÐ Ë ÒÁÚÄÅÌÑÅÍÙÍ ËÁÔÁÌÏÇÁÍ SMB É ÐÅÞÁÔØ ÎÁ SMB-ÐÒÉÎÔÅÒÙ.

%description client -l uk
ðÁËÅÔ samba-client ÎÁÄÁ¤ ÄÅÑË¦ ËÌ¦¤ÎÔÉ SMB ÄÌÑ ÒÏÂÏÔÉ Ú¦ ×ÂÕÄÏ×ÁÎÏÀ
ÆÁÊÌÏ×ÏÀ ÓÉÓÔÅÍÏÀ SMB × Linux. ã¦ ËÌ¦¤ÎÔÉ ÄÏÚ×ÏÌÑÀÔØ ÏÔÒÉÍÕ×ÁÔÉ ÄÏÓÔÕÐ
ÄÏ ËÁÔÁÌÏÇ¦× ÓÐ¦ÌØÎÏÇÏ ×ÉËÏÒÉÓÔÁÎÎÑ SMB ÔÁ ÄÒÕË ÎÁ SMB-ÐÒ¦ÎÔÅÒÉ.

%package common
Summary:	Files used by both Samba servers and clients
Summary(es):	Common files between samba and samba-clients
Summary(ja):	Samba ¥µ¡¼¥Ð¡¼¤È¥¯¥é¥¤¥¢¥ó¥È¤Ç»ÈÍÑ¤µ¤ì¤ë¥×¥í¥°¥é¥à
Summary(pl):	Pliki u¿ywane przez serwer i klientów Samba
Summary(pt_BR):	Arquivos em comum entre samba e samba-clients
Summary(ru):	æÁÊÌÙ, ÉÓÐÏÌØÚÕÅÍÙÅ ËÁË ÓÅÒ×ÅÒÏÍ, ÔÁË É ËÌÉÅÎÔÏÍ Samba
Summary(uk):	æÁÊÌÉ, ÝÏ ×ÉËÏÒÉÓÔÏ×ÕÀÔØÓÑ ÑË ÓÅÒ×ÅÒÏÍ, ÔÁË ¦ ËÌ¦¤ÎÔÏÍ Samba
Group:		Networking/Daemons

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description common -l ja
Samba-common ¤Ï Samba ¤Î¥µ¡¼¥Ð¤È¥¯¥é¥¤¥¢¥ó¥È¤ÎÎ¾Êý¤Î¥Ñ¥Ã¥±¡¼¥¸¤Ç
»ÈÍÑ¤µ¤ì¤ë¥Õ¥¡¥¤¥ë¤òÄó¶¡¤·¤Þ¤¹¡£

%description common -l pl
Samba-common dostarcza pliki niezbêdne zarówno dla serwera jak i
klientów Samba.

%description common -l pt_BR
Arquivos em comum entre os pacotes samba e samba-clients.

%description common -l ru
Samba-common ÓÏÄÅÒÖÉÔ ÆÁÊÌÙ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ ÒÁÂÏÔÙ ËÁË ËÌÉÅÎÔÁ, ÔÁË É
ÓÅÒ×ÅÒÁ Samba.

%description common -l uk
Samba-common Í¦ÓÔÉÔØ ÆÁÊÌÉ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ ÒÏÂÏÔÉ ÑË ËÌ¦¤ÎÔÁ, ÔÁË ¦
ÓÅÒ×ÅÒÁ Samba.

%package winbind
Summary:	Samba-winbind daemon, utilities and documentation
Summary(pl):	Demon samba-winbind, narzêdzia i dokumentacja
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description winbind
Provides the winbind daemon and testing tools to allow authentication
and group/user enumeration from a Windows or Samba domain controller.

%description winbind -l pl
Pakiet zawiera demona winbind oraz narzêdzia testowe. Umo¿liwia
uwierzytelnianie i wyliczanie grup/u¿ytkowników z kontrolera domeny
Windows lub Samba.

%package -n nss_wins
Summary:	Name Service Switch service for WINS
Summary(pl):	Us³uga Name Service Switch dla WINS
Group:		Base
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names
to IP addresses.

%description -n nss_wins -l pl
Biblioteka dzielona libnss_wins rozwi±zuj±ca nazwy NetBIOS na adresy
IP.

%package -n pam-pam_smbpass
Summary:	PAM Samba Password Module
Summary(pl):	Modu³ PAM smbpass
Group:		Base
Obsoletes:	pam_smbpass

%description -n pam-pam_smbpass
PAM module which can be used on conforming systems to keep the
smbpasswd (Samba password) database in sync with the unix password
file.

%description -n pam-pam_smbpass -l pl
Modu³ PAM, który mo¿e byæ u¿ywany do trzymania pliku smbpasswd (has³a
Samby) zsynchronizowanego z has³ami unixowymi.

%package -n libsmbclient
Summary:	libsmbclient - samba client library
Summary(pl):	libsmbclient - biblioteka klienta samby
Group:		Libraries

%description -n libsmbclient
libsmbclient - library that allows to use samba clients functions.

%description -n libsmbclient -l pl
libsmbclient - biblioteka pozwalaj±ca korzystaæ z funcji klienta
samby.

%package -n libsmbclient-devel
Summary:	libsmbclient - samba client library
Summary(pl):	libsmbclient - biblioteka klienta samby
Summary(pt_BR):	Ferramentas de desenvolvimento para clientes samba
Group:		Development/Libraries
Requires:	libsmbclient = %{epoch}:%{version}-%{release}

%description -n libsmbclient-devel
Header files for libsmbclient.

%description -n libsmbclient-devel -l pl
Pliki nag³ówkowe dla libsmbclient.

%description -n libsmbclient-devel -l pt_BR
Arquivos de inclusão, bibliotecas e documentação necessários para
desenvolver aplicativos clientes para o samba.

%package -n libsmbclient-static
Summary:	Static version of libsmbclient - samba client library
Summary(pl):	Statyczna wersja libsmbclient - biblioteki klienta samby
Summary(pt_BR):	Ferramentas de desenvolvimento para clientes samba
Group:		Development/Libraries
Requires:	libsmbclient = %{epoch}:%{version}-%{release}

%description -n libsmbclient-static
Static libsmbclient library.

%description -n libsmbclient-static -l pl
Statyczna biblioteka libsmbclient.

%package -n smbget
Summary:	A utility for retrieving files using the SMB protocol
Summary(pl):	Narzêdzie do pobierania plików protoko³em SMB
Group:		Applications/Networking

%description -n smbget
wget-like utility for download files over SMB.

%description -n smbget -l pl
Narzêdzie podobne do wgeta do pobierania plików protoko³em SMB
u¿ywanym w sieciach MS Windows.

%package -n cups-backend-smb
Summary:	CUPS backend for printing to SMB printers
Summary(pl):	Backend CUPS-a drukuj±cy na drukarkach SMB
Group:		Applications/Printing
Requires:	%{name}-client = %{epoch}:%{version}-%{release}
Requires:	cups

%description -n cups-backend-smb
CUPS backend for printing to SMB printers.

%description -n cups-backend-smb -l pl
Backend CUPS-a drukuj±cy na drukarkach SMB.

%package -n python-samba
Summary:	Samba python tools and libraries
Summary(pl):	Narzêdzia i biblioteki pythona do samby
Group:		Applications/Networking

%description -n python-samba
Samba python tools and libraries.

%description -n python-samba -l pl
Narzêdzia i biblioteki pythona do samby.

%package vfs-audit
Summary:	VFS module to audit file access
Summary(pl):	Modu³ VFS do monitorowania operacji na plikach
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-audit
A simple module to audit file access to the syslog facility. The
following operations are logged: share connect/disconnect, directory
opens/create/remove, file open/close/rename/unlink/chmod.

%description vfs-audit -l pl
Prosty modu³ do monitorowania dostêpu do plików do sysloga.
Monitorowane s± nastêpuj±ce operacje: pod³±czone/od³±czenie do zasobu,
otwarcie/utworzenie/zmiana nazwy katalogu, otwarcie/zamknêcie/zmiana
nazwy/skasowania/zmiana praw plików.

%package vfs-cap
Summary:	VFS module for CAP and samba compatibility
Summary(pl):	Modu³ VFS zgodno¶ci z CAP (Columbia AppleTalk Program)
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-cap
Convert an incoming Shift-JIS character to the 3 byte hex
representation used by the Columbia AppleTalk Program (CAP), i.e. :AB.
This is used for compatibility between Samba and CAP.

%description vfs-cap -l pl
Zamienia znaki kodowane Shift-JIS do trzybajowej szestnastkowej
reprezentacji u¿ywanej przez program Columbia AppleTalk Program (CAP).

%package vfs-default_quota
Summary:	VFS module to store default quotas in a specified quota record
Summary(pl):	Modu³ VFS do zapisywania domy¶lnych limitów w okre¶lonym rekordzie
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-default_quota
This VFS modules stores default quotas in a specified quota record.

%description vfs-default_quota -l pl
Ten modu³ VFS zapisuje domy¶lne limity (quoty) w okre¶lonym rekordzie
limitów.

%package vfs-expand_msdfs
Summary:	VFS module for hosting a Microsoft Distributed File System Tree
Summary(pl):	Modu³ VFS obs³ugi Microsoft Distributed File System
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-expand_msdfs
A VFS module for hosting a Microsoft Distributed File System Tree.

The Distributed File System (DFS) provides a means of separating the
logical view of files and directories that users see from the actual
physical locations of these resources on the network. It allows for
higher availability, smoother storage expansion, load balancing, and
so on.

%description vfs-expand_msdfs -l pl
Modu³ VFS do udostêpniania drzewa systemu plików Microsoft Distributed
File System.

Distributed File System (DFS) umo¿liwia rozdzielanie logicznego widoku
plików i katalogów widocznych przez u¿ytkowników z fizycznego
umiejscowienia tych zasobów w sieci. Pozwala to na wy¿sz± dostêpno¶æ,
p³ynniejsze powiêkszanie przestrzeni, rozdzielanie obci±¿enia itp.

%package vfs-fake_perms
Summary:	VFS module to report read-only fires as writable
Summary(pl):	Modu³ VFS udaj±cy, ¿e pliki tylko do odczytu s± zapisywalne
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-fake_perms
This module allow Roaming Profile files and directories to be set (on
the Samba server under UNIX) as read only. This module will, if
installed on the Profiles share, report to the client that the Profile
files and directories are writeable. This satisfies the client even
though the files will never be overwritten as the client logs out or
shuts down.

%description vfs-fake_perms -l pl
Ten modu³ pozwala na ustawienie plików i katalogów z wêdruj±cych
profili (Roaming Profiles) jako tylko do odczytu. Modu³ ten w
przypadku zainstalowania na udziale z profilami bêdzie zg³asza³
klientom, ¿e pliki i katalogi z profilu s± zapisywane. To wystarczy
klientom pomimo, ¿e pliki nie zostan± nigdy nadpisane przy logowaniu
lub wylogowywaniu klienta.

%package vfs-netatalk
Summary:	VFS module for ease co-existence of samba and netatalk
Summary(pl):	Modu³ VFS u³atwiaj±cy wspó³pracê serwisów samba i netatalk
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-netatalk
Package contains a netatalk VFS module for ease co-existence of Samba
and netatalk file sharing services.

%description vfs-netatalk -l pl
Pakiet zawiera modu³ VFS netatalk umo¿liwiaj±cy wspó³pracê us³ug samba
i netatalk przy udostêpnianiu zasobów.

%package vfs-recycle
Summary:	VFS module to add recycle bin facility to a samba share
Summary(pl):	Modu³ VFS dodaj±cy mo¿liwo¶æ kosza do zasobu samby
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-recycle
VFS module to add recycle bin facility to a samba share.

%description vfs-recycle -l pl
Modu³ VFS dodaj±cy mo¿liwo¶æ kosza do zasobu samby.

%package vfs-readonly
Summary:	VFS module for read-only limitation for specified share
Summary(pl):	Modu³ VFS do ograniczania okre¶lonego udzia³u tylko do odczytu
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-readonly
This module performs a read-only limitation for specified share (or
all of them if it is loaded in a [global] section) based on period
definition in smb.conf.

%description vfs-readonly -l pl
Ten modu³ wprowadza ograniczenie tylko do odczytu dla okre¶lonego
udzia³u (lub wszystkich, je¶li jest wczytywany w sekcji [global]) w
oparciu o definicje okresów w smb.conf.

%package vfs-shadow_copy
Summary:	VFS module to make automatic copy of data in samba share
Summary(pl):	Modu³ VFS do tworzenia automatycznych kopii danych w zasobach samby
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-shadow_copy
VFS module to make automatic copy of data in samba share.

%description vfs-shadow_copy -l pl
Modu³ VFS do tworzenia automatycznych kopii danych w zasobach samby.

%package vfs-vscan-clamav
Summary:	On-access virus scanning for samba using ClamAV
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy ClamAV
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	clamav
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}

%description vfs-vscan-clamav
A vfs-module for samba to implement on-access scanning using the
ClamAV antivirus software (which must be installed to use this).

%description vfs-vscan-clamav -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego ClamAV
(które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%package vfs-vscan-fprot
Summary:	On-access virus scanning for samba using FPROT
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy FPROT
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-fprot

%description vfs-vscan-fprot
A vfs-module for samba to implement on-access scanning using the FPROT
antivirus software (which must be installed to use this).

%description vfs-vscan-fprot -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego FPROT
(które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%package vfs-vscan-fsav
Summary:	On-access virus scanning for samba using F-Secure AntiVirus
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy F-Secure AntiVirus
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-fsav

%description vfs-vscan-fsav
A vfs-module for samba to implement on-access scanning using the
F-Secure AntiVirus antivirus software (which must be installed to use
this).

%description vfs-vscan-fsav -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego F-Secure
AntiVirus (które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%package vfs-vscan-kavp
Summary:	On-access virus scanning for samba using Kaspersky AVP
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy Kaspersky AVP
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-kavp

%description vfs-vscan-kavp
A vfs-module for samba to implement on-access scanning using the
Kaspersky AVP antivirus software (which must be installed to use
this).

%description vfs-vscan-kavp -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego
Kaspersky AVP (które musi byæ zainstalowane, aby wykorzystaæ ten
modu³).

%package vfs-vscan-mks
Summary:	On-access virus scanning for samba using mks
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy mks
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	mksd
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-mks

%description vfs-vscan-mks
A vfs-module for samba to implement on-access scanning using the mks
antivirus software (which must be installed to use this).

%description vfs-vscan-mks -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego mks
(które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%package vfs-vscan-openantivirus
Summary:	On-access virus scanning for samba using OpenAntivirus
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy OpenAntiVirus
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-openantivirus

%description vfs-vscan-openantivirus
A vfs-module for samba to implement on-access scanning using the
OpenAntivirus antivirus software (which must be installed to use
this).

%description vfs-vscan-openantivirus -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego
OpenAntiVirus.org (które musi byæ zainstalowane, aby wykorzystaæ ten
modu³).

%package vfs-vscan-sophos
Summary:	On-access virus scanning for samba using Sophos
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy Sophos
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-sophos

%description vfs-vscan-sophos
A vfs-module for samba to implement on-access scanning using the
Sophos antivirus software (which must be installed to use this).

%description vfs-vscan-sophos -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego Sophos
(które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%package vfs-vscan-symantec
Summary:	On-access virus scanning for samba using Symantec
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy Symantec
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-symantec

%description vfs-vscan-symantec
A vfs-module for samba to implement on-access scanning using the
Symantec antivirus software (which must be installed to use this).

%description vfs-vscan-symantec -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego firmy
Symantec (które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%package vfs-vscan-trend
Summary:	On-access virus scanning for samba using Trend
Summary(pl):	Skaner antywirusowy online wykorzystuj±cy Trend
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-vscan = %{epoch}:%{version}-%{release}
Obsoletes:	vscan-trend

%description vfs-vscan-trend
A vfs-module for samba to implement on-access scanning using the Trend
antivirus software (which must be installed to use this).

%description vfs-vscan-trend -l pl
Modu³ vfs do samby implementuj±cy skaning antywirusowy w czasie
dostêpu do plików korzystaj±c z oprogramowania antywirusowego Trend
(które musi byæ zainstalowane, aby wykorzystaæ ten modu³).

%prep
%setup -q
%patch0 -p1
%ifarch amd64
%patch1 -p1
%endif
#%{?with_ipv6:%patch2 -p1}
%patch3 -p1

cd examples/VFS
tar xjf %{SOURCE7}

%build
cd source
%{__libtoolize}
%{__autoconf}

# Removed options (default or not supported by configure script)
#	--with-mmap \
#	--with-netatalk \
#	--without-smbwrapper \
#	--with-sslinc=%{_prefix} \
#	--with-vfs \
#	--with-tdbsam \
#	%{?with_ipv6:--with-ipv6} \

%configure \
	--with-acl-support \
	--with-automount \
	--with-libsmbclient \
	--with-pam \
	--with-pam_smbpass \
	--with%{!?with_ldap:out}-ads \
	--with-privatedir=%{_sysconfdir}/samba \
	--with-quotas \
	--with-readline \
	--with-smbmount \
	--with-swatdir=%{_datadir}/swat \
	--with-syslog \
	--with-utmp \
	--with-fhs \
        %{?with_python:--with-python} \
	--with-expsam=xml,%{?with_mysql:mysql} \
	%{?with_ldapsam:--with-ldapsam} \
	--with%{!?with_ldap:out}-ldap \
	--with%{!?with_krb5:out}-krb5

%{__make} proto
%{__make} everything pam_smbpass bin/smbget client/mount.cifs

cd ../examples/VFS
%{__autoconf}
%configure \
	CFLAGS="%{rpmcflags} -fPIC"
%{__make}
mv README{,.vfs}

cd samba-vscan-%{vscan_version}
cp %{_datadir}/automake/config.sub .
%configure
%{__make} -j1 all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d,security,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/var/{lock,log,log/archiv,spool}/samba \
	$RPM_BUILD_ROOT{/sbin,/%{_lib}/security,%{_libdir},%{_vfsdir},%{_includedir},%{_sambahome}}

cd source
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CONFIGDIR=$RPM_BUILD_ROOT%{_sysconfdir}/samba

install script/mksmbpasswd.sh $RPM_BUILD_ROOT%{_sbindir}
cd ..

ln -sf %{_bindir}/smbmount $RPM_BUILD_ROOT/sbin/mount.smbfs

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smb
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/samba
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/swat
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/samba
install %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/samba
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/samba/smb.conf
install %{SOURCE8} $RPM_BUILD_ROOT/etc/rc.d/init.d/winbind
install %{SOURCE9} $RPM_BUILD_ROOT/etc/sysconfig/winbind

install source/client/mount.cifs	$RPM_BUILD_ROOT/sbin/mount.cifs
install source/nsswitch/libnss_winbind.so $RPM_BUILD_ROOT/%{_lib}/libnss_winbind.so.2
ln -s libnss_winbind.so.2		$RPM_BUILD_ROOT/%{_lib}/libnss_winbind.so
install source/nsswitch/libnss_wins.so	$RPM_BUILD_ROOT/%{_lib}/libnss_wins.so.2
ln -s libnss_wins.so.2			$RPM_BUILD_ROOT/%{_lib}/libnss_wins.so
install source/nsswitch/pam_winbind.so	$RPM_BUILD_ROOT/%{_lib}/security
install source/bin/pam_smbpass.so	$RPM_BUILD_ROOT/%{_lib}/security
install source/bin/wbinfo		$RPM_BUILD_ROOT%{_bindir}
install source/bin/smbget		$RPM_BUILD_ROOT%{_bindir}

mv $RPM_BUILD_ROOT%{_libdir}/samba/libsmbclient.so $RPM_BUILD_ROOT%{_libdir}/libsmbclient.so.0
mv $RPM_BUILD_ROOT%{_libdir}/samba/libsmbclient.a $RPM_BUILD_ROOT%{_libdir}/libsmbclient.a
ln -s libsmbclient.so.0 $RPM_BUILD_ROOT%{_libdir}/libsmbclient.so

install source/include/libsmbclient.h $RPM_BUILD_ROOT%{_includedir}

# vscan modules
install examples/VFS/samba-vscan-%{vscan_version}/*.so $RPM_BUILD_ROOT%{_vfsdir}
install examples/VFS/samba-vscan-%{vscan_version}/{clamav,fprot,icap,kaspersky,mks,openantivirus,sophos,trend,f-secure}/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/samba

touch $RPM_BUILD_ROOT/var/lock/samba/{STATUS..LCK,wins.dat,browse.dat}

echo 127.0.0.1 localhost > $RPM_BUILD_ROOT%{_sysconfdir}/samba/lmhosts

%if %{with cups}
install -d $RPM_BUILD_ROOT%{cups_serverbin}/backend
ln -s %{_bindir}/smbspool $RPM_BUILD_ROOT%{cups_serverbin}/backend/smb
%endif

> $RPM_BUILD_ROOT%{_sysconfdir}/samba/smbusers
> $RPM_BUILD_ROOT/etc/security/blacklist.samba

rm -f docs/faq/*.{sgml,txt}
rm -f docs/htmldocs/*.[0-9].html

# we have this utility in tdb package
rm -f $RPM_BUILD_ROOT{%{_bindir}/tdbdump,%{_mandir}/man8/tdbdump.8*}

# python stuff
%if %{with python}
install -d $RPM_BUILD_ROOT%{py_sitedir}
cp -R source/build/lib.*/samba $RPM_BUILD_ROOT%{py_sitedir}
%endif

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

%post winbind
/sbin/chkconfig --add winbind
if [ -r /var/lock/subsys/winbind ]; then
	/etc/rc.d/init.d/winbind restart >&2
else
	echo "Run \"/etc/rc.d/init.d/winbind start\" to start Winbind daemon."
fi

%preun winbind
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/winbind ]; then
		/etc/rc.d/init.d/winbind stop >&2
	fi
	/sbin/chkconfig --del winbind
fi

%post swat
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun swat
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
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/smbd
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_bindir}/smbpasswd
%attr(755,root,root) %{_bindir}/smbcontrol
%attr(755,root,root) %{_bindir}/tdbbackup

%dir %{_libdir}/%{name}/pdb
%dir %{_vfsdir}

%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/smbusers
%attr(754,root,root) /etc/rc.d/init.d/smb
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/samba
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/samba
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
%{_mandir}/man8/tdbbackup.8*

%dir %{_sambahome}
%dir /var/lock/samba
%ghost /var/lock/samba/*

%attr(0750,root,root) %dir /var/log/samba
%attr(0750,root,root) %dir /var/log/archiv/samba
%attr(1777,root,root) %dir /var/spool/samba
%if %{with ldap}
%doc examples/LDAP
%endif

%if %{with mysql}
%files pdb-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/pdb/mysql.so
%endif

%files pdb-xml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/pdb/xml.so

%files winbind
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/winbindd
%attr(755,root,root) %{_bindir}/wbinfo
%attr(755,root,root) /%{_lib}/security/pam_winbind*
%attr(755,root,root) /%{_lib}/libnss_winbind*
%attr(754,root,root) /etc/rc.d/init.d/winbind
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/winbind
#%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/system-auth-winbind*
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man1/wbinfo*.1*

%files -n nss_wins
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_wins*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/mount.smbfs
%attr(755,root,root) /sbin/mount.cifs
%attr(755,root,root) %{_bindir}/smbmount
%attr(755,root,root) %{_bindir}/smbmnt
%attr(755,root,root) %{_bindir}/smbumount
%attr(755,root,root) %{_bindir}/net
%attr(755,root,root) %{_bindir}/smbtree
%{_mandir}/man8/net.8*
%{_mandir}/man8/smbmnt.8*
%{_mandir}/man8/smbmount.8*
%{_mandir}/man8/smbumount.8*
%{_mandir}/man8/mount.cifs.8*
%attr(755,root,root) %{_bindir}/nmblookup
%attr(755,root,root) %{_bindir}/smbclient
%attr(755,root,root) %{_bindir}/smbtar
%attr(755,root,root) %{_bindir}/smbcacls
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
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
%doc Roadmap docs/*.pdf docs/registry/*
%doc docs/htmldocs/*.* docs/{history,THANKS}
%dir %{_libdir}/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/lmhosts
%{_libdir}/%{name}/*.dat
#%attr(755,root,root) %{_bindir}/make_smbcodepage
#%attr(755,root,root) %{_bindir}/make_unicodemap
%attr(755,root,root) %{_bindir}/testparm
%attr(755,root,root) %{_bindir}/testprns
%attr(755,root,root) %{_bindir}/ntlm_auth
%attr(755,root,root) %{_bindir}/smbcquotas
%attr(755,root,root) %{_bindir}/profiles
%attr(755,root,root) %{_bindir}/pdbedit
#%attr(755,root,root) %{_bindir}/make_printerdef
%dir %{_libdir}/%{name}/charset
%attr(755,root,root) %{_libdir}/%{name}/charset/*.so
#%{_mandir}/man1/make_smbcodepage.1*
#%{_mandir}/man1/make_unicodemap.1*
%{_mandir}/man1/editreg.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man1/testprns.1*
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/vfstest.1*

%{_mandir}/man1/log2pcap.1*

%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/lmhosts.5*

%files swat
%defattr(644,root,root,755)
#%doc swat/README* swat/help/*
%doc swat/help/*
%attr(755,root,root) %{_sbindir}/swat
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/swat
%dir %{_datadir}/swat
%{_datadir}/swat/help
%{_datadir}/swat/images
%{_datadir}/swat/include
%dir %{_datadir}/swat/lang
%lang(ja) %{_datadir}/swat/lang/ja
%lang(tr) %{_datadir}/swat/lang/tr
%{_datadir}/swat/using_samba
%lang(de) %{_libdir}/%{name}/de.msg
%{_libdir}/%{name}/en.msg
%lang(fr) %{_libdir}/%{name}/fr.msg
%lang(it) %{_libdir}/%{name}/it.msg
%lang(ja) %{_libdir}/%{name}/ja.msg
%lang(nl) %{_libdir}/%{name}/nl.msg
%lang(pl) %{_libdir}/%{name}/pl.msg
%lang(tr) %{_libdir}/%{name}/tr.msg
%{_mandir}/man8/swat.8*

%if %{with python}
%files -n python-samba
%defattr(644,root,root,755)
%dir %{py_sitedir}/samba
%attr(755,root,root) %{py_sitedir}/samba/*.so
%{py_sitedir}/samba/*.py
%doc source/python/{README,gprinterdata,gtdbtool,gtkdictbrowser.py}
%doc source/python/examples
%endif

%files -n pam-pam_smbpass
%defattr(644,root,root,755)
%doc source/pam_smbpass/{CHAN*,README,TODO} source/pam_smbpass/samples
%attr(755,root,root) /%{_lib}/security/pam_smbpass.so

%files -n libsmbclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so.*

%files -n libsmbclient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so
%{_includedir}/libsmbclient.h

%files -n libsmbclient-static
%defattr(644,root,root,755)
%{_libdir}/libsmbclient.a

%files -n smbget
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smbget
%{_mandir}/man1/smbget.1*
%{_mandir}/man5/smbgetrc.5*

%if %{with cups}
%files -n cups-backend-smb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smbspool
%attr(755,root,root) %{cups_serverbin}/backend/smb
%{_mandir}/man8/smbspool.8*
%endif

%files vfs-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/audit.so
%attr(755,root,root) %{_vfsdir}/extd_audit.so
%attr(755,root,root) %{_vfsdir}/full_audit.so


%files vfs-cap
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/cap.so

%files vfs-default_quota
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/default_quota.so

%files vfs-expand_msdfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/expand_msdfs.so

%files vfs-fake_perms
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/fake_perms.so

%files vfs-netatalk
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/netatalk.so

%files vfs-readonly
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/readonly.so

%files vfs-recycle
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/recycle.so

%files vfs-shadow_copy
%defattr(644,root,root,755)
%attr(755,root,root) %{_vfsdir}/shadow_copy.so

%files vfs-vscan-clamav
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-clamav.conf
%attr(755,root,root) %{_vfsdir}/vscan-clamav.so

%files vfs-vscan-fprot
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-fprotd.conf
%attr(755,root,root) %{_vfsdir}/vscan-fprotd.so

%files vfs-vscan-fsav
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-fsav.conf
%attr(755,root,root) %{_vfsdir}/vscan-fsav.so

%files vfs-vscan-kavp
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-kavp.conf
%attr(755,root,root) %{_vfsdir}/vscan-kavp.so

%ifarch %{ix86}
%files vfs-vscan-mks
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-mks32.conf
%attr(755,root,root) %{_vfsdir}/vscan-mksd.so
%endif

%files vfs-vscan-openantivirus
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-oav.conf
%attr(755,root,root) %{_vfsdir}/vscan-oav.so

%files vfs-vscan-sophos
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-sophos.conf
%attr(755,root,root) %{_vfsdir}/vscan-sophos.so

%files vfs-vscan-symantec
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-icap.conf
%attr(755,root,root) %{_vfsdir}/vscan-icap.so

%files vfs-vscan-trend
%defattr(644,root,root,755)
#%doc examples/VFS/%{name}-vscan-%{vscan_version}/{INSTALL,FAQ}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/samba/vscan-trend.conf
%attr(755,root,root) %{_vfsdir}/vscan-trend.so
