#
# Conditional build:
# _with_ldap	- with LDAP support
# _with_ipv6    - with IPv6 support
#
Summary:	SMB server
Summary(pl):	Serwer SMB
Summary(cs):	Server SMB
Summary(da):	SMB server
Summary(de):	SMB-Server
Summary(es):	El servidor SMB
Summary(fi):	SMB-palvelin
Summary(fr):	Serveur SMB
Summary(it):	Server SMB
Summary(ja):	Samba SMB サーバー
Summary(pl):	Serwer SMB
Summary(pt_BR):	Cliente e servidor SMB
Summary(ru):	SMB клиент и сервер
Summary(tr):	SMB sunucusu
Summary(uk):	SMB клієнт та сервер
Summary(zh_CN):	Samba 客户端和服务器.
Name:		samba
Version:	2.2.5
Release:	6
License:	GPL v2
Group:		Networking/Daemons
URL:		http://www.samba.org/
Source0:	ftp://ftp.samba.org/pub/samba/%{name}-%{version}.tar.bz2
Source1:	smb.init
Source2:	%{name}.pamd
Source3:	swat.inetd
Source4:	%{name}.sysconfig
Source5:	%{name}.logrotate
Source6:	smb.conf
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
Prereq:		/sbin/chkconfig
Requires:	pam >= 0.66
Requires:	logrotate
Requires:	samba-common = %{version}
BuildRequires:	autoconf
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	readline-devel >= 4.2
BuildRequires:	pam-devel > 0.66
%{?_with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.6a
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/samba
%define		_libdir		%{_sysconfdir}
%define		_localstatedir	%{_var}/log/samba

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
Samba poskytuje server SMB, který lze použít pro poskytování síťových
služeb klientům SMB (někdy nazývaných klienti "LAN manažer") včetně
klientů různých verzí MS Windows, OS/2 a dalších linuxových strojů.
Samba též poskytuje některé klienty SMB, kteří komplementují vestavěný
souborový systém SMB v Linuxu. Samba používá protokoly NetBIOS přes
TCP/IP (NetBT) a NEpotřebuje protokol NetBEUI (neformátovaný rámec
NetBIOS od společnosti Microsoft.

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
Samba は MS Windows の様々なバージョン、OS/2 そして他の Linux マシン
を含む SMB (たまに "Lan Manager" と呼ばれる)
クライアントにネットワーク サービスを提供するために使用される SMB
サーバを提供します。Samba は NetBIOS over TCP/IP (NetBT)
プロトコルを使用し、 NetBEUI(Microsoft Raw NetBIOS frame)
プロトコルは必要ありません。

Samba ほとんど動作する NT ドメインコントロールの機能を特徴とし、
好きなブラウザを使って samba の smb.conf ファイルをリモート管理する
新しい SWAT (Samba Web Administration Tool) を含みます。
目下のところこれは inetd を通して TCP ポート 901 で有効になります。

%description -l pl
Samba udostępnia serwer SMB, który może być użyty w celu dostarczenia
usług sieciowych (potocznie zwanych "Lan Manager"), dla klientów
takich jak MS Windows, OS/2 a także maszyn linuksowych. W pakiecie
znajduje się również oprogramowanie klienckie. Samba używa protokołu
NetBIOS po TCP/IP (NetBT) i nie wymaga protokołu NetBEUI. Ta wersja ma
pełne wsparcie dla blokowania plików, a także wsparcie dla kodowania
haseł w standardzie MS i zarzadzania bazą WINS.

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
Samba надає SMB-сервер, що може бути використаний для надання
мережевих сервісів SMB (що їх іноді називають "Lan Manager") клієнтам,
включаючи різноманітні версії MS Windows, OS/2, та інші Linux-машини.
Samba також надає SMB-клієнтів, що працюють з вбудованою в Linux
файловою системою SMB.

Samba використовує протокол NetBIOS over TCP/IP (NetBT) та не потребує
протоколу NetBEUI (Microsoft Raw NetBIOS frame).

Samba містить майже працюючу реализацію NT Domain Control та новый
SWAT (Samba Web Administration Tool), котрий дозволяє віддалено
керувати конфігураційним файлом smb.conf за допомогою вашого
улюбленого WEB-броузера. Поки що він дозволений через inetd на
TCP-порту 901.

%package -n swat
Summary:	Samba Web Administration Tool
Summary(es):	Samba SWAT and Web documentation
Summary(pl):	Narzędzie administracyjne serwisu Samba
Summary(pt_BR):	Samba SWAT e documentação Web
Summary(ru):	Программа конфигурации SMB-сервера Samba
Summary(uk):	Програма конфигурації SMB-сервера Samba
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
swat pozwala na kompleksową konfigurację smb.conf przy pomocy
przeglądarki WWW.

%description -n swat -l pt_BR
SWAT - ferramentada Web de configuração do Samba.

%description -n swat -l ru
Пакет samba-swat включает новый SWAT (Samba Web Administration Tool),
для удаленного администрирования файла smb.conf при помощи вашего
любимого Web-браузера.

%description -n swat -l uk
Пакет samba-swat містить новий SWAT (Samba Web Administration Tool),
для дистанційного адміністрування файлу smb.conf за допомогою вашого
улюбленого Web-браузеру.

%package client
Summary:	Samba client programs
Summary(es):	Cliente SMB de Samba
Summary(ja):	Samba (SMB) クライアントプログラム
Summary(pl):	Klienci serwera Samba
Summary(pt_BR):	Cliente SMB do samba
Summary(ru):	Клиентские программы Samba (SMB)
Summary(uk):	Клієнтські програми Samba (SMB)
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
e também, à impressoras SMB.

%description client -l es
Cliente SMB de Samba.

%description client -l ja
Samba-client は Linux 上に含まれている SMB ファイルシステムを補う SMB
クライアントを提供します。これらは SMB 共有のアクセスと SMB
プリンタへの印刷を許可します。

%description client -l pl
Samba-client dostarcza pewne programy które uzupełniają system plików
SMB zawarty w jądrze. Pozwala na współdzielenie i drukowanie w sieci
SMB.

%description client -l pt_BR
O pacote samba-clientes prove alguns clientes SMB, que complementam o
sistema de arquivos SMB do Linux. Eles permitem o acesso a shares SMB,
e também, à impressoras SMB.

%description client -l ru
Пакет samba-client предоставляет некоторые клиенты SMB для работы со
встроенной файловой системой SMB в Linux. Эти клиенты позволяют
получать доступ к разделяемым каталогам SMB и печать на SMB-принтеры.

%description client -l uk
Пакет samba-client надає деякі клієнти SMB для роботи зі вбудованою
файловою системою SMB в Linux. Ці клієнти дозволяють отримувати доступ
до каталогів спільного використання SMB та друк на SMB-прінтери.

%package common
Summary:	Files used by both Samba servers and clients
Summary(es):	Common files between samba and samba-clients
Summary(ja):	Samba サーバーとクライアントで使用されるプログラム
Summary(pl):	Pliki używane przez serwer i klientów Samba
Summary(pt_BR):	Arquivos em comum entre samba e samba-clients
Summary(ru):	Файлы, используемые как сервером, так и клиентом Samba
Summary(uk):	Файли, що використовуються як сервером, так і клієнтом Samba
Group:		Networking/Daemons

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description common -l ja
Samba-common は Samba のサーバとクライアントの両方のパッケージで
使用されるファイルを提供します。

%description common -l pl
Samba-common dostarcza pliki niezbędne zarówno dla serwera jak i
klientów Samba.

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
Summary(pl):	Moduł PAM smbpass
Group:		Base
Obsoletes:	pam_smbpass

%description -n pam-pam_smbpass
PAM module which can be used on conforming systems to keep the
smbpasswd (Samba password) database in sync with the unix password
file.

%description -n pam-pam_smbpass -l pl
Moduł PAMa, który może być używany do trzymania pliku smbpasswd (hasła
Samby) zsynchronizowanego z hasłami unixowymi.

%package -n libsmbclient
Summary:	libsmbclient - samba client library
Summary(pl):	libsmbclient - biblioteka klienta samby
Group:		Libraries

%description -n libsmbclient
libsmbclient - library that allows to use samba clients functions.

%description -n libsmbclient -l pl
libsmbclient - biblioteka pozwalająca korzystać z funcji klienta
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
Pliki nagłówkowe dla libsmbclient.

%description -n libsmbclient-devel -l pt_BR
Arquivos de inclusão, bibliotecas e documentação necessários para
desenvolver aplicativos clientes para o samba.

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d,security,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/{var/{lock,log,log/archiv,spool},home/services}/samba \
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

install source/nsswitch/libnss_wins.so	$RPM_BUILD_ROOT/lib/libnss_wins.so.2
install source/nsswitch/pam_winbind.so	$RPM_BUILD_ROOT/lib/security/
install source/bin/pam_smbpass.so	$RPM_BUILD_ROOT/lib/security/
install source/bin/wbinfo		$RPM_BUILD_ROOT%{_bindir}

install source/bin/libsmbclient.so $RPM_BUILD_ROOT/lib/libsmbclient.so.0
ln -s libsmbclient.so.0 $RPM_BUILD_ROOT/lib/libsmbclient.so

install source/include/libsmbclient.h $RPM_BUILD_ROOT%{_includedir}

touch $RPM_BUILD_ROOT/var/lock/samba/{STATUS..LCK,wins.dat,browse.dat}

echo 127.0.0.1 localhost > $RPM_BUILD_ROOT%{_libdir}/lmhosts

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
%doc docs/nsswitch/README
%doc source/nsswitch/README winbind.pam
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/smbd
%attr(755,root,root) %{_sbindir}/winbindd
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_bindir}/smbpasswd
%attr(755,root,root) %{_bindir}/smbcontrol

%attr(755,root,root) /lib/libnss_wins*
%attr(755,root,root) /lib/security/pam_winbind.so

%dir %{_libdir}
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
%attr(755,root,root) %{_bindir}/smbspool
%attr(755,root,root) %{_bindir}/smbcacls
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/smbcacls.1*
%attr(755,root,root) %{_bindir}/rpcclient
%{_mandir}/man1/rpcclient.1*
%attr(755,root,root) %{_bindir}/wbinfo
%{_mandir}/man1/wbinfo.1*

%files common
%defattr(644,root,root,755)
%doc README Manifest WHATSNEW.txt
%doc Roadmap docs/faq docs/Registry/*
%doc docs/textdocs/* docs/htmldocs/*.* docs/{history,announce,THANKS}
%config(noreplace) %verify(not size mtime md5) %{_libdir}/smb.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_libdir}/lmhosts
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
