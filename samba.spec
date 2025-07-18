# TODO:
# - gpfs.h (nfs-ganesha?)
#
# Note:
# - unpredictible build failures:
#   fail: http://buildlogs.pld-linux.org//index.php?dist=th&arch=i686&ok=0&name=samba&id=8e631f35-f333-464e-b872-135db73f0a67&action=tail
#   ok: http://buildlogs.pld-linux.org//index.php?dist=th&arch=i686&ok=1&name=samba&id=1188195b-4017-48c5-8c07-f1deb41b5800&action=tail 
#
# Conditional build:
%bcond_without	ads		# ActiveDirectory support
%bcond_without	ceph		# Ceph (RADOS) storage support
%bcond_without	cups		# CUPS support
%bcond_without	glusterfs	# GlusterFS storage support
%bcond_without	ldap		# LDAP support
%bcond_without	avahi		# Avahi support
%bcond_without	dmapi		# DMAPI support
%bcond_without	fam		# FAM support
%bcond_without	lttng		# lttng-ust support
%bcond_without	spotlight	# Spotlight tracker support
%bcond_without	systemd		# systemd integration
%bcond_without	winexe		# winexe tool
%bcond_with	system_heimdal	# Use system Heimdal libraries [since samba 4.4.x build fails with heimdal 1.5.x/7.x]
%bcond_without	system_libbsd	# system libbsd for MD5, strl*, setproctitle, getpeeridfunctions
%bcond_without	system_libs	# system libraries from SAMBA project (talloc,tdb,tevent)
%bcond_without	ctdb_pcp	# Performance Co-Pilot support for CTDB
# turn on when https://bugzilla.samba.org/show_bug.cgi?id=11764 is fixed
%bcond_with	replace
%bcond_without	lmdb		# LMDB module in ldb (64-bit only)

%define		ver		4.22.3
%define		rel		1
%define		ldb_ver		2.11.0
%define		ldb_rel		%{ver}.%{rel}

%if %{with system_libs}
%define		talloc_ver	2:2.4.3
%define		tdb_ver		2:1.4.13
%define		tevent_ver	0.16.2
%endif

# dmapi-devel with xfsprogs-devel >= 4.11(?) needs largefile (64bit off_t) that isn't detected properly
%ifarch %{ix86}
%undefine	with_dmapi
%endif

%ifnarch %arch64
# lmdb support requires 64-bit size_t
%undefine	with_lmdb
%endif

# NOTE: packages order is: server + additions, common, clients, libs+devel, ldap
Summary:	Samba Active Directory and SMB server
Summary(pl.UTF-8):	Serwer Samba Active Directory i SMB
Name:		samba
Version:	%{ver}
Release:	%{rel}
Epoch:		1
License:	GPL v3
Group:		Networking/Daemons
Source0:	https://download.samba.org/pub/samba/stable/%{name}-%{version}.tar.gz
# Source0-md5:	7a8e074950e15aa40997311fff217580
Source1:	smb.init
Source2:	samba.pamd
Source4:	samba.sysconfig
Source5:	samba.logrotate
Source6:	smb.conf
Source7:	winbind.init
Source8:	winbind.sysconfig
Source9:	samba.init
Patch0:		system-heimdal.patch
Patch1:		%{name}-c++-nofail.patch
Patch2:		%{name}-lprng-no-dot-printers.patch
Patch4:		unicodePwd-nthash-values-over-LDAP.patch
Patch5:		%{name}-heimdal.patch
Patch6:		server-role.patch
Patch8:		%{name}-no_libbsd.patch
Patch9:		heimdal-atomic.patch
URL:		https://www.samba.org/
BuildRequires:	acl-devel
%{?with_avahi:BuildRequires:	avahi-devel}
BuildRequires:	bison
%{?with_ceph:BuildRequires:	ceph-devel >= 11}
BuildRequires:	cmocka-devel >= 1.1.3
%if %{with winexe}
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-pthreads-w32
# for string.h
BuildRequires:	crossmingw32-runtime
BuildRequires:	crossmingw64-gcc
%endif
%{?with_cups:BuildRequires:	cups-devel >= 1:1.2.0}
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	dbus-devel
%{?with_dmapi:BuildRequires:	dmapi-devel}
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	flex
# just FAM API
%{?with_fam:BuildRequires:	gamin-devel}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
# new features up to 7.9
%{?with_glusterfs:BuildRequires:	glusterfs-devel >= 4}
BuildRequires:	gnutls-devel >= 3.6.13
BuildRequires:	gpgme-devel
%{?with_system_heimdal:BuildRequires:	heimdal-devel >= 1.5.3-1}
BuildRequires:	iconv
BuildRequires:	jansson-devel
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	libarchive-devel >= 3.1.2
%if %{without system_heimdal}
%ifnarch %arch_with_atomics64
BuildRequires:	libatomic-devel
%endif
%endif
%{?with_system_libbsd:BuildRequires:	libbsd-devel}
BuildRequires:	libcap-devel
BuildRequires:	libcom_err-devel
BuildRequires:	libicu-devel
BuildRequires:	libmagic-devel
BuildRequires:	libnscd-devel
BuildRequires:	libnsl-devel
BuildRequires:	libtasn1-devel >= 3.8
BuildRequires:	libtirpc-devel
BuildRequires:	libunwind-devel
BuildRequires:	liburing-devel
BuildRequires:	libxslt-progs
%{?with_lmdb:BuildRequires:	lmdb-devel >= 0.9.16}
%{?with_lttng:BuildRequires:	lttng-ust-devel}
BuildRequires:	make >= 1:3.81
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	ncurses-ext-devel >= 5.2
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
# detected and used for linking, but dropped by -Wl,--as-needed
#BuildRequires:	openssl-devel
BuildRequires:	pam-devel >= 0.99.8.1
%{?with_ctdb_pcp:BuildRequires:	pcp-devel}
BuildRequires:	perl-ExtUtils-MakeMaker
%{!?with_system_heimdal:BuildRequires:	perl-modules}
BuildRequires:	perl-Parse-Yapp >= 1.05
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.6
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-dns
BuildRequires:	python3-iso8601
BuildRequires:	python3-markdown
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-subunit
BuildRequires:	python3-testtools
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpcsvc-proto
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.025
BuildRequires:	sed >= 4.0
BuildRequires:	subunit-devel
%{?with_systemd:BuildRequires:	systemd-devel}
%{?with_spotlight:BuildRequires:	tracker-devel >= 2.0}
BuildRequires:	xfsprogs-devel
BuildRequires:	zlib-devel >= 1.2.3
%if %{with system_libs}
BuildRequires:	python3-talloc-devel >= %{talloc_ver}
BuildRequires:	python3-tdb >= %{tdb_ver}
BuildRequires:	python3-tevent >= %{tevent_ver}
BuildRequires:	talloc-devel >= %{talloc_ver}
BuildRequires:	tdb-devel >= %{tdb_ver}
BuildRequires:	tevent-devel >= %{tevent_ver}
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
# for samba_{dnsupdate,kcc,spnupdate,upgradedns} scripts
Requires:	logrotate >= 3.7-4
Requires:	pam >= 0.99.8.1
Requires:	python3-samba = %{epoch}:%{version}-%{release}
Requires:	rc-scripts >= 0.4.0.12
Requires:	setup >= 2.4.6-7
Requires:	systemd-units >= 38
# smbd links with libcups
%{?with_cups:Requires:	cups-lib >= 1:1.2.0}
Obsoletes:	samba-doc-html < 1:4
Obsoletes:	samba-doc-pdf < 1:4
Obsoletes:	samba-pdb-xml < 3.0.23
Obsoletes:	samba-vfs-audit < 1:4.1.4-3
Obsoletes:	samba-vfs-block < 1:4.1.4-3
Obsoletes:	samba-vfs-cap < 1:4.1.4-3
Obsoletes:	samba-vfs-catia < 1:4.1.4-3
Obsoletes:	samba-vfs-default_quota < 1:4.1.4-3
Obsoletes:	samba-vfs-expand_msdfs < 1:4.1.4-3
Obsoletes:	samba-vfs-fake_perms < 1:4.1.4-3
Obsoletes:	samba-vfs-netatalk < 1:4.1.4-3
Obsoletes:	samba-vfs-readahead < 1:4.1.4-3
Obsoletes:	samba-vfs-readonly < 1:4.1.4-3
Obsoletes:	samba-vfs-recycle < 1:4.1.4-3
Obsoletes:	samba-vfs-scannedonly < 1:4.1.4-3
Obsoletes:	samba-vfs-shadow_copy < 1:4.1.4-3
Obsoletes:	samba3 < 1:4.1.4-3
Obsoletes:	samba3-server < 1:4.1.4-3
Obsoletes:	samba3-vfs-audit < 1:4.1.4-3
Obsoletes:	samba3-vfs-cap < 1:4.1.4-3
Obsoletes:	samba3-vfs-catia < 1:4.1.4-3
Obsoletes:	samba3-vfs-default_quota < 1:4.1.4-3
Obsoletes:	samba3-vfs-expand_msdfs < 1:4.1.4-3
Obsoletes:	samba3-vfs-fake_perms < 1:4.1.4-3
Obsoletes:	samba3-vfs-netatalk < 1:4.1.4-3
Obsoletes:	samba3-vfs-readahead < 1:4.1.4-3
Obsoletes:	samba3-vfs-readonly < 1:4.1.4-3
Obsoletes:	samba3-vfs-recycle < 1:4.1.4-3
Obsoletes:	samba3-vfs-scannedonly < 1:4.1.4-3
Obsoletes:	samba3-vfs-shadow_copy < 1:4.1.4-3
Obsoletes:	samba4 < 1:4.1.4-3
Obsoletes:	samba4-common-server < 1:4.1.4-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sambahome	/home/services/samba
%if %{with cups}
%define		cups_serverbin	%{_prefix}/lib/cups
%endif
%define		schemadir	/usr/share/openldap/schema

# CFLAGS modified (the second ./configure)
%undefine	configure_cache

%description
Samba provides an SMB server which can be used to provide network
services to SMB (sometimes called "Lan Manager") clients, including
various versions of MS Windows, OS/2, and other Linux machines. Samba
also provides some SMB clients, which complement the built-in SMB
filesystem in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame) protocol.

%description -l pl.UTF-8
Samba udostępnia serwer SMB, który może być użyty w celu dostarczenia
usług sieciowych (potocznie zwanych "Lan Manager"), dla klientów
takich jak MS Windows, OS/2 a także maszyn linuksowych. W pakiecie
znajduje się również oprogramowanie klienckie. Samba używa protokołu
NetBIOS po TCP/IP (NetBT) i nie wymaga protokołu NetBEUI. Ta wersja ma
pełne wsparcie dla blokowania plików, a także wsparcie dla kodowania
haseł w standardzie MS i zarządzania bazą WINS.

%package vfs-ceph
Summary:	VFS module to host shares on Ceph file system
Summary(pl.UTF-8):	Moduł VFS do serwowania zasobów z systemu plików Ceph
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	ceph-libs >= 11

%description vfs-ceph
VFS module to host shares on Ceph file system.

This module only works with the libceph.so user-space client. It is
not needed if you are using the kernel client or the FUSE client.

%description vfs-ceph -l pl.UTF-8
Moduł VFS do serwowania zasobów z systemu plików Ceph.

Ten moduł działa jedynie z klientem przestrzeni użytkownika
libceph.so. Jest zbędny w przypadku używania klienta dostarczanego
przez jądro lub FUSE.

%package vfs-glusterfs
Summary:	VFS module to host shares on GlusterFS file system
Summary(pl.UTF-8):	Moduł VFS do serwowania zasobów z systemu plików GlusterFS
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description vfs-glusterfs
VFS module to host shares on GlusterFS file system.

%description vfs-glusterfs -l pl.UTF-8
Moduł VFS do serwowania zasobów z systemu plików GlusterFS.

%package common
Summary:	Files used by both Samba servers and clients
Summary(pl.UTF-8):	Pliki używane przez serwer i klientów Samby
Group:		Networking/Daemons
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
# for samba-tool script
Requires:	python3-samba = %{epoch}:%{version}-%{release}
Obsoletes:	samba3-common < 1:4.1.4-3
Obsoletes:	samba4-common < 1:4.1.4-3

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description common -l pl.UTF-8
Samba-common dostarcza pliki niezbędne zarówno dla serwera jak i
klientów Samby.

%package client
Summary:	Samba client programs
Summary(pl.UTF-8):	Klienci serwera Samba
Group:		Applications/Networking
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%{?with_system_heimdal:Requires:	heimdal-libs >= 1.5.3-1}
Requires:	libsmbclient = %{epoch}:%{version}-%{release}
Suggests:	cifs-utils
Obsoletes:	samba3-client < 1:4.1.4-3
Obsoletes:	samba4-client < 1:4.1.4-3
Obsoletes:	smbfs

%description client
Samba-client provides some SMB clients, which complement the build-in
SMB filesystem in Linux. These allow accessing of SMB shares and
printing to SMB printers.

%description client -l pl.UTF-8
Samba-client dostarcza programy uzupełniające obsługę systemu plików
SMB zawartą w jądrze. Pozwalają one na współdzielenie zasobów SMB i
drukowanie w sieci SMB.

%package winbind
Summary:	Samba-winbind daemon, utilities and documentation
Summary(pl.UTF-8):	Demon samba-winbind, narzędzia i dokumentacja
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	systemd-units >= 38
Obsoletes:	samba3-winbind < 1:4.1.4-3
Obsoletes:	samba4-winbind < 1:4.1.4-3
# pam_winbind is not complete replacement, but pam_smbpass has been removed (in samba 4.4)
#Obsoletes:	pam-pam_smbpass < 1:4.4

%description winbind
Provides the winbind daemon and testing tools to allow authentication
and group/user enumeration from a Windows or Samba domain controller.

%description winbind -l pl.UTF-8
Pakiet zawiera demona winbind oraz narzędzia testowe. Umożliwia
uwierzytelnianie i wyliczanie grup/użytkowników z kontrolera domeny
Windows lub Samba.

%package -n cups-backend-smb
Summary:	CUPS backend for printing to SMB printers
Summary(pl.UTF-8):	Backend CUPS-a drukujący na drukarkach SMB
Group:		Applications/Printing
Requires:	%{name}-client = %{epoch}:%{version}-%{release}
Requires:	cups >= 1:1.2.0
Obsoletes:	cups-backend-smb3 < 1:4.1.4-3

%description -n cups-backend-smb
CUPS backend for printing to SMB printers.

%description -n cups-backend-smb -l pl.UTF-8
Backend CUPS-a drukujący na drukarkach SMB.

%package -n nss_wins
Summary:	Name Service Switch service for WINS
Summary(pl.UTF-8):	Usługa Name Service Switch dla WINS
Group:		Base
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	nss_wins3 < 1:4.1.4-3

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names
to IP addresses.

%description -n nss_wins -l pl.UTF-8
Biblioteka dzielona libnss_wins rozwiązująca nazwy NetBIOS na adresy
IP.

%package -n smbget
Summary:	A utility for retrieving files using the SMB protocol
Summary(pl.UTF-8):	Narzędzie do pobierania plików protokołem SMB
Group:		Applications/Networking
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	smbget3 < 1:4.1.4-3

%description -n smbget
wget-like utility for downloading files over SMB.

%description -n smbget -l pl.UTF-8
Narzędzie podobne do wgeta do pobierania plików protokołem SMB
używanym w sieciach MS Windows.

%package libs
Summary:	Samba shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Samby
Group:		Libraries
Requires:	gnutls >= 3.6.13
Requires:	ldb = %{epoch}:%{ldb_ver}-%{ldb_rel}
%if %{with system_libs}
Requires:	talloc >= %{talloc_ver}
Requires:	tdb >= %{tdb_ver}
Requires:	tevent >= %{tevent_ver}
%endif
# samba 4.11+ dropped support for python2
Obsoletes:	python-samba < 1:4.11
Obsoletes:	samba-vfs-notify_fam < 1:4.4.4

%description libs
Samba shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Samby.

%package devel
Summary:	Header files for Samba
Summary(pl.UTF-8):	Pliki nagłówkowe Samby
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	samba3-devel < 1:4.1.4-3
Obsoletes:	samba4-devel < 1:4.1.4-3

%description devel
Header files for Samba.

%description devel -l pl.UTF-8
Pliki nagłówkowe Samby.

%package pidl
Summary:	Perl IDL compiler
Summary(pl.UTF-8):	Kompilator IDL w Perlu
Group:		Development/Tools
Obsoletes:	samba4-pidl < 1:4.1.4-3

%description pidl
The samba-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols.

%description pidl -l pl.UTF-8
Ten pakiet zawiera kompilator IDL napisany w Perlu, używany przez
Sambę oraz Wiresharka to analizy IDL i podobnych protokołów.

%package -n python3-samba
Summary:	Samba modules for Python 3
Summary(pl.UTF-8):	Moduły Samby dla Pythona 3
Group:		Development/Languages/Python
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	python3 >= 1:3.6
Requires:	python3-dns
Requires:	python3-iso8601
Requires:	python3-ldb = %{epoch}:%{ldb_ver}-%{ldb_rel}
Requires:	python3-modules >= 1:3.5
%if %{with system_libs}
Requires:	python3-talloc >= %{talloc_ver}
Requires:	python3-tevent >= %{tevent_ver}
%endif

%description -n python3-samba
Samba modules for Python3.

%description -n python3-samba -l pl.UTF-8
Moduły Samby dla Pythona 3.

%package test
Summary:	Testing tools for Samba servers and clients
Summary(pl.UTF-8):	Narzędzia testowe dla serwerów i klientów Samby
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-winbind = %{epoch}:%{version}-%{release}
Obsoletes:	samba4-test < 1:4.1.4-3
Obsoletes:	samba4-test-devel < 1:4.1.4-3
Obsoletes:	samba-test-devel < 1:4.5.1-3

%description test
samba-test provides testing tools for both the server and client
packages of Samba.

%description test -l pl.UTF-8
Narzędzia testowe dla serwerów i klientów Samby.

%package -n libsmbclient
Summary:	libsmbclient and libwbclient - Samba client libraries
Summary(pl.UTF-8):	libsmbclient i libwbclient - biblioteki klienckie Samby
Group:		Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	samba3-libsmbclient < 1:4.1.4-3

%description -n libsmbclient
libsmbclient and libwbclient - libraries that allow to use Samba
client functions.

%description -n libsmbclient -l pl.UTF-8
libsmbclient i libwbclient - biblioteki pozwalające korzystać z funcji
klienta Samby.

%package -n libsmbclient-devel
Summary:	Development files for Samba client libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek klienta Samby
Group:		Development/Libraries
Requires:	libsmbclient = %{epoch}:%{version}-%{release}
Obsoletes:	libsmbclient-static < 1:4
Obsoletes:	samba3-libsmbclient-devel < 1:4.1.4-3

%description -n libsmbclient-devel
Header files for libsmbclient and libwbclient libraries.

%description -n libsmbclient-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libsmbclient i libwbclient.

%package -n openldap-schema-samba
Summary:	Samba LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla Samby
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
Obsoletes:	openldap-schema-samba3 < 1:4.1.4-3
BuildArch:	noarch

%description -n openldap-schema-samba
This package contains samba.schema for OpenLDAP.

%description -n openldap-schema-samba -l pl.UTF-8
Ten pakiet zawiera schemat Samby (samba.schema) dla OpenLDAP-a.

%package -n ctdb
Summary:	A Clustered Database based on Samba's Trivial Database (TDB)
Summary(pl.UTF-8):	Klastrowa baza danych oparta na bazie danych Trivial Database z Samby (TDB)
Group:		Daemons
URL:		http://ctdb.samba.org/
Requires(post,preun,postun):	systemd-units
Requires(post):	/bin/systemd-tmpfiles
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	coreutils
Requires:	fileutils
# for ps and killall
Requires:	gawk
Requires:	psmisc
Requires:	sed
%if %{with system_libs}
Requires:	tdb >= %{tdb_ver}
%endif
# for pkill and pidof:
Requires:	procps
# for netstat:
Requires:	ethtool
Requires:	net-tools
# for ip:
Requires:	iproute2
Requires:	iptables
# for flock, getopt, kill:
Requires:	util-linux

%description -n ctdb
CTDB is a cluster implementation of the TDB database used by Samba and
other projects to store temporary data. If an application is already
using TDB for temporary data it is very easy to convert that
application to be cluster aware and use CTDB instead.

%description -n ctdb -l pl.UTF-8
CTDB to klastrowa implementacja bazy danych TDB używanej w Sambie oraz
innych projektach do przechowywania danych tymczasowych. Jeśli jakaś
aplikacja już wykorzystuje TDB do trzymania danych tymczasowych,
bardzo przerobić ją na klastrowalną, wykorzystującą CTDB.

%package -n pcp-ctdb
Summary:	CTDB PMDA
Summary(pl.UTF-8):	PMDA CTDB
Group:		Applications/System
Requires:	ctdb = %{epoch}:%{version}-%{release}
Requires:	pcp

%description -n pcp-ctdb
This PMDA extracts metrics from the locally running ctdbd daemon for
export to PMCD.

%description -n pcp-ctdb -l pl.UTF-8
Ten PMDA odczytuje pomiary z lokalnie działającego demona ctdbd w celu
wyeksportowania do PMCD.

%package -n ldb
Summary:	LDAP-like embedded database
Summary(pl.UTF-8):	Wbudowana baza danych podobna do LDAP
Version:	%{ldb_ver}
Release:	%{ldb_rel}
Group:		Libraries
%{?with_lmdb:Requires:	lmdb-libs >= 0.9.16}
Requires:	talloc >= %{talloc_ver}
Requires:	tdb >= %{tdb_ver}
Requires:	tevent >= %{tevent_ver}
Requires:	popt >= 1.6
Provides:	libldb = %{epoch}:%{version}-%{release}
Obsoletes:	libldb < 1.1.0-3
# ldb 1.6+ dropped python2 support
Obsoletes:	python-ldb < 1.6
Obsoletes:	python-ldb-devel < 1.6

%description -n ldb
An extensible library that implements an LDAP like API to access
remote LDAP servers, or use local tdb databases.

%description -n ldb -l pl.UTF-8
Rozszerzalna biblioteka implementująca API podobne do LDAP pozwalające
na dostęp do zdalnych serwerów LDAP lub wykorzystanie lokalnych baz
danych tdb.

%package -n ldb-tools
Summary:	Tools to manage LDB files
Summary(pl.UTF-8):	Narzędzia do zarządzania plikami LDB
Version:	%{ldb_ver}
Release:	%{ldb_rel}
Group:		Applications/Databases
Requires:	ldb = %{epoch}:%{ldb_ver}-%{ldb_rel}

%description -n ldb-tools
Tools to manage LDB files.

%description -n ldb-tools -l pl.UTF-8
Narzędzia do zarządzania plikami LDB.

%package -n ldb-devel
Summary:	Header files for the LDB library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LDB
Version:	%{ldb_ver}
Release:	%{ldb_rel}
Group:		Development/Libraries
Requires:	ldb = %{epoch}:%{ldb_ver}-%{ldb_rel}
Requires:	talloc-devel >= %{talloc_ver}
Requires:	tdb-devel >= %{tdb_ver}
Requires:	tevent-devel >= %{tevent_ver}
Provides:	libldb-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libldb-devel < 1.1.0-3

%description -n ldb-devel
Header files needed to develop programs that link against the LDB
library.

%description -n ldb-devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do tworzenia programów wykorzystujących
bibliotekę LDB.

%package -n python3-ldb
Summary:	Python 3 bindings for the LDB library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki LDB
Version:	%{ldb_ver}
Release:	%{ldb_rel}
Group:		Libraries/Python
Requires:	ldb = %{epoch}:%{ldb_ver}-%{ldb_rel}
Requires:	python3-tdb >= %{tdb_ver}
Obsoletes:	pyldb < 1.1.0-1
Obsoletes:	python3-ldb-devel < 2.10.0

%description -n python3-ldb
Python 3 bindings for the LDB library.

%description -n python3-ldb -l pl.UTF-8
Wiązania Pythona 3 do biblioteki LDB.

%prep
%setup -q
%{?with_system_heimdal:%patch -P0 -p1}
%patch -P1 -p1
%patch -P2 -p1
%patch -P4 -p1
%{?with_system_heimdal:%patch -P5 -p1}
%patch -P6 -p1

%{!?with_system_libbsd:%patch -P8 -p1}
%if %{without system_heimdal}
%ifnarch %arch_with_atomics64
%patch -P9 -p1
%endif
%endif

%{__sed} -i -e '1s|#!/usr/bin/env bash|#!/bin/bash|' ctdb/tools/onnode
%{__sed} -i -e '1s|#!/usr/bin/env perl|#!/usr/bin/perl|' pidl/pidl
%{__sed} -i -e '/sed_expr1/ s|/usr/bin/env perl|/usr/bin/perl|' source3/script/wscript_build
%{__sed} -i -e '1s|#!/usr/bin/env python|#!/usr/bin/python|' source4/scripting/bin/samba*
%{__sed} -i -e '1s|#!/usr/bin/env python3|#!%{__python3}|' source3/script/samba-log-parser

%if %{with system_heimdal}
%{__mv} source4/heimdal_build/krb5-types{,-smb}.h
%endif

grep -q 'LDB_VERSION[[:space:]]*=[[:space:]]*['"'"'"]%{ldb_ver}['"'"'"]' lib/ldb/wscript

%build
LDFLAGS="${LDFLAGS:-%rpmldflags}" \
CFLAGS="${CFLAGS:-%rpmcflags}" \
CXXFLAGS="${CXXFLAGS:-%rpmcxxflags}" \
FFLAGS="${FFLAGS:-%rpmcflags}" \
FCFLAGS="${FCFLAGS:-%rpmcflags}" \
CPPFLAGS="${CPPFLAGS:-%rpmcppflags}" \
%{?__cc:CC="%{__cc}"} \
%{?__cxx:CXX="%{__cxx}"} \
./configure \
	--enable-fhs \
	--prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--with-privatelibdir=%{_libdir}/samba \
	--with-modulesdir=%{_libdir}/samba \
	--with-pammodulesdir=/%{_lib}/security \
	--with-lockdir=/var/lib/samba \
	--with-privatedir=%{_sysconfdir}/samba \
	--disable-rpath \
	--disable-rpath-install \
	--builtin-libraries=%{?with_replace:replace,}ccan%{?xxxx:,samba-cluster-support} \
	--bundled-libraries=NONE,iniparser,%{!?with_system_libs:talloc,tdb,tevent,pytalloc,pytalloc-util,pytdb,pytevent},%{!?with_system_heimdal:roken,wind,hx509,asn1,heimbase,hcrypto,krb5,gssapi,heimntlm,hdb,kdc,com_err,compile_et,asn1_compile} \
	--private-libraries='!ldb' \
	--with-shared-modules=idmap_ad,idmap_adex,idmap_hash,idmap_ldap,idmap_rid,idmap_tdb2,auth_samba4,vfs_dfs_samba4 \
	--with-cluster-support \
	--with-acl-support \
	--with%{!?with_ads:out}-ads \
	%{?with_ctdb_pcp:--enable-pmda} \
	--with-automount \
	--with%{!?with_dmapi:out}-dmapi \
	--with%{!?with_fam:out}-fam \
	--with-iconv \
	--with%{!?with_ldap:out}-ldap \
	--with%{!?with_lttng:out}-lttng \
	--with-pam \
	--with-quotas \
	--with-regedit \
	--with-sendfile-support \
	--with-syslog \
%if %{with systemd}
	--with-systemd \
	--systemd-install-services \
	--with-systemddir=%{systemdunitdir} \
%else
	--without-systemd \
%endif
	--with-utmp \
	--with-winbind \
	--with%{!?with_winexe:out}-winexe \
	--%{?with_avahi:en}%{!?with_avahi:dis}able-avahi \
	--enable-cups \
	%{__enable_disable glusterfs} \
	--enable-iprint \
	%{__enable_disable spotlight}

%{__make} V=1

# Build PIDL for installation into vendor directories before
# 'make proto' gets to it.
cd pidl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d,security,sysconfig/rc-inetd,ld.so.conf.d,env.d} \
	$RPM_BUILD_ROOT{/var/{log/archive,spool}/samba,/var/lib/samba/printing} \
	$RPM_BUILD_ROOT/var/log/samba/cores/{smbd,nmbd,winbindd} \
	$RPM_BUILD_ROOT{/sbin,/%{_lib}/security,%{_libdir},%{_libdir}/samba/vfs,%{_includedir},%{_sambahome},%{schemadir}} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CONFIGDIR=$RPM_BUILD_ROOT%{_sysconfdir}/samba

# Install PIDL
%{__make} -C pidl install \
	PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

# Clean out crap left behind by the PIDL install
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Parse/Pidl/.packlist

install -p source3/script/mksmbpasswd.sh $RPM_BUILD_ROOT%{_sbindir}

:> $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ctdb

cp -p packaging/systemd/samba.conf.tmp $RPM_BUILD_ROOT%{systemdtmpfilesdir}/samba.conf
echo "d /var/run/ctdb 755 root root" > $RPM_BUILD_ROOT%{systemdtmpfilesdir}/ctdb.conf
cp -p bin/default/packaging/systemd/ctdb.service $RPM_BUILD_ROOT%{systemdunitdir}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smb
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/samba
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/samba
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/samba
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/samba/smb.conf
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/winbind
cp -p %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/winbind
install -p %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/samba

echo "LDB_MODULES_PATH=%{_libdir}/samba/ldb" > $RPM_BUILD_ROOT/etc/env.d/LDB_MODULES_PATH

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libnss_winbind.so* $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libnss_wins.so* $RPM_BUILD_ROOT/%{_lib}

touch $RPM_BUILD_ROOT/var/lib/samba/{wins.dat,browse.dat}

echo '127.0.0.1 localhost' > $RPM_BUILD_ROOT%{_sysconfdir}/samba/lmhosts

%if "%{_lib}" == "lib64"
echo "%{_libdir}/samba" >$RPM_BUILD_ROOT/etc/ld.so.conf.d/samba64.conf
%else
echo "%{_libdir}/samba" >$RPM_BUILD_ROOT/etc/ld.so.conf.d/samba.conf
%endif

%if %{with cups}
install -d $RPM_BUILD_ROOT%{cups_serverbin}/backend
ln -s %{_bindir}/smbspool $RPM_BUILD_ROOT%{cups_serverbin}/backend/smb
%endif

> $RPM_BUILD_ROOT%{_sysconfdir}/samba/smbusers
> $RPM_BUILD_ROOT/etc/security/blacklist.samba

%if %{with ldap}
cp -p examples/LDAP/samba.schema $RPM_BUILD_ROOT%{schemadir}
%endif

# remove man pages for not installed commands
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/log2pcap.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man7/traffic_{learner,replay}.7*
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_cacheprime.8*
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_gpfs.8*
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_prealloc.8*
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_tsmsm.8*

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add samba
/sbin/chkconfig --add smb
%service samba restart "Samba AD daemon"
%service smb restart "Samba SMB daemons"
%systemd_post samba.service
%systemd_post smb.service nmb.service

%preun
if [ "$1" = "0" ]; then
	%service samba stop
	%service smb stop
	/sbin/chkconfig --del samba
	/sbin/chkconfig --del smb
fi
%systemd_preun samba.service
%systemd_preun smb.service nmb.service

%postun
%systemd_reload

%triggerpostun -- samba3
/sbin/chkconfig --add smb
%service smb restart "Samba SMB daemons"
%systemd_post smb.service nmb.service

%triggerpostun -- samba4
### samba4 < 1:4.1.1-1
# CVE-2013-4476
if [ -e %{_sysconfdir}/samba/tls/key.pem ]; then
	PERMS=$(stat -c %a %{_sysconfdir}/samba/tls/key.pem)
	if [ "$PERMS" != "600" ]; then
		chmod 600 %{_sysconfdir}/samba/tls/key.pem || :
		echo "Fixed permissions of private key file %{_sysconfdir}/samba/tls/key.pem from $PERMS to 600"
		echo "Consider regenerating TLS certificate"
		echo "Removing all tls .pem files will cause an auto-regeneration with the correct permissions"
	fi
fi

### any
/sbin/chkconfig --add samba
%service samba restart "Samba AD daemons"
%systemd_post samba.service

%triggerpostun -- samba < 1:4.9.2-3
%{_bindir}/net groupmap add sid=S-1-5-32-546 unixgroup=nobody type=builtin || :

%triggerprein common -- samba4
cp -a %{_sysconfdir}/samba/smb.conf %{_sysconfdir}/samba/smb.conf.samba4

%triggerpostun common -- samba4
%{__mv} -f %{_sysconfdir}/samba/smb.conf %{_sysconfdir}/samba/smb.conf.rpmnew
%{__mv} %{_sysconfdir}/samba/smb.conf.samba4 %{_sysconfdir}/samba/smb.conf

%triggerprein common -- samba3-server
cp -a %{_sysconfdir}/samba/smb.conf %{_sysconfdir}/samba/smb.conf.samba4

%triggerpostun common -- samba3-server
%{__mv} -f %{_sysconfdir}/samba/smb.conf %{_sysconfdir}/samba/smb.conf.rpmnew
%{__mv} %{_sysconfdir}/samba/smb.conf.samba4 %{_sysconfdir}/samba/smb.conf

%post winbind
/sbin/ldconfig
/sbin/chkconfig --add winbind
%service winbind restart "Winbind daemon"
%systemd_post winbind.service

%preun winbind
if [ "$1" = "0" ]; then
	%service winbind stop
	/sbin/chkconfig --del winbind
fi
%systemd_preun winbind.service

%postun winbind
/sbin/ldconfig
%systemd_reload

%triggerpostun winbind -- samba3-winbind
/sbin/chkconfig --add winbind
%service winbind restart "Winbind daemon"
%systemd_post winbind.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%triggerpostun libs -- samba-libs < 1:4.18.0-2
if [ ! -L %{_libdir}/libsmbconf.so.0 ]; then
	%{__rm} -f %{_libdir}/libsmbconf.so.0
fi
if [ ! -L %{_libdir}/libsmbldap.so.2 ]; then
	%{__rm} -f %{_libdir}/libsmbldap.so.2
fi
if [ ! -L %{_libdir}/libsamba-errors.so.1 ]; then
	%{__rm} -f %{_libdir}/libsamba-errors.so.1
fi
/sbin/ldconfig

%post	-n libsmbclient -p /sbin/ldconfig
%postun	-n libsmbclient -p /sbin/ldconfig

%post -n openldap-schema-samba
# dependant schemas: cosine(uid) inetorgperson(displayName) nis(gidNumber)
%openldap_schema_register %{schemadir}/samba.schema -d cosine,inetorgperson,nis
%service -q ldap restart

%postun -n openldap-schema-samba
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/samba.schema
	%service -q ldap restart
fi

%triggerpostun -n openldap-schema-samba -- openldap-schema-samba3 < 1:4.1.4-3
# dependant schemas: cosine(uid) inetorgperson(displayName) nis(gidNumber)
%openldap_schema_register %{schemadir}/samba.schema -d cosine,inetorgperson,nis
%service -q ldap restart

%post -n ctdb
/bin/systemd-tmpfiles --create %{systemdtmpfilesdir}/ctdb.conf
%systemd_post ctdb.service

%preun -n ctdb
%systemd_preun ctdb.service

%postun -n ctdb
%systemd_reload

%post	-n ldb -p /sbin/ldconfig
%postun	-n ldb -p /sbin/ldconfig

%post	-n python3-ldb -p /sbin/ldconfig
%postun	-n python3-ldb -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{?with_ldap:%doc examples/LDAP}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samba/smbusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/samba
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/samba
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.samba
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/samba
%config(noreplace) %verify(not md5 mtime size) /etc/env.d/LDB_MODULES_PATH
%attr(754,root,root) /etc/rc.d/init.d/samba
%attr(754,root,root) /etc/rc.d/init.d/smb
%if %{with systemd}
%{systemdunitdir}/nmb.service
%{systemdunitdir}/smb.service
%{systemdunitdir}/samba.service
%{systemdunitdir}/samba-bgqd.service
%endif
%{systemdtmpfilesdir}/samba.conf
%attr(755,root,root) %{_bindir}/dumpmscat
%attr(755,root,root) %{_bindir}/oLschema2ldif
%attr(755,root,root) %{_bindir}/pdbedit
%attr(755,root,root) %{_bindir}/profiles
%attr(755,root,root) %{_bindir}/sharesec
%attr(755,root,root) %{_bindir}/smbcontrol
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_sbindir}/eventlogadm
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/samba
%attr(755,root,root) %{_sbindir}/samba_dnsupdate
%attr(755,root,root) %{_sbindir}/samba_downgrade_db
%attr(755,root,root) %{_sbindir}/samba-gpupdate
%attr(755,root,root) %{_sbindir}/samba_kcc
%attr(755,root,root) %{_sbindir}/samba_spnupdate
%attr(755,root,root) %{_sbindir}/samba_upgradedns
%attr(755,root,root) %{_sbindir}/smbd
%dir %{_libdir}/samba/bind9
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_10.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_11.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_12.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_14.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_16.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_18.so
%dir %{_libdir}/samba/gensec
%attr(755,root,root) %{_libdir}/samba/gensec/krb5.so
%if %{with system_heimdal}
%dir %{_libdir}/samba/hdb
%attr(755,root,root) %{_libdir}/samba/hdb/hdb_samba4.so
%endif
%dir %{_libdir}/samba/krb5
%attr(755,root,root) %{_libdir}/samba/krb5/async_dns_krb5_locator.so
%dir %{_libdir}/samba/ldb
%attr(755,root,root) %{_libdir}/samba/ldb/aclread.so
%attr(755,root,root) %{_libdir}/samba/ldb/acl.so
%attr(755,root,root) %{_libdir}/samba/ldb/anr.so
%attr(755,root,root) %{_libdir}/samba/ldb/audit_log.so
%attr(755,root,root) %{_libdir}/samba/ldb/count_attrs.so
%attr(755,root,root) %{_libdir}/samba/ldb/descriptor.so
%attr(755,root,root) %{_libdir}/samba/ldb/dirsync.so
%attr(755,root,root) %{_libdir}/samba/ldb/dns_notify.so
%attr(755,root,root) %{_libdir}/samba/ldb/dsdb_notification.so
%attr(755,root,root) %{_libdir}/samba/ldb/encrypted_secrets.so
%attr(755,root,root) %{_libdir}/samba/ldb/extended_dn_in.so
%attr(755,root,root) %{_libdir}/samba/ldb/extended_dn_out.so
%attr(755,root,root) %{_libdir}/samba/ldb/extended_dn_store.so
%attr(755,root,root) %{_libdir}/samba/ldb/group_audit_log.so
%attr(755,root,root) %{_libdir}/samba/ldb/ildap.so
%attr(755,root,root) %{_libdir}/samba/ldb/instancetype.so
%attr(755,root,root) %{_libdir}/samba/ldb/lazy_commit.so
%attr(755,root,root) %{_libdir}/samba/ldb/ldbsamba_extensions.so
%attr(755,root,root) %{_libdir}/samba/ldb/linked_attributes.so
%attr(755,root,root) %{_libdir}/samba/ldb/new_partition.so
%attr(755,root,root) %{_libdir}/samba/ldb/objectclass_attrs.so
%attr(755,root,root) %{_libdir}/samba/ldb/objectclass.so
%attr(755,root,root) %{_libdir}/samba/ldb/objectguid.so
%attr(755,root,root) %{_libdir}/samba/ldb/operational.so
%attr(755,root,root) %{_libdir}/samba/ldb/paged_results.so
%attr(755,root,root) %{_libdir}/samba/ldb/partition.so
%attr(755,root,root) %{_libdir}/samba/ldb/password_hash.so
%attr(755,root,root) %{_libdir}/samba/ldb/ranged_results.so
%attr(755,root,root) %{_libdir}/samba/ldb/repl_meta_data.so
%attr(755,root,root) %{_libdir}/samba/ldb/resolve_oids.so
%attr(755,root,root) %{_libdir}/samba/ldb/rootdse.so
%attr(755,root,root) %{_libdir}/samba/ldb/samba3sam.so
%attr(755,root,root) %{_libdir}/samba/ldb/samba3sid.so
%attr(755,root,root) %{_libdir}/samba/ldb/samba_dsdb.so
%attr(755,root,root) %{_libdir}/samba/ldb/samba_secrets.so
%attr(755,root,root) %{_libdir}/samba/ldb/samldb.so
%attr(755,root,root) %{_libdir}/samba/ldb/schema_data.so
%attr(755,root,root) %{_libdir}/samba/ldb/schema_load.so
%attr(755,root,root) %{_libdir}/samba/ldb/secrets_tdb_sync.so
%attr(755,root,root) %{_libdir}/samba/ldb/show_deleted.so
%attr(755,root,root) %{_libdir}/samba/ldb/subtree_delete.so
%attr(755,root,root) %{_libdir}/samba/ldb/subtree_rename.so
%attr(755,root,root) %{_libdir}/samba/ldb/tombstone_reanimate.so
%attr(755,root,root) %{_libdir}/samba/ldb/unique_object_sids.so
%attr(755,root,root) %{_libdir}/samba/ldb/update_keytab.so
%attr(755,root,root) %{_libdir}/samba/ldb/vlv.so
%attr(755,root,root) %{_libdir}/samba/ldb/wins_ldb.so
%dir %{_libdir}/samba/process_model
%attr(755,root,root) %{_libdir}/samba/process_model/prefork.so
%attr(755,root,root) %{_libdir}/samba/process_model/standard.so
%dir %{_libdir}/samba/service
%attr(755,root,root) %{_libdir}/samba/service/cldap.so
%attr(755,root,root) %{_libdir}/samba/service/dcerpc.so
%attr(755,root,root) %{_libdir}/samba/service/dns.so
%attr(755,root,root) %{_libdir}/samba/service/dns_update.so
%attr(755,root,root) %{_libdir}/samba/service/drepl.so
%attr(755,root,root) %{_libdir}/samba/service/kcc.so
%attr(755,root,root) %{_libdir}/samba/service/kdc.so
%attr(755,root,root) %{_libdir}/samba/service/ldap.so
%attr(755,root,root) %{_libdir}/samba/service/nbtd.so
%attr(755,root,root) %{_libdir}/samba/service/ntp_signd.so
%attr(755,root,root) %{_libdir}/samba/service/s3fs.so
%attr(755,root,root) %{_libdir}/samba/service/winbindd.so
%attr(755,root,root) %{_libdir}/samba/service/wrepl.so
%dir %{_libdir}/samba/vfs
%attr(755,root,root) %{_libdir}/samba/vfs/acl_tdb.so
%attr(755,root,root) %{_libdir}/samba/vfs/acl_xattr.so
%attr(755,root,root) %{_libdir}/samba/vfs/aio_fork.so
%attr(755,root,root) %{_libdir}/samba/vfs/aio_pthread.so
%attr(755,root,root) %{_libdir}/samba/vfs/audit.so
%attr(755,root,root) %{_libdir}/samba/vfs/btrfs.so
%attr(755,root,root) %{_libdir}/samba/vfs/cap.so
%attr(755,root,root) %{_libdir}/samba/vfs/catia.so
%{?with_ceph:%attr(755,root,root) %{_libdir}/samba/vfs/ceph_snapshots.so}
%attr(755,root,root) %{_libdir}/samba/vfs/commit.so
%attr(755,root,root) %{_libdir}/samba/vfs/crossrename.so
%attr(755,root,root) %{_libdir}/samba/vfs/default_quota.so
%attr(755,root,root) %{_libdir}/samba/vfs/dfs_samba4.so
%attr(755,root,root) %{_libdir}/samba/vfs/dirsort.so
%attr(755,root,root) %{_libdir}/samba/vfs/expand_msdfs.so
%attr(755,root,root) %{_libdir}/samba/vfs/extd_audit.so
%attr(755,root,root) %{_libdir}/samba/vfs/fake_perms.so
%attr(755,root,root) %{_libdir}/samba/vfs/fileid.so
%attr(755,root,root) %{_libdir}/samba/vfs/fruit.so
%attr(755,root,root) %{_libdir}/samba/vfs/full_audit.so
%attr(755,root,root) %{_libdir}/samba/vfs/gpfs.so
%attr(755,root,root) %{_libdir}/samba/vfs/io_uring.so
%attr(755,root,root) %{_libdir}/samba/vfs/linux_xfs_sgid.so
%attr(755,root,root) %{_libdir}/samba/vfs/media_harmony.so
%attr(755,root,root) %{_libdir}/samba/vfs/offline.so
%attr(755,root,root) %{_libdir}/samba/vfs/posix_eadb.so
%attr(755,root,root) %{_libdir}/samba/vfs/preopen.so
%attr(755,root,root) %{_libdir}/samba/vfs/readahead.so
%attr(755,root,root) %{_libdir}/samba/vfs/readonly.so
%attr(755,root,root) %{_libdir}/samba/vfs/recycle.so
%attr(755,root,root) %{_libdir}/samba/vfs/snapper.so
%attr(755,root,root) %{_libdir}/samba/vfs/shadow_copy2.so
%attr(755,root,root) %{_libdir}/samba/vfs/shadow_copy.so
%attr(755,root,root) %{_libdir}/samba/vfs/shell_snap.so
%attr(755,root,root) %{_libdir}/samba/vfs/streams_depot.so
%attr(755,root,root) %{_libdir}/samba/vfs/streams_xattr.so
%attr(755,root,root) %{_libdir}/samba/vfs/syncops.so
%attr(755,root,root) %{_libdir}/samba/vfs/time_audit.so
%attr(755,root,root) %{_libdir}/samba/vfs/unityed_media.so
%attr(755,root,root) %{_libdir}/samba/vfs/virusfilter.so
%attr(755,root,root) %{_libdir}/samba/vfs/widelinks.so
%attr(755,root,root) %{_libdir}/samba/vfs/worm.so
%attr(755,root,root) %{_libdir}/samba/vfs/xattr_tdb.so
%dir %{_libexecdir}/samba
%attr(755,root,root) %{_libexecdir}/samba/rpcd_classic
%attr(755,root,root) %{_libexecdir}/samba/rpcd_epmapper
%attr(755,root,root) %{_libexecdir}/samba/rpcd_fsrvp
%attr(755,root,root) %{_libexecdir}/samba/rpcd_lsad
%attr(755,root,root) %{_libexecdir}/samba/rpcd_mdssvc
%attr(755,root,root) %{_libexecdir}/samba/rpcd_spoolss
%attr(755,root,root) %{_libexecdir}/samba/rpcd_winreg
%attr(755,root,root) %{_libexecdir}/samba/rpcd_witness
%attr(755,root,root) %{_libexecdir}/samba/samba-bgqd
%attr(755,root,root) %{_libexecdir}/samba/samba-dcerpcd
%dir %{_datadir}/samba/admx
%{_datadir}/samba/admx/GNOME_Settings.admx
%{_datadir}/samba/admx/samba.admx
%lang(en) %{_datadir}/samba/admx/en-US
%lang(ru) %{_datadir}/samba/admx/ru-RU
%if %{with spotlight}
%{_datadir}/samba/mdssvc
%endif
%{_datadir}/samba/setup
%{_mandir}/man1/oLschema2ldif.1*
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/samba.8*
%{_mandir}/man8/samba-bgqd.8*
%{_mandir}/man8/samba-dcerpcd.8*
%{_mandir}/man8/samba_downgrade_db.8*
%{_mandir}/man8/samba-gpupdate.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_aio_fork.8*
%{_mandir}/man8/vfs_aio_pthread.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_cap.8*
%{_mandir}/man8/vfs_catia.8*
%{?with_ceph:%{_mandir}/man8/vfs_ceph_snapshots.8*}
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_expand_msdfs.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_fruit.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_io_uring.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_media_harmony.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%{_mandir}/man8/vfs_snapper.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_time_audit.8*
%{_mandir}/man8/vfs_worm.8*
%{_mandir}/man8/vfs_xattr_tdb.8*
%{_mandir}/man8/vfs_offline.8*
%{_mandir}/man8/vfs_shell_snap.8*
%{_mandir}/man8/vfs_unityed_media.8*
%{_mandir}/man8/vfs_virusfilter.8*
%{_mandir}/man8/vfs_widelinks.8*

%dir %{_sambahome}
%dir /var/lib/samba
%ghost /var/lib/samba/*.dat
%dir /var/lib/samba/printing

%attr(750,root,root) %dir /var/log/samba
%attr(750,root,root) %dir /var/log/samba/cores
%attr(750,root,root) %dir /var/log/samba/cores/smbd
%attr(750,root,root) %dir /var/log/samba/cores/nmbd
%attr(750,root,root) %dir /var/log/archive/samba
%attr(1777,root,root) %dir /var/spool/samba

%if %{with ceph}
%files vfs-ceph
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/ceph.so
%attr(755,root,root) %{_libdir}/samba/vfs/ceph_new.so
%{_mandir}/man8/vfs_ceph.8*
%{_mandir}/man8/vfs_ceph_new.8*
%endif

%files vfs-glusterfs
%defattr(644,root,root,755)
%if %{with glusterfs}
%attr(755,root,root) %{_libdir}/samba/vfs/glusterfs.so
%{_mandir}/man8/vfs_glusterfs.8*
%endif
%attr(755,root,root) %{_libdir}/samba/vfs/glusterfs_fuse.so
%{_mandir}/man8/vfs_glusterfs_fuse.8*

%files common
%defattr(644,root,root,755)
%doc PFIF.txt README.cifs-utils README.md SECURITY.md WHATSNEW.txt
%dir %{_sysconfdir}/samba
%attr(664,root,fileshare) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samba/lmhosts
%attr(755,root,root) %{_bindir}/dbwrap_tool
%attr(755,root,root) %{_bindir}/net
%attr(755,root,root) %{_bindir}/nmblookup
%attr(755,root,root) %{_bindir}/reg*
%attr(755,root,root) %{_bindir}/samba-regedit
%attr(755,root,root) %{_bindir}/samba-tool
%attr(755,root,root) %{_bindir}/smbpasswd
%attr(755,root,root) %{_bindir}/testparm
%dir %{_libdir}/samba/auth
%attr(755,root,root) %{_libdir}/samba/auth/samba4.so
%dir %{_datadir}/samba
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/reg*.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/net.8*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/samba-tool.8*

%if %{without system_libs}
%attr(755,root,root) %{_bindir}/tdbbackup
%attr(755,root,root) %{_bindir}/tdbdump
%attr(755,root,root) %{_bindir}/tdbtool
%attr(755,root,root) %{_libdir}/samba/libtalloc.so.*
%attr(755,root,root) %{_libdir}/samba/libtdb.so.*
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbtool.8*
%endif

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cifsdd
%attr(755,root,root) %{_bindir}/mdsearch
%attr(755,root,root) %{_bindir}/mvxattr
%attr(755,root,root) %{_bindir}/rpcclient
%attr(755,root,root) %{_bindir}/smbcacls
%attr(755,root,root) %{_bindir}/smbclient
%attr(755,root,root) %{_bindir}/smbcquotas
%attr(755,root,root) %{_bindir}/smbtar
%attr(755,root,root) %{_bindir}/smbtree
%if %{with winexe}
%attr(755,root,root) %{_bindir}/winexe
%endif
%attr(755,root,root) %{_bindir}/wspsearch
%{_mandir}/man1/mdsearch.1*
%{_mandir}/man1/mvxattr.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%if %{with winexe}
%{_mandir}/man1/winexe.1*
%endif
%{_mandir}/man1/wspsearch.1*
%{_mandir}/man8/cifsdd.8*

%files winbind
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/winbind
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/winbind
%if %{with systemd}
%{systemdunitdir}/winbind.service
%endif
%attr(755,root,root) %{_bindir}/ntlm_auth
%attr(755,root,root) %{_bindir}/samba-log-parser
%attr(755,root,root) %{_bindir}/wbinfo
%attr(755,root,root) %{_sbindir}/winbindd
%attr(755,root,root) /%{_lib}/security/pam_winbind.so
%attr(755,root,root) /%{_lib}/libnss_winbind.so*
%dir %{_libdir}/samba/krb5
%attr(755,root,root) %{_libdir}/samba/krb5/winbind_krb5_locator.so
%attr(755,root,root) %{_libdir}/samba/libidmap-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libnss-info-private-samba.so
%dir %{_libdir}/samba/idmap
%attr(755,root,root) %{_libdir}/samba/idmap/ad.so
%attr(755,root,root) %{_libdir}/samba/idmap/autorid.so
%attr(755,root,root) %{_libdir}/samba/idmap/hash.so
%attr(755,root,root) %{_libdir}/samba/idmap/ldap.so
%attr(755,root,root) %{_libdir}/samba/idmap/rfc2307.so
%attr(755,root,root) %{_libdir}/samba/idmap/rid.so
%attr(755,root,root) %{_libdir}/samba/idmap/script.so
%attr(755,root,root) %{_libdir}/samba/idmap/tdb2.so
%dir %{_libdir}/samba/nss_info
%attr(755,root,root) %{_libdir}/samba/nss_info/hash.so
%attr(755,root,root) %{_libdir}/samba/nss_info/rfc2307.so
%attr(755,root,root) %{_libdir}/samba/nss_info/sfu20.so
%attr(755,root,root) %{_libdir}/samba/nss_info/sfu.so
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/samba-log-parser.1*
%{_mandir}/man1/wbinfo*.1*
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man8/idmap_ad.8*
%{_mandir}/man8/idmap_autorid.8*
%{_mandir}/man8/idmap_hash.8*
%{_mandir}/man8/idmap_ldap.8*
%{_mandir}/man8/idmap_nss.8*
%{_mandir}/man8/idmap_rfc2307.8*
%{_mandir}/man8/idmap_rid.8*
%{_mandir}/man8/idmap_script.8*
%{_mandir}/man8/idmap_tdb2.8*
%{_mandir}/man8/idmap_tdb.8*
%{_mandir}/man8/pam_winbind.8*
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man8/winbind_krb5_locator.8*
%attr(750,root,root) %dir /var/log/samba/cores/winbindd

%if %{with cups}
%files -n cups-backend-smb
%defattr(644,root,root,755)
%attr(755,root,root) %{cups_serverbin}/backend/smb
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/samba
%endif
%attr(755,root,root) %{_libexecdir}/samba/smbspool_krb5_wrapper
%attr(755,root,root) %{_bindir}/smbspool
%{_mandir}/man8/smbspool.8*
%{_mandir}/man8/smbspool_krb5_wrapper.8*
%endif

%files -n nss_wins
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_wins.so*

%files -n smbget
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smbget
%{_mandir}/man1/smbget.1*

%files libs
%defattr(644,root,root,755)
%if "%{_lib}" == "lib64"
/etc/ld.so.conf.d/samba64.conf
%else
/etc/ld.so.conf.d/samba.conf
%endif
%attr(755,root,root) %{_libdir}/libdcerpc-binding.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-binding.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-samr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-samr.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-server.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-server-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-server-core.so.0
%attr(755,root,root) %{_libdir}/libdcerpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc.so.0
%attr(755,root,root) %{_libdir}/libndr-krb5pac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-krb5pac.so.0
%attr(755,root,root) %{_libdir}/libndr-nbt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-nbt.so.0
%attr(755,root,root) %{_libdir}/libndr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr.so.6
%attr(755,root,root) %{_libdir}/libndr-standard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-standard.so.0
%attr(755,root,root) %{_libdir}/libsamba-credentials.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-credentials.so.1
%attr(755,root,root) %{_libdir}/libsamba-errors.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-errors.so.1
%attr(755,root,root) %{_libdir}/libsamba-hostconfig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-hostconfig.so.0
%attr(755,root,root) %{_libdir}/libsamba-passdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-passdb.so.0
%attr(755,root,root) %{_libdir}/libsamba-policy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-policy.so.0
%attr(755,root,root) %{_libdir}/libsamba-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-util.so.0
%attr(755,root,root) %{_libdir}/libsamdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamdb.so.0
%attr(755,root,root) %{_libdir}/libtevent-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtevent-util.so.0
%attr(755,root,root) %{_libdir}/libnetapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetapi.so.1
%attr(755,root,root) %{_libdir}/libsmbconf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsmbconf.so.0
%attr(755,root,root) %{_libdir}/libsmbldap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsmbldap.so.2
%dir %{_libdir}/samba

%if %{without replace}
%attr(755,root,root) %{_libdir}/samba/libreplace-private-samba.so
%endif
%if %{without system_heimdal}
%attr(755,root,root) %{_libdir}/samba/libasn1-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcom-err-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgssapi-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libhcrypto-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libhdb-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libheimbase-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libheimntlm-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libhx509-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libkdc-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libkrb5-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libroken-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libwind-private-samba.so
%endif
%attr(755,root,root) %{_libdir}/samba/libad-claims-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libaddns-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libads-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libasn1util-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libauth4-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libauthkrb5-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libauth-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libauth-unix-token-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libauthn-policy-util-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libCHARSET3-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcliauth-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libclidns-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcli-cldap-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcli-ldap-common-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcli-ldap-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcli-nbt-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcli-smb-common-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcli-spoolss-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcluster-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcmdline-contexts-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcmdline-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libcommon-auth-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libctdb-event-client-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdb-glue-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-pkt-auth-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdbwrap-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-samba-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-samba4-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdfs-server-ad-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdnsserver-common-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdsdb-garbage-collect-tombstones-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libdsdb-module-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libevents-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libflag-mapping-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgenrand-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgensec-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgpext-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgpo-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgse-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libgss-preauth-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libHDB-SAMBA4-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libhttp-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libinterfaces-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libiov-buf-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libkrb5samba-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libldbsamba-private-samba.so
%attr(755,root,root) %{_libdir}/samba/liblibcli-lsa3-private-samba.so
%attr(755,root,root) %{_libdir}/samba/liblibcli-netlogon3-private-samba.so
%attr(755,root,root) %{_libdir}/samba/liblibsmb-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libLIBWBCLIENT-OLD-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libmessages-dgm-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libmessages-util-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libMESSAGING-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libMESSAGING-SEND-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libmscat-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libmsghdr-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libmsrpc3-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libndr-samba-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libndr-samba4-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libnetif-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libnet-keytab-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libnpa-tstream-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libpac-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libposix-eadb-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libprinter-driver-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libprinting-migrate-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libprocess-model-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libREG-FULL-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libregistry-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libRPC-SERVER-LOOP-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libRPC-WORKER-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba3-util-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-cluster-support-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-debug-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-modules-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-net-join.cpython-3*-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-net-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-python.cpython-3*-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-security-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamba-sockets-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsamdb-common-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libscavenge-dns-records-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsecrets3-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libserver-id-db-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libserver-role-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libservice-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libshares-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsmbclient-raw-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsmbd-base-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsmbd-shim-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsmbldaphelper-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsmbpasswdparser-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsmb-transport-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsocket-blocking-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libstable-sort-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libsys-rw-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libtalloc-report-printf-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libtalloc-report-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libtdb-wrap-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libtime-basic-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libutil-crypt-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libutil-reg-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libutil-setid-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libutil-tdb-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libxattr-tdb-private-samba.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/samba-4.0/charset.h
%dir %{_includedir}/samba-4.0/core
%{_includedir}/samba-4.0/core/doserr.h
%{_includedir}/samba-4.0/core/error.h
%{_includedir}/samba-4.0/core/hresult.h
%{_includedir}/samba-4.0/core/ntstatus.h
%{_includedir}/samba-4.0/core/ntstatus_gen.h
%{_includedir}/samba-4.0/core/werror.h
%{_includedir}/samba-4.0/core/werror_gen.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/dcerpc_server.h
%{_includedir}/samba-4.0/dcesrv_core.h
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
%{_includedir}/samba-4.0/gen_ndr/claims.h
%{_includedir}/samba-4.0/gen_ndr/dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/lsa.h
%{_includedir}/samba-4.0/gen_ndr/misc.h
%{_includedir}/samba-4.0/gen_ndr/nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/ndr_misc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl_c.h
%{_includedir}/samba-4.0/gen_ndr/netlogon.h
%{_includedir}/samba-4.0/gen_ndr/samr.h
%{_includedir}/samba-4.0/gen_ndr/security.h
%{_includedir}/samba-4.0/gen_ndr/server_id.h
%{_includedir}/samba-4.0/gen_ndr/svcctl.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/ndr/ndr_nbt.h
%{_includedir}/samba-4.0/ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/rpc_common.h
%dir %{_includedir}/samba-4.0/samba
%{_includedir}/samba-4.0/samba/session.h
%{_includedir}/samba-4.0/samba/version.h
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/attr.h
%{_includedir}/samba-4.0/util/blocking.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/discard.h
%{_includedir}/samba-4.0/util/fault.h
%{_includedir}/samba-4.0/util/genrand.h
%{_includedir}/samba-4.0/util/idtree.h
%{_includedir}/samba-4.0/util/idtree_random.h
%{_includedir}/samba-4.0/util/signal.h
%{_includedir}/samba-4.0/util/substitute.h
%{_includedir}/samba-4.0/util/tevent_ntstatus.h
%{_includedir}/samba-4.0/util/tevent_unix.h
%{_includedir}/samba-4.0/util/tevent_werror.h
%{_includedir}/samba-4.0/util/tfork.h
%{_includedir}/samba-4.0/util/time.h
%{_includedir}/samba-4.0/util_ldb.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/netapi.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/smb3posix.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%attr(755,root,root) %{_libdir}/libdcerpc-binding.so
%attr(755,root,root) %{_libdir}/libdcerpc-samr.so
%attr(755,root,root) %{_libdir}/libdcerpc-server.so
%attr(755,root,root) %{_libdir}/libdcerpc-server-core.so
%attr(755,root,root) %{_libdir}/libdcerpc.so
%attr(755,root,root) %{_libdir}/libndr-krb5pac.so
%attr(755,root,root) %{_libdir}/libndr-nbt.so
%attr(755,root,root) %{_libdir}/libndr.so
%attr(755,root,root) %{_libdir}/libndr-standard.so
%attr(755,root,root) %{_libdir}/libnetapi.so
%attr(755,root,root) %{_libdir}/libsamba-credentials.so
%attr(755,root,root) %{_libdir}/libsamba-errors.so
%attr(755,root,root) %{_libdir}/libsamba-hostconfig.so
%attr(755,root,root) %{_libdir}/libsamba-passdb.so
%attr(755,root,root) %{_libdir}/libsamba-policy.so
%attr(755,root,root) %{_libdir}/libsamba-util.so
%attr(755,root,root) %{_libdir}/libsamdb.so
%attr(755,root,root) %{_libdir}/libsmbconf.so
%attr(755,root,root) %{_libdir}/libsmbldap.so
%attr(755,root,root) %{_libdir}/libtevent-util.so
%{_pkgconfigdir}/dcerpc.pc
%{_pkgconfigdir}/dcerpc_samr.pc
%{_pkgconfigdir}/dcerpc_server.pc
%{_pkgconfigdir}/ndr.pc
%{_pkgconfigdir}/ndr_krb5pac.pc
%{_pkgconfigdir}/ndr_nbt.pc
%{_pkgconfigdir}/ndr_standard.pc
%{_pkgconfigdir}/netapi.pc
%{_pkgconfigdir}/samba-credentials.pc
%{_pkgconfigdir}/samba-hostconfig.pc
%{_pkgconfigdir}/samba-policy.pc
%{_pkgconfigdir}/samba-util.pc
%{_pkgconfigdir}/samdb.pc

%files pidl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pidl
%{_mandir}/man1/pidl.1*
%{_mandir}/man3/Parse::Pidl*.3*
%{perl_vendorlib}/Parse/Pidl*

%files -n python3-samba
%defattr(644,root,root,755)
%dir %{py3_sitedir}/samba
%{py3_sitedir}/samba/*.py
%{py3_sitedir}/samba/__pycache__
%attr(755,root,root) %{py3_sitedir}/samba/*.so
%dir %{py3_sitedir}/samba/dcerpc
%{py3_sitedir}/samba/dcerpc/*.py
%{py3_sitedir}/samba/dcerpc/__pycache__
%attr(755,root,root) %{py3_sitedir}/samba/dcerpc/*.so
%dir %{py3_sitedir}/samba/domain
%{py3_sitedir}/samba/domain/*.py
%{py3_sitedir}/samba/domain/__pycache__
%dir %{py3_sitedir}/samba/domain/models
%{py3_sitedir}/samba/domain/models/*.py
%{py3_sitedir}/samba/domain/models/__pycache__
%dir %{py3_sitedir}/samba/emulate
%{py3_sitedir}/samba/emulate/*.py
%{py3_sitedir}/samba/emulate/__pycache__
%dir %{py3_sitedir}/samba/gp
%{py3_sitedir}/samba/gp/*.py
%{py3_sitedir}/samba/gp/__pycache__
%dir %{py3_sitedir}/samba/gp/util
%{py3_sitedir}/samba/gp/util/*.py
%{py3_sitedir}/samba/gp/util/__pycache__
%dir %{py3_sitedir}/samba/gp_parse
%{py3_sitedir}/samba/gp_parse/*.py
%{py3_sitedir}/samba/gp_parse/__pycache__
%dir %{py3_sitedir}/samba/kcc
%{py3_sitedir}/samba/kcc/*.py
%{py3_sitedir}/samba/kcc/__pycache__
%dir %{py3_sitedir}/samba/netcmd
%{py3_sitedir}/samba/netcmd/*.py
%{py3_sitedir}/samba/netcmd/__pycache__
%dir %{py3_sitedir}/samba/netcmd/domain
%{py3_sitedir}/samba/netcmd/domain/*.py
%{py3_sitedir}/samba/netcmd/domain/__pycache__
%dir %{py3_sitedir}/samba/netcmd/domain/auth
%{py3_sitedir}/samba/netcmd/domain/auth/*.py
%{py3_sitedir}/samba/netcmd/domain/auth/__pycache__
%dir %{py3_sitedir}/samba/netcmd/domain/auth/policy
%{py3_sitedir}/samba/netcmd/domain/auth/policy/*.py
%{py3_sitedir}/samba/netcmd/domain/auth/policy/__pycache__
%dir %{py3_sitedir}/samba/netcmd/domain/auth/silo
%{py3_sitedir}/samba/netcmd/domain/auth/silo/*.py
%{py3_sitedir}/samba/netcmd/domain/auth/silo/__pycache__
%dir %{py3_sitedir}/samba/netcmd/domain/claim
%{py3_sitedir}/samba/netcmd/domain/claim/*.py
%{py3_sitedir}/samba/netcmd/domain/claim/__pycache__
%dir %{py3_sitedir}/samba/netcmd/domain/kds
%{py3_sitedir}/samba/netcmd/domain/kds/*.py
%{py3_sitedir}/samba/netcmd/domain/kds/__pycache__
%dir %{py3_sitedir}/samba/netcmd/service_account
%{py3_sitedir}/samba/netcmd/service_account/*.py
%{py3_sitedir}/samba/netcmd/service_account/__pycache__
%dir %{py3_sitedir}/samba/netcmd/user
%{py3_sitedir}/samba/netcmd/user/*.py
%{py3_sitedir}/samba/netcmd/user/__pycache__
%dir %{py3_sitedir}/samba/netcmd/user/auth
%{py3_sitedir}/samba/netcmd/user/auth/*.py
%{py3_sitedir}/samba/netcmd/user/auth/__pycache__
%dir %{py3_sitedir}/samba/netcmd/user/readpasswords
%{py3_sitedir}/samba/netcmd/user/readpasswords/*.py
%{py3_sitedir}/samba/netcmd/user/readpasswords/__pycache__
%dir %{py3_sitedir}/samba/provision
%{py3_sitedir}/samba/provision/*.py
%{py3_sitedir}/samba/provision/__pycache__
%dir %{py3_sitedir}/samba/samba3
%{py3_sitedir}/samba/samba3/*.py
%{py3_sitedir}/samba/samba3/__pycache__
%attr(755,root,root) %{py3_sitedir}/samba/samba3/*.so
%dir %{py3_sitedir}/samba/subunit
%{py3_sitedir}/samba/subunit/*.py
%{py3_sitedir}/samba/subunit/__pycache__
%dir %{py3_sitedir}/samba/tests
%{py3_sitedir}/samba/tests/*.py
%{py3_sitedir}/samba/tests/__pycache__
%dir %{py3_sitedir}/samba/tests/blackbox
%{py3_sitedir}/samba/tests/blackbox/*.py
%{py3_sitedir}/samba/tests/blackbox/__pycache__
%dir %{py3_sitedir}/samba/tests/dcerpc
%{py3_sitedir}/samba/tests/dcerpc/*.py
%{py3_sitedir}/samba/tests/dcerpc/__pycache__
%dir %{py3_sitedir}/samba/tests/dns_forwarder_helpers
%{py3_sitedir}/samba/tests/dns_forwarder_helpers/*.py
%{py3_sitedir}/samba/tests/dns_forwarder_helpers/__pycache__
%dir %{py3_sitedir}/samba/tests/kcc
%{py3_sitedir}/samba/tests/kcc/*.py
%{py3_sitedir}/samba/tests/kcc/__pycache__
%dir %{py3_sitedir}/samba/tests/krb5
%{py3_sitedir}/samba/tests/krb5/*.py
%{py3_sitedir}/samba/tests/krb5/__pycache__
%dir %{py3_sitedir}/samba/tests/samba_tool
%{py3_sitedir}/samba/tests/samba_tool/*.py
%{py3_sitedir}/samba/tests/samba_tool/__pycache__
%dir %{py3_sitedir}/samba/tests/emulate
%{py3_sitedir}/samba/tests/emulate/*.py
%{py3_sitedir}/samba/tests/emulate/__pycache__
%dir %{py3_sitedir}/samba/tests/ndr
%{py3_sitedir}/samba/tests/ndr/*.py
%{py3_sitedir}/samba/tests/ndr/__pycache__
%if %{without system_libs}
%attr(755,root,root) %{py3_sitedir}/ldb.so
%attr(755,root,root) %{py3_sitedir}/talloc.so
%attr(755,root,root) %{py3_sitedir}/tdb.so
%attr(755,root,root) %{py3_sitedir}/_tevent.so
%endif

%files test
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gentest
%attr(755,root,root) %{_bindir}/locktest
%attr(755,root,root) %{_bindir}/masktest
%attr(755,root,root) %{_bindir}/ndrdump
%attr(755,root,root) %{_bindir}/smbtorture
%attr(755,root,root) %{_libdir}/samba/libdlz-bind9-for-torture-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libtorture-private-samba.so
%{_mandir}/man1/gentest.1*
%{_mandir}/man1/locktest.1*
%{_mandir}/man1/masktest.1*
%{_mandir}/man1/ndrdump.1*
%{_mandir}/man1/smbtorture.1*

%files -n libsmbclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so.*
%attr(755,root,root) %{_libdir}/libwbclient.so.*
%{_mandir}/man7/libsmbclient.7*

%files -n libsmbclient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so
%attr(755,root,root) %{_libdir}/libwbclient.so
%dir %{_includedir}/samba-4.0
%{_includedir}/samba-4.0/libsmbclient.h
%{_includedir}/samba-4.0/wbclient.h
%{_pkgconfigdir}/smbclient.pc
%{_pkgconfigdir}/wbclient.pc

%if %{with ldap}
%files -n openldap-schema-samba
%defattr(644,root,root,755)
%{schemadir}/samba.schema
%endif

%files -n ctdb
%defattr(644,root,root,755)
%doc ctdb/README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ctdb
%{_sysconfdir}/ctdb/notify.sh
%{_sysconfdir}/ctdb/debug-hung-script.sh
%{_sysconfdir}/ctdb/ctdb-backup-persistent-tdbs.sh
%{_sysconfdir}/ctdb/ctdb-crash-cleanup.sh
%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/debug_locks.sh
%dir %{_localstatedir}/lib/ctdb

%if %{with systemd}
%{systemdunitdir}/ctdb.service
%endif

%dir %{_sysconfdir}/ctdb
%{_sysconfdir}/ctdb/statd-callout
# CTDB scripts, no config files
# script with executable bit means activated
%dir %{_sysconfdir}/ctdb/nfs-checks.d
%{_sysconfdir}/ctdb/nfs-checks.d/00.portmapper.check
%{_sysconfdir}/ctdb/nfs-checks.d/10.status.check
%{_sysconfdir}/ctdb/nfs-checks.d/20.nfs.check
%{_sysconfdir}/ctdb/nfs-checks.d/30.nlockmgr.check
%{_sysconfdir}/ctdb/nfs-checks.d/40.mountd.check
%{_sysconfdir}/ctdb/nfs-checks.d/50.rquotad.check
%{_sysconfdir}/ctdb/nfs-checks.d/README
%{_sysconfdir}/ctdb/nfs-linux-kernel-callout
# CTDB scripts, no config files
# script with executable bit means activated
%dir %{_sysconfdir}/ctdb/events
%dir %{_sysconfdir}/ctdb/events/legacy
%dir %{_sysconfdir}/ctdb/events/notification
%{_sysconfdir}/ctdb/events/notification/README
%dir %{_datadir}/ctdb
%dir %{_datadir}/ctdb/events
%dir %{_datadir}/ctdb/events/legacy
%{_datadir}/ctdb/events/legacy/00.ctdb.script
%{_datadir}/ctdb/events/legacy/01.reclock.script
%{_datadir}/ctdb/events/legacy/05.system.script
%{_datadir}/ctdb/events/legacy/10.interface.script
%{_datadir}/ctdb/events/legacy/11.natgw.script
%{_datadir}/ctdb/events/legacy/11.routing.script
%{_datadir}/ctdb/events/legacy/13.per_ip_routing.script
%{_datadir}/ctdb/events/legacy/20.multipathd.script
%{_datadir}/ctdb/events/legacy/31.clamd.script
%{_datadir}/ctdb/events/legacy/40.vsftpd.script
%{_datadir}/ctdb/events/legacy/41.httpd.script
%{_datadir}/ctdb/events/legacy/46.update-keytabs.script
%{_datadir}/ctdb/events/legacy/47.samba-dcerpcd.script
%{_datadir}/ctdb/events/legacy/48.netbios.script
%{_datadir}/ctdb/events/legacy/49.winbind.script
%{_datadir}/ctdb/events/legacy/50.samba.script
%{_datadir}/ctdb/events/legacy/60.nfs.script
%{_datadir}/ctdb/events/legacy/70.iscsi.script
%{_datadir}/ctdb/events/legacy/91.lvs.script
%{_datadir}/ctdb/events/legacy/95.database.script
%dir %{_datadir}/ctdb/scripts
%attr(755,root,root) %{_datadir}/ctdb/scripts/winbind_ctdb_updatekeytab.sh
%{systemdtmpfilesdir}/ctdb.conf
%attr(755,root,root) %{_sbindir}/ctdbd
%attr(755,root,root) %{_bindir}/ctdb
%attr(755,root,root) %{_bindir}/ping_pong
%attr(755,root,root) %{_bindir}/ltdbtool
%attr(755,root,root) %{_bindir}/ctdb_diagnostics
%attr(755,root,root) %{_bindir}/onnode
%dir %{_libexecdir}/ctdb
%{_libexecdir}/ctdb/ctdb_natgw
%{_libexecdir}/ctdb/ctdb_recovery_helper
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-config
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-event
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-eventd
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_killtcp
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_lock_helper
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_lvs
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_mutex_fcntl_helper
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_smnotify_helper
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-path
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_takeover_helper
%attr(755,root,root) %{_libexecdir}/ctdb/statd_callout
%attr(755,root,root) %{_libexecdir}/ctdb/statd_callout_helper
%attr(755,root,root) %{_libexecdir}/ctdb/tdb_mutex_check

%{_mandir}/man1/ctdb.1*
%{_mandir}/man1/ctdb_diagnostics.1*
%{_mandir}/man1/ctdbd.1*
%{_mandir}/man1/onnode.1*
%{_mandir}/man1/ltdbtool.1*
%{_mandir}/man1/ping_pong.1*
%{_mandir}/man5/ctdb-script.options.5*
%{_mandir}/man5/ctdb.conf.5*
%{_mandir}/man5/ctdb.sysconfig.5*
%{_mandir}/man7/ctdb.7*
%{_mandir}/man7/ctdb-tunables.7*
%{_mandir}/man7/ctdb-statistics.7*

%if %{with ctdb_pcp}
%files -n pcp-ctdb
%defattr(644,root,root,755)
%dir /var/lib/pcp/pmdas/ctdb
%doc /var/lib/pcp/pmdas/ctdb/README
%attr(755,root,root) /var/lib/pcp/pmdas/ctdb/Install
%attr(755,root,root) /var/lib/pcp/pmdas/ctdb/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/ctdb/pmdactdb
/var/lib/pcp/pmdas/ctdb/domain.h
/var/lib/pcp/pmdas/ctdb/help
/var/lib/pcp/pmdas/ctdb/pmns
%endif

%files -n ldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldb.so.2
%attr(755,root,root) %{_libdir}/samba/libldb-key-value-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libldb-tdb-err-map-private-samba.so
%attr(755,root,root) %{_libdir}/samba/libldb-tdb-int-private-samba.so
%{?with_lmdb:%attr(755,root,root) %{_libdir}/samba/libldb-mdb-int-private-samba.so}
%dir %{_libdir}/samba/ldb
%attr(755,root,root) %{_libdir}/samba/ldb/*.so

%files -n ldb-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldbadd
%attr(755,root,root) %{_bindir}/ldbdel
%attr(755,root,root) %{_bindir}/ldbedit
%attr(755,root,root) %{_bindir}/ldbmodify
%attr(755,root,root) %{_bindir}/ldbrename
%attr(755,root,root) %{_bindir}/ldbsearch
%attr(755,root,root) %{_libdir}/samba/libldb-cmdline-private-samba.so
%{_mandir}/man1/ldbadd.1*
%{_mandir}/man1/ldbdel.1*
%{_mandir}/man1/ldbedit.1*
%{_mandir}/man1/ldbmodify.1*
%{_mandir}/man1/ldbrename.1*
%{_mandir}/man1/ldbsearch.1*

%files -n ldb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libldb.so
%{_includedir}/samba-4.0/ldb_module.h
%{_includedir}/samba-4.0/ldb_handlers.h
%{_includedir}/samba-4.0/ldb_errors.h
%{_includedir}/samba-4.0/ldb_version.h
%{_includedir}/samba-4.0/ldb.h
%{_pkgconfigdir}/ldb.pc
%{_mandir}/man3/ldb.3*

%files -n python3-ldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/libpyldb-util.cpython-3*-private-samba.so
%attr(755,root,root) %{py3_sitedir}/ldb.cpython-*.so
%{py3_sitedir}/_ldb_text.py
%{py3_sitedir}/__pycache__/_ldb_text.cpython-*.py[co]
