Summary:	SMB client and server
Summary(pl):	Klient i serwer SMB
Name:		samba
Version:	2.0.4b
Release:	1
Copyright:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://samba.anu.edu.au/pub/samba/%{name}-%{version}.tar.gz
Source1:	samba.PLD.tar.bz2
Source2:	samba.pamd
Patch0:		samba-glibc2.1.patch
Patch1:		samba-config.patch
Patch2:		samba-cap.patch
Prereq:		/sbin/chkconfig 
Requires:	pam >= 0.66 
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	pam-devel
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Samba provides an SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients, including various versions of MS Windows, OS/2,
and other Linux machines. Samba also provides some SMB
clients, which complement the built-in SMB filesystem
in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

This release is known as the "Locking Update" and has full
support for Opportunistic File Locking. In addition this update
includes native support for Microsoft encrypted passwords,
improved browse list and WINS database management.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.
Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.

%description -l pl
Samba udostêpnia serwer SMB, który mo¿e byæ u¿yty w celu dostarczenia
us³ug sieciowych (potocznie zwanych "Lan Manager"), dla klientów takich
jak MS Windows, OS/2 a tak¿e maszyn linuxowych.  W pakiecie znajduje siê
równie¿ oprogramowanie klienckie. Samba u¿ywa protoko³u NetBIOS po TCP/IP
(NetBT) i nie wymaga protoko³u NetBEUI. Ta wersja ma pe³ne wsparcie dla
blokowania plików, a tak¿e wsparcie dla kodowania hase³ w standardzie
MS i zarzadzania baz± WINS.

UWAGA: w przeciwieñstwie do wersji 2.0.2 aktualnie samba pozbawiona jest
mozliwo¶ci kontrolowania domeny NT.

%package -n swat
Summary:	Samba Web Administration Tool
Summary(pl):	Narzêdzie administracyjne serwisu Samba
Group:		Networking/Admin
Group(pl):	Sieciowe/Administracja
Requires:	%{name}

%description -n swat
swat allows a Samba administrator to configure the complex smb.conf
file via a Web browser. In addition, a swat configuration page has
help links to all the configurable options in the smb.conf file
allowing an administrator to easily look up the effects of any change.

swat is run from inetd

%description -n swat -l pl
swat pozwala na kompleksow± konfiguracjê smb.conf przy pomocy przegl±darki
internetowej.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd source
autoconf
LDFLAGS="-s" export LDFLAGS \
%configure \
	--prefix=/usr \
	--sysconfdir=/etc/samba \
	--sbindir=%{_sbindir} \
	--bindir=%{_bindir} \
	--with-privatedir=/etc/samba \
	--libdir=/etc/samba \
	--localstatedir=/var \
	--with-swatdir=%{_datadir}/swat \
	--with-smbmount \
	--with-smbwrapper \
	--with-quotas \
	--with-syslog \
	--with-automount
	
make all smbwrapper bin/smbrun bin/debug2html

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/samba/codepages/src \
	$RPM_BUILD_ROOT/etc/{logrotate.d,pam.d,sysconfig} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/home/samba \
	$RPM_BUILD_ROOT/lib/security \
	$RPM_BUILD_ROOT/usr/{bin,man/man{1,5,7,8},sbin} \
	$RPM_BUILD_ROOT/var/{lock,log,spool}/samba \
	$RPM_BUILD_ROOT%{_datadir}/swat/{include,images,help}

( cd source;
make install \
	prefix=$RPM_BUILD_ROOT/usr \
	BASEDIR=$RPM_BUILD_ROOT/usr \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	LIBDIR=$RPM_BUILD_ROOT/etc/samba \
	PRIVATEDIR=$RPM_BUILD_ROOT/etc/samba \
	SWATDIR=$RPM_BUILD_ROOT%{_datadir}/swat \
	VARDIR=$RPM_BUILD_ROOT/var
)

install  source/codepages/codepage_def.* \
	$RPM_BUILD_ROOT/etc/samba/codepages/src

install  packaging/PLD/smb.conf		$RPM_BUILD_ROOT/etc/samba
install  packaging/PLD/smbusers		$RPM_BUILD_ROOT/etc/samba
install  packaging/PLD/smbprint		$RPM_BUILD_ROOT%{_bindir}
install  packaging/PLD/smbadduser	$RPM_BUILD_ROOT%{_bindir}
install  packaging/PLD/findsmb		$RPM_BUILD_ROOT%{_bindir}
install  packaging/PLD/smb.init		$RPM_BUILD_ROOT/etc/rc.d/init.d/smb
install  packaging/PLD/samba.log	$RPM_BUILD_ROOT/etc/logrotate.d/samba
install  %{SOURCE2}			$RPM_BUILD_ROOT/etc/pam.d/samba

install -s source/bin/*.so 	$RPM_BUILD_ROOT/lib/security
install -s source/bin/{smbsh,smbrun,debug2html} $RPM_BUILD_ROOT%{_bindir}


touch $RPM_BUILD_ROOT/var/lock/samba/{STATUS..LCK,wins.dat,browse.dat}

echo 127.0.0.1 localhost > $RPM_BUILD_ROOT/etc/samba/lmhosts

echo "NICELEVEL=+5" > $RPM_BUILD_ROOT/etc/sysconfig/samba

for i in 437 737 850 852 861 866 932 949 950 936; do
$RPM_BUILD_ROOT%{_bindir}/make_smbcodepage c $i \
$RPM_BUILD_ROOT/etc/samba/codepages/src/codepage_def.$i \
$RPM_BUILD_ROOT/etc/samba/codepages/codepage.$i; done

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man{1,5,7,8}/* \
	README Manifest WHATSNEW.txt Roadmap docs/*.reg swat/README

%post
/sbin/chkconfig --add smb
if test -r /var/run/smb.pid; then
	/etc/rc.d/init.d/smb stop >&2
	/etc/rc.d/init.d/smb start >&2
else
	echo "Run \"/etc/rc.d/init.d/smb start\" to start samba daemons."
fi

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/smb stop >&2
	/sbin/chkconfig --del smb
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz Manifest.gz WHATSNEW.txt.gz
%doc Roadmap.gz docs/faq/*.html docs/*.reg.gz 

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/smbd

%dir /etc/samba
%config(noreplace) %verify(not size mtime md5) /etc/samba/smb.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/samba/smbusers
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/samba/lmhosts

%attr(750,root,root) /etc/rc.d/init.d/smb
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/samba
%attr(640,root,root) /etc/logrotate.d/samba
%attr(640,root,root) /etc/pam.d/samba

%attr(755,root,root) /lib/security/*.so

%{_mandir}/man[157]/*
%{_mandir}/man8/nmbd.8.gz
%{_mandir}/man8/smbd.8.gz
%{_mandir}/man8/smbmnt.8.gz
%{_mandir}/man8/smbmount.8.gz
%{_mandir}/man8/smbpasswd.8.gz
%{_mandir}/man8/smbumount.8.gz

%dir /home/samba
/etc/samba/codepages

%dir /var/lock/samba
%ghost /var/lock/samba/*

%attr(0750,root,root) %dir /var/log/samba
%attr(1777,root,root) %dir /var/spool/samba

%files -n swat
%defattr(644,root,root,755)
%doc swat/README.gz
%attr(755,root,root) %{_sbindir}/swat
%{_datadir}/swat
%{_mandir}/man8/swat.8.gz
