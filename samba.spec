Summary:	SMB server
Summary(pl):	Serwer SMB
Summary(cs):	Server SMB
Summary(da):	SMB server
Summary(de):	SMB-Server
Summary(fi):	SMB-palvelin
Summary(fr):	Serveur SMB
Summary(it):	Server SMB
Summary(tr):	SMB sunucusu
Name:		samba
Version:	2.2.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
URL:		http://www.samba.org/
Source0:	ftp://ftp.samba.org/pub/samba/%{name}-%{version}.tar.gz
Source1:	smb.init
Source2:	%{name}.pamd
Source3:	swat.inetd
Source4:	%{name}.sysconfig
Source5:	%{name}.logrotate
Source6:	smb.conf
Patch1:		%{name}-config.patch
Patch2:		%{name}-cap.patch
Patch3:		%{name}-DESTDIR.patch
Patch6:		%{name}-manpages_PLD_fixes.patch
Patch7:		%{name}-smbprint.patch
Patch8:		%{name}-autoconf.patch
Patch9:		%{name}-smbadduser.patch
Patch10:	%{name}-nocups.patch
Patch11:	%{name}-nmbd_socket.patch
Prereq:		/sbin/chkconfig
Requires:	pam >= 0.66
Requires:	logrotate
Requires:	samba-common = %{version} 
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	readline-devel >= 4.2
BuildRequires:	pam-devel > 0.66
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

%description -l pl
Samba udostêpnia serwer SMB, który mo¿e byæ u¿yty w celu dostarczenia
us³ug sieciowych (potocznie zwanych "Lan Manager"), dla klientów
takich jak MS Windows, OS/2 a tak¿e maszyn linuxowych. W pakiecie
znajduje siê równie¿ oprogramowanie klienckie. Samba u¿ywa protoko³u
NetBIOS po TCP/IP (NetBT) i nie wymaga protoko³u NetBEUI. Ta wersja ma
pe³ne wsparcie dla blokowania plików, a tak¿e wsparcie dla kodowania
hase³ w standardzie MS i zarzadzania baz± WINS.

%package -n swat
Summary:	Samba Web Administration Tool
Summary(pl):	Narzêdzie administracyjne serwisu Samba
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administacyjne
Requires:	%{name}
Requires:	rc-inetd >= 0.8.2
Requires:	inetdaemon

%description -n swat
swat allows a Samba administrator to configure the complex smb.conf
file via a Web browser. In addition, a swat configuration page has
help links to all the configurable options in the smb.conf file
allowing an administrator to easily look up the effects of any change.

swat is run from inet server.

%description -n swat -l pl
swat pozwala na kompleksow± konfiguracjê smb.conf przy pomocy
przegl±darki www.

%package client
Summary:	Samba client programs.
Summary(pl):	Klienci serwera Samba
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Requires:	samba-common = %{version}
Obsoletes:	smbfs

%description client
Samba-client provides some SMB clients, which complement the build-in
SMB filesystem in Linux. These allow accessing of SMB shares and
printing to SMB printers.

%description client -l pl
Klient-samby dostarcza pewne programy które uzupe³niaj± system plików
SMB zawarty w j±drze. Pozwala na wspó³dzielenie i drukowanie w sieci
SMB.

%package common
Summary:	Files used by both Samba servers and clients.
Summary(pl):	Pliki u¿ywane przez serwer i klientów Samba.
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description common -l pl
Samba-common dostarcza pliki niezbêdne zarówno dla serwera jak i
klientów Samba.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
#update required
#%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
cd source
autoconf
%configure \
	--with-readline \
	--with-privatedir=%{_libdir} \
	--with-lockdir=%{_var}/lock/samba \
	--with-swatdir=%{_datadir}/swat \
	--with-smbmount \
	--with-automount \
	--without-smbwrapper \
	--with-netatalk \
	--with-msdfs \
	--with-quotas \
	--with-vfs \
	--with-utmp \
	--with-syslog \
	--with-mmap \
	--with-pam \
	--with-ssl \
	--with-sslinc=%{_prefix}
	
%{__make} all 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d,security,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/{var/{lock,log,log/archiv,spool},home}/samba \
	$RPM_BUILD_ROOT/sbin 

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

touch $RPM_BUILD_ROOT/var/lock/samba/{STATUS..LCK,wins.dat,browse.dat}

echo 127.0.0.1 localhost > $RPM_BUILD_ROOT%{_libdir}/lmhosts

> $RPM_BUILD_ROOT%{_libdir}/smbusers
> $RPM_BUILD_ROOT/etc/security/blacklist.samba

gzip -9nf README Manifest WHATSNEW.txt Roadmap docs/*.reg swat/README \
	docs/textdocs/* docs/{history,announce,THANKS}

rm -f docs/faq/*.{sgml,txt}
rm -f docs/htmldocs/*.[0-9].*.html

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
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/smbd
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_bindir}/smbpasswd
%attr(755,root,root) %{_bindir}/convert_smbpasswd
%attr(755,root,root) %{_bindir}/smbcontrol

%dir %{_libdir}
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_libdir}/smbusers
%attr(754,root,root) /etc/rc.d/init.d/smb
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/samba
%attr(640,root,root) /etc/logrotate.d/samba
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/samba
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.samba
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/smbpasswd.8*

%dir /home/samba
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

%files common
%defattr(644,root,root,755)
%doc README.gz Manifest.gz WHATSNEW.txt.gz
%doc Roadmap.gz docs/faq docs/*.reg.gz
%doc docs/textdocs docs/htmldocs/*.* docs/{history,announce,THANKS}.gz
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
%doc swat/README*
%attr(755,root,root) %{_sbindir}/swat
%{_datadir}/swat
%{_mandir}/man8/swat.8*

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/swat
