# TODO: tracker support (--enable-spotlight)?
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
%bcond_without	ldap		# LDAP support
%bcond_without	avahi		# Avahi support
%bcond_without	dmapi		# DMAPI support
%bcond_without	python2		# without Python2 bindings
%bcond_without	systemd		# systemd integration
%bcond_with	system_heimdal	# Use system Heimdal libraries [since samba 4.4.x build fails with heimdal 1.5.x/7.x]
%bcond_with	system_libbsd	# system libbsd for MD5 and strl* functions
%bcond_without	system_libs	# system libraries from SAMBA project (talloc,tdb,tevent,ldb)
%bcond_without	ctdb_pcp	# Performance Co-Pilot support for CTDB
# turn on when https://bugzilla.samba.org/show_bug.cgi?id=11764 is fixed
%bcond_with	replace

%if %{with system_libs}
%define		ldb_ver		1.5.5
%define		talloc_ver	2:2.1.16
%define		tdb_ver		2:1.3.18
%define		tevent_ver	0.9.39
%endif

# dmapi-devel with xfsprogs-devel >= 4.11(?) needs largefile (64bit off_t) that isn't detected properly
%ifarch %{ix86}
%undefine	with_dmapi
%endif

%include	/usr/lib/rpm/macros.perl

# NOTE: packages order is: server + additions, common, clients, libs+devel, ldap
%define		virusfilter_version 0.1.4
Summary:	Samba Active Directory and SMB server
Summary(pl.UTF-8):	Serwer Samba Active Directory i SMB
Name:		samba
Version:	4.10.8
Release:	1
Epoch:		1
License:	GPL v3
Group:		Networking/Daemons
Source0:	https://download.samba.org/pub/samba/stable/%{name}-%{version}.tar.gz
# Source0-md5:	f3c722bbcd903479008fa1b529f56365
Source1:	smb.init
Source2:	samba.pamd
Source4:	samba.sysconfig
Source5:	samba.logrotate
Source6:	smb.conf
Source7:	winbind.init
Source8:	winbind.sysconfig
Source9:	samba.init
Source10:	https://bitbucket.org/fumiyas/samba-virusfilter/downloads/samba-virusfilter-%{virusfilter_version}.tar.bz2
# Source10-md5:	4bef017601d87f52f8c82819a3ff56ee
Patch0:		system-heimdal.patch
Patch1:		%{name}-c++-nofail.patch
Patch2:		%{name}-lprng-no-dot-printers.patch

Patch4:		unicodePwd-nthash-values-over-LDAP.patch
Patch5:		%{name}-heimdal.patch
Patch6:		server-role.patch
Patch7:		%{name}-bug-9816.patch
Patch8:		%{name}-no_libbsd.patch
URL:		https://www.samba.org/
BuildRequires:	acl-devel
%{?with_avahi:BuildRequires:	avahi-devel}
%{?with_ceph:BuildRequires:	ceph-devel >= 0.73}
BuildRequires:	cmocka-devel >= 1.1.3
%{?with_cups:BuildRequires:	cups-devel >= 1:1.2.0}
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	dbus-devel
%{?with_dmapi:BuildRequires:	dmapi-devel}
BuildRequires:	docbook-style-xsl-nons
# just FAM API
BuildRequires:	gamin-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext-tools
BuildRequires:	glusterfs-devel
BuildRequires:	gnutls-devel >= 3.0.0
%{?with_system_heimdal:BuildRequires:	heimdal-devel >= 1.5.3-1}
BuildRequires:	iconv
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	libarchive-devel >= 3.1.2
%{?with_system_libbsd:BuildRequires:	libbsd-devel}
BuildRequires:	libcap-devel
BuildRequires:	libcom_err-devel
BuildRequires:	libmagic-devel
BuildRequires:	libnscd-devel
BuildRequires:	make >= 3.81
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	ncurses-ext-devel >= 5.2
BuildRequires:	nss_wrapper >= 1.0.2
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
BuildRequires:	pam-devel >= 0.99.8.1
%{?with_ctdb_pcp:BuildRequires:	pcp-devel}
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Parse-Yapp >= 1.05
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5.0
BuildRequires:	python-dns
BuildRequires:	python-iso8601
BuildRequires:	python-modules >= 1:2.5.0
BuildRequires:	python-subunit
BuildRequires:	python-testtools
%else
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-dns
BuildRequires:	python3-iso8601
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-subunit
BuildRequires:	python3-testtools
%endif
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	sed >= 4.0
BuildRequires:	socket_wrapper >= 1.1.2
BuildRequires:	subunit-devel
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	xfsprogs-devel
BuildRequires:	zlib-devel >= 1.2.3
%if %{with system_libs}
BuildRequires:	ldb-devel >= %{ldb_ver}
	%if %{with python2}
BuildRequires:	python-ldb-devel >= %{ldb_ver}
BuildRequires:	python-talloc-devel >= %{talloc_ver}
BuildRequires:	python-tdb >= %{tdb_ver}
BuildRequires:	python-tevent >= %{tevent_ver}
	%endif
BuildRequires:	python3-ldb-devel >= %{ldb_ver}
BuildRequires:	python3-talloc-devel >= %{talloc_ver}
BuildRequires:	python3-tdb >= %{tdb_ver}
BuildRequires:	python3-tevent >= %{tevent_ver}
BuildRequires:	talloc-devel >= %{talloc_ver}
BuildRequires:	tdb-devel >= %{tdb_ver}
BuildRequires:	tevent-devel >= %{tevent_ver}
%endif
BuildRequires:	uid_wrapper >= 1.1.0
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
Obsoletes:	samba-doc-html
Obsoletes:	samba-doc-pdf
Obsoletes:	samba-pdb-xml
Obsoletes:	samba-vfs-audit
Obsoletes:	samba-vfs-block
Obsoletes:	samba-vfs-cap
Obsoletes:	samba-vfs-catia
Obsoletes:	samba-vfs-default_quota
Obsoletes:	samba-vfs-expand_msdfs
Obsoletes:	samba-vfs-fake_perms
Obsoletes:	samba-vfs-netatalk
Obsoletes:	samba-vfs-readahead
Obsoletes:	samba-vfs-readonly
Obsoletes:	samba-vfs-recycle
Obsoletes:	samba-vfs-scannedonly
Obsoletes:	samba-vfs-shadow_copy
Obsoletes:	samba3
Obsoletes:	samba3-server
Obsoletes:	samba3-vfs-audit
Obsoletes:	samba3-vfs-cap
Obsoletes:	samba3-vfs-catia
Obsoletes:	samba3-vfs-default_quota
Obsoletes:	samba3-vfs-expand_msdfs
Obsoletes:	samba3-vfs-fake_perms
Obsoletes:	samba3-vfs-netatalk
Obsoletes:	samba3-vfs-readahead
Obsoletes:	samba3-vfs-readonly
Obsoletes:	samba3-vfs-recycle
Obsoletes:	samba3-vfs-scannedonly
Obsoletes:	samba3-vfs-shadow_copy
Obsoletes:	samba4
Obsoletes:	samba4-common-server
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
Obsoletes:	samba3-common
Obsoletes:	samba4-common

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
Obsoletes:	samba3-client
Obsoletes:	samba4-client
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
Obsoletes:	samba3-winbind
Obsoletes:	samba4-winbind
# pam_winbind is not complete replacement, but pam_smbpass has been removed (in samba 4.4)
#Obsoletes:	pam-pam_smbpass

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
Obsoletes:	cups-backend-smb3

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
Obsoletes:	nss_wins3

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
Obsoletes:	smbget3

%description -n smbget
wget-like utility for downloading files over SMB.

%description -n smbget -l pl.UTF-8
Narzędzie podobne do wgeta do pobierania plików protokołem SMB
używanym w sieciach MS Windows.

%package libs
Summary:	Samba shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Samby
Group:		Libraries
Requires:	gnutls >= 3.0.0
%if %{with system_libs}
Requires:	ldb >= %{ldb_ver}
Requires:	talloc >= %{talloc_ver}
Requires:	tdb >= %{tdb_ver}
Requires:	tevent >= %{tevent_ver}
%endif
Obsoletes:	samba-vfs-notify_fam

%description libs
Samba shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Samby.

%package devel
Summary:	Header files for Samba
Summary(pl.UTF-8):	Pliki nagłówkowe Samby
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	samba3-devel
Obsoletes:	samba4-devel

%description devel
Header files for Samba.

%description devel -l pl.UTF-8
Pliki nagłówkowe Samby.

%package pidl
Summary:	Perl IDL compiler
Summary(pl.UTF-8):	Kompilator IDL w Perlu
Group:		Development/Tools
Obsoletes:	samba4-pidl

%description pidl
The samba-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols.

%description pidl -l pl.UTF-8
Ten pakiet zawiera kompilator IDL napisany w Perlu, używany przez
Sambę oraz Wiresharka to analizy IDL i podobnych protokołów.

%package -n python-samba
Summary:	Samba modules for Python
Summary(pl.UTF-8):	Moduły Samby dla Pythona
Group:		Development/Languages/Python
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	python
Requires:	python-dns
Requires:	python-iso8601
Requires:	python-modules
%if %{with system_libs}
Requires:	python-ldb >= %{ldb_ver}
Requires:	python-talloc >= %{talloc_ver}
Requires:	python-tevent >= %{tevent_ver}
%endif
Obsoletes:	python-samba4

%description -n python-samba
Samba modules for Python.

%description -n python-samba -l pl.UTF-8
Moduły Samby dla Pythona.

%package -n python3-samba
Summary:	Samba modules for Python 3
Summary(pl.UTF-8):	Moduły Samby dla Pythona 3
Group:		Development/Languages/Python
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	python3
Requires:	python3-dns
Requires:	python3-iso8601
Requires:	python3-modules
%if %{with system_libs}
Requires:	python3-ldb >= %{ldb_ver}
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
Obsoletes:	samba4-test
Obsoletes:	samba4-test-devel
Obsoletes:	samba-test-devel

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
Obsoletes:	samba3-libsmbclient

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
Obsoletes:	libsmbclient-static
Obsoletes:	samba3-libsmbclient-devel

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
Obsoletes:	openldap-schema-samba3
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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

%description -l pl.UTF-8
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

%prep
%setup -q
%{?with_system_heimdal:%patch0 -p1}
%patch1 -p1
%patch2 -p1

%patch4 -p1
%{?with_system_heimdal:%patch5 -p1}
%patch6 -p1
%patch7 -p1
%{!?with_system_libbsd:%patch8 -p1}

%{__sed} -i -e 's|#!/usr/bin/env python|#!/usr/bin/python|' source4/scripting/bin/samba*
%{__sed} -i -e 's|#!/usr/bin/env perl|#!/usr/bin/perl|' pidl/pidl

%if %{with system_heimdal}
%{__mv} source4/heimdal_build/krb5-types{,-smb}.h
%endif

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
	--builtin-libraries=%{?with_replace:replace,}ccan,samba-cluster-support \
	--bundled-libraries=NONE,iniparser,%{!?with_system_libs:talloc,tdb,ldb,tevent,pytalloc,pytalloc-util,pytdb,pytevent,pyldb,pyldb-util},%{!?with_system_heimdal:roken,wind,hx509,asn1,heimbase,hcrypto,krb5,gssapi,heimntlm,hdb,kdc,com_err,compile_et,asn1_compile} \
	--with-shared-modules=idmap_ad,idmap_adex,idmap_hash,idmap_ldap,idmap_rid,idmap_tdb2,auth_samba4,vfs_dfs_samba4 \
	--with-cluster-support \
	--with-acl-support \
	--with%{!?with_ads:out}-ads \
	%{?with_ctdb_pcp:--enable-pmda} \
	--with-automount \
	--with%{!?with_dmapi:out}-dmapi \
	--with-dnsupdate \
	%{?with_python2:--extra-python=/usr/bin/python2} \
	--with-iconv \
	--with%{!?with_ldap:out}-ldap \
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
	--%{?with_avahi:en}%{!?with_avahi:dis}able-avahi \
	--enable-cups \
	--enable-iprint

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
	$RPM_BUILD_ROOT/var/log/samba/cores/{smbd,nmbd} \
	$RPM_BUILD_ROOT{/sbin,/%{_lib}/security,%{_libdir},%{_libdir}/samba/vfs,%{_includedir},%{_sambahome},%{schemadir}} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CONFIGDIR=$RPM_BUILD_ROOT%{_sysconfdir}/samba

# Undo the PIDL install, we want to try again with the right options.
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/perl5

# Install PIDL
%{__make} -C pidl install \
	PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

# Clean out crap left behind by the PIDL install
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/wscript_build
%{__rm} -r $RPM_BUILD_ROOT%{perl_vendorlib}/Parse/Yapp
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Parse/Pidl/.packlist

install -p source3/script/mksmbpasswd.sh $RPM_BUILD_ROOT%{_sbindir}

:> $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ctdb

cp -p packaging/systemd/samba.conf.tmp $RPM_BUILD_ROOT%{systemdtmpfilesdir}/samba.conf
echo "d /var/run/ctdb 755 root root" > $RPM_BUILD_ROOT%{systemdtmpfilesdir}/ctdb.conf
cp -p ctdb/config/ctdb.service $RPM_BUILD_ROOT%{systemdunitdir}

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
install -p bin/vfstest $RPM_BUILD_ROOT%{_bindir}

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

# remove tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ctdb*_tests
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/ctdb/tests
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ctdb/tests

%if %{with python2}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif
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
/sbin/chkconfig --add samba
%service samba restart "Samba AD daemons"
%systemd_post samba.service

%triggerpostun -- samba < 1:4.9.2-3
%{_bindir}/net groupmap add sid=S-1-5-32-546 unixgroup=nobody type=builtin || :

%triggerpostun -- samba4 < 1:4.1.1-1
# CVE-2013-4476
[ -e %{_sysconfdir}/samba/tls/key.pem ] || exit 0
PERMS=$(stat -c %a %{_sysconfdir}/samba/tls/key.pem)
if [ "$PERMS" != "600" ]; then
	chmod 600 %{_sysconfdir}/samba/tls/key.pem || :
	echo "Fixed permissions of private key file %{_sysconfdir}/samba/tls/key.pem from $PERMS to 600"
	echo "Consider regenerating TLS certificate"
	echo "Removing all tls .pem files will cause an auto-regeneration with the correct permissions"
fi

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

%post	-n python-samba -p /sbin/ldconfig
%postun	-n python-samba -p /sbin/ldconfig

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
%{systemdunitdir}/nmb.service
%{systemdunitdir}/smb.service
%{systemdunitdir}/samba.service
%{systemdtmpfilesdir}/samba.conf
%attr(755,root,root) %{_bindir}/dumpmscat
%attr(755,root,root) %{_bindir}/oLschema2ldif
%attr(755,root,root) %{_bindir}/pdbedit
%attr(755,root,root) %{_bindir}/profiles
%attr(755,root,root) %{_bindir}/sharesec
%attr(755,root,root) %{_bindir}/smbcontrol
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_bindir}/winexe
%attr(755,root,root) %{_sbindir}/eventlogadm
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/samba
%attr(755,root,root) %{_sbindir}/samba_dnsupdate
%attr(755,root,root) %{_sbindir}/samba-gpupdate
%attr(755,root,root) %{_sbindir}/samba_kcc
%attr(755,root,root) %{_sbindir}/samba_spnupdate
%attr(755,root,root) %{_sbindir}/samba_upgradedns
%attr(755,root,root) %{_sbindir}/smbd
%dir %{_libdir}/samba/bind9
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_9.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_10.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_11.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_12.so
%dir %{_libdir}/samba/gensec
%attr(755,root,root) %{_libdir}/samba/gensec/krb5.so
%if %{with system_heimdal}
%dir %{_libdir}/samba/hdb
%attr(755,root,root) %{_libdir}/samba/hdb/hdb_samba4.so
%endif
%dir %{_libdir}/samba/ldb
%attr(755,root,root) %{_libdir}/samba/ldb/aclread.so
%attr(755,root,root) %{_libdir}/samba/ldb/acl.so
%attr(755,root,root) %{_libdir}/samba/ldb/anr.so
%attr(755,root,root) %{_libdir}/samba/ldb/audit_log.so
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
%attr(755,root,root) %{_libdir}/samba/ldb/local_password.so
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
%attr(755,root,root) %{_libdir}/samba/ldb/simple_dn.so
%attr(755,root,root) %{_libdir}/samba/ldb/simple_ldap_map.so
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
%attr(755,root,root) %{_libdir}/samba/service/web.so
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
%attr(755,root,root) %{_libdir}/samba/vfs/linux_xfs_sgid.so
%attr(755,root,root) %{_libdir}/samba/vfs/media_harmony.so
%attr(755,root,root) %{_libdir}/samba/vfs/netatalk.so
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
%attr(755,root,root) %{_libdir}/samba/vfs/worm.so
%attr(755,root,root) %{_libdir}/samba/vfs/xattr_tdb.so
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
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_fruit.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_media_harmony.8*
%{_mandir}/man8/vfs_netatalk.8*
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
%{_mandir}/man8/vfs_ceph.8*
%endif

%files vfs-glusterfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/glusterfs.so
%attr(755,root,root) %{_libdir}/samba/vfs/glusterfs_fuse.so
%{_mandir}/man8/vfs_glusterfs.8*
%{_mandir}/man8/vfs_glusterfs_fuse.8*

%files common
%defattr(644,root,root,755)
%doc BUILD_SYSTEMS.txt PFIF.txt README.cifs-utils README.Coding README.contributing README.md WHATSNEW.txt
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
%attr(755,root,root) %{_bindir}/vfstest
%dir %{_libdir}/samba/auth
%attr(755,root,root) %{_libdir}/samba/auth/script.so
%attr(755,root,root) %{_libdir}/samba/auth/samba4.so
%dir %{_datadir}/samba
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/reg*.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man1/vfstest.1*
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
%attr(755,root,root) %{_bindir}/findsmb
%attr(755,root,root) %{_bindir}/mvxattr
%attr(755,root,root) %{_bindir}/rpcclient
%attr(755,root,root) %{_bindir}/smbcacls
%attr(755,root,root) %{_bindir}/smbclient
%attr(755,root,root) %{_bindir}/smbcquotas
%attr(755,root,root) %{_bindir}/smbtar
%attr(755,root,root) %{_bindir}/smbtree
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/mvxattr.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man8/cifsdd.8*

%files winbind
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/winbind
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/winbind
%{systemdunitdir}/winbind.service
%attr(755,root,root) %{_bindir}/ntlm_auth
%attr(755,root,root) %{_bindir}/wbinfo
%attr(755,root,root) %{_sbindir}/winbindd
%attr(755,root,root) /%{_lib}/security/pam_winbind.so
%attr(755,root,root) /%{_lib}/libnss_winbind.so*
%dir %{_libdir}/samba/krb5
%attr(755,root,root) %{_libdir}/samba/krb5/winbind_krb5_locator.so
%attr(755,root,root) %{_libdir}/samba/libidmap-samba4.so
%attr(755,root,root) %{_libdir}/samba/libnss-info-samba4.so
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
%{_mandir}/man5/smbgetrc.5*

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
%attr(755,root,root) %{_libdir}/libdcerpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc.so.0
%attr(755,root,root) %{_libdir}/libndr-krb5pac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-krb5pac.so.0
%attr(755,root,root) %{_libdir}/libndr-nbt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-nbt.so.0
%attr(755,root,root) %{_libdir}/libndr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr.so.0
%attr(755,root,root) %{_libdir}/libndr-standard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-standard.so.0
%attr(755,root,root) %{_libdir}/libsamba-credentials.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-credentials.so.0
%attr(755,root,root) %{_libdir}/libsamba-errors.so.1
%attr(755,root,root) %{_libdir}/libsamba-hostconfig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-hostconfig.so.0
%attr(755,root,root) %{_libdir}/libsamba-passdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-passdb.so.0
%if %{with python2}
%attr(755,root,root) %{_libdir}/libsamba-policy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-policy.so.0
%endif
%attr(755,root,root) %{_libdir}/libsamba-policy.cpython-3*so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-policy.cpython-3*.so.0
%attr(755,root,root) %{_libdir}/libsamba-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-util.so.0
%attr(755,root,root) %{_libdir}/libsamdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamdb.so.0
%attr(755,root,root) %{_libdir}/libtevent-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtevent-util.so.0
%attr(755,root,root) %{_libdir}/libnetapi.so.0
%attr(755,root,root) %{_libdir}/libsmbconf.so.0
%attr(755,root,root) %{_libdir}/libsmbldap.so.2
%dir %{_libdir}/samba

%if %{without replace}
%attr(755,root,root) %{_libdir}/samba/libreplace-samba4.so
%endif
%if %{without system_heimdal}
%attr(755,root,root) %ghost %{_libdir}/samba/libasn1-samba4.so.8
%attr(755,root,root) %{_libdir}/samba/libasn1-samba4.so.8.0.0
%attr(755,root,root) %ghost %{_libdir}/samba/libcom_err-samba4.so.0
%attr(755,root,root) %{_libdir}/samba/libcom_err-samba4.so.0.25
%attr(755,root,root) %ghost %{_libdir}/samba/libgssapi-samba4.so.2
%attr(755,root,root) %{_libdir}/samba/libgssapi-samba4.so.2.0.0
%attr(755,root,root) %ghost %{_libdir}/samba/libhcrypto-samba4.so.5
%attr(755,root,root) %{_libdir}/samba/libhcrypto-samba4.so.5.0.1
%attr(755,root,root) %ghost %{_libdir}/samba/libhdb-samba4.so.11
%attr(755,root,root) %{_libdir}/samba/libhdb-samba4.so.11.0.2
%attr(755,root,root) %ghost %{_libdir}/samba/libheimbase-samba4.so.1
%attr(755,root,root) %{_libdir}/samba/libheimbase-samba4.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/samba/libheimntlm-samba4.so.1
%attr(755,root,root) %{_libdir}/samba/libheimntlm-samba4.so.1.0.1
%attr(755,root,root) %ghost %{_libdir}/samba/libhx509-samba4.so.5
%attr(755,root,root) %{_libdir}/samba/libhx509-samba4.so.5.0.0
%attr(755,root,root) %ghost %{_libdir}/samba/libkdc-samba4.so.2
%attr(755,root,root) %{_libdir}/samba/libkdc-samba4.so.2.0.0
%attr(755,root,root) %ghost %{_libdir}/samba/libkrb5-samba4.so.26
%attr(755,root,root) %{_libdir}/samba/libkrb5-samba4.so.26.0.0
%attr(755,root,root) %ghost %{_libdir}/samba/libroken-samba4.so.19
%attr(755,root,root) %{_libdir}/samba/libroken-samba4.so.19.0.1
%attr(755,root,root) %ghost %{_libdir}/samba/libwind-samba4.so.0
%attr(755,root,root) %{_libdir}/samba/libwind-samba4.so.0.0.0
%endif
%attr(755,root,root) %{_libdir}/samba/libaddns-samba4.so
%attr(755,root,root) %{_libdir}/samba/libads-samba4.so
%attr(755,root,root) %{_libdir}/samba/libasn1util-samba4.so
%attr(755,root,root) %{_libdir}/samba/libauth4-samba4.so
%attr(755,root,root) %{_libdir}/samba/libauthkrb5-samba4.so
%attr(755,root,root) %{_libdir}/samba/libauth-samba4.so
%attr(755,root,root) %{_libdir}/samba/libauth-unix-token-samba4.so
%attr(755,root,root) %{_libdir}/samba/libCHARSET3-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcliauth-samba4.so
%attr(755,root,root) %{_libdir}/samba/libclidns-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcli-cldap-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcli-ldap-common-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcli-ldap-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcli-nbt-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcli-smb-common-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcli-spoolss-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcluster-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcmdline-contexts-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcmdline-credentials-samba4.so
%attr(755,root,root) %{_libdir}/samba/libcommon-auth-samba4.so
%attr(755,root,root) %{_libdir}/samba/libctdb-event-client-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdb-glue-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdbwrap-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-samba-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdfs-server-ad-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdnsserver-common-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdsdb-garbage-collect-tombstones-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdsdb-module-samba4.so
%attr(755,root,root) %{_libdir}/samba/libevents-samba4.so
%attr(755,root,root) %{_libdir}/samba/libflag-mapping-samba4.so
%attr(755,root,root) %{_libdir}/samba/libgenrand-samba4.so
%attr(755,root,root) %{_libdir}/samba/libgensec-samba4.so
%attr(755,root,root) %{_libdir}/samba/libgpext-samba4.so
%attr(755,root,root) %{_libdir}/samba/libgse-samba4.so
%attr(755,root,root) %{_libdir}/samba/libHDB-SAMBA4-samba4.so
%attr(755,root,root) %{_libdir}/samba/libhttp-samba4.so
%attr(755,root,root) %{_libdir}/samba/libinterfaces-samba4.so
%attr(755,root,root) %{_libdir}/samba/libiov-buf-samba4.so
%attr(755,root,root) %{_libdir}/samba/libkrb5samba-samba4.so
%attr(755,root,root) %{_libdir}/samba/libldbsamba-samba4.so
%attr(755,root,root) %{_libdir}/samba/liblibcli-lsa3-samba4.so
%attr(755,root,root) %{_libdir}/samba/liblibcli-netlogon3-samba4.so
%attr(755,root,root) %{_libdir}/samba/liblibsmb-samba4.so
%attr(755,root,root) %{_libdir}/samba/libLIBWBCLIENT-OLD-samba4.so
%attr(755,root,root) %{_libdir}/samba/libmessages-dgm-samba4.so
%attr(755,root,root) %{_libdir}/samba/libmessages-util-samba4.so
%attr(755,root,root) %{_libdir}/samba/libMESSAGING-samba4.so
%attr(755,root,root) %{_libdir}/samba/libMESSAGING-SEND-samba4.so
%attr(755,root,root) %{_libdir}/samba/libmscat-samba4.so
%attr(755,root,root) %{_libdir}/samba/libmsghdr-samba4.so
%attr(755,root,root) %{_libdir}/samba/libmsrpc3-samba4.so
%attr(755,root,root) %{_libdir}/samba/libndr-samba4.so
%attr(755,root,root) %{_libdir}/samba/libndr-samba-samba4.so
%attr(755,root,root) %{_libdir}/samba/libnetif-samba4.so
%attr(755,root,root) %{_libdir}/samba/libnet-keytab-samba4.so
%attr(755,root,root) %{_libdir}/samba/libnon-posix-acls-samba4.so
%attr(755,root,root) %{_libdir}/samba/libnpa-tstream-samba4.so
%attr(755,root,root) %{_libdir}/samba/libpac-samba4.so
%attr(755,root,root) %{_libdir}/samba/libpopt-samba3-cmdline-samba4.so
%attr(755,root,root) %{_libdir}/samba/libpopt-samba3-samba4.so
%attr(755,root,root) %{_libdir}/samba/libposix-eadb-samba4.so
%attr(755,root,root) %{_libdir}/samba/libprinting-migrate-samba4.so
%attr(755,root,root) %{_libdir}/samba/libprocess-model-samba4.so
%attr(755,root,root) %{_libdir}/samba/libregistry-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba3-util-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba-debug-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba-modules-samba4.so
%if %{with python2}
%attr(755,root,root) %{_libdir}/samba/libsamba-net-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba-python-samba4.so
%endif
%attr(755,root,root) %{_libdir}/samba/libsamba-net.cpython-3*-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba-python.cpython-3*-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba-security-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamba-sockets-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsamdb-common-samba4.so
%attr(755,root,root) %{_libdir}/samba/libscavenge-dns-records-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsecrets3-samba4.so
%attr(755,root,root) %{_libdir}/samba/libserver-id-db-samba4.so
%attr(755,root,root) %{_libdir}/samba/libserver-role-samba4.so
%attr(755,root,root) %{_libdir}/samba/libservice-samba4.so
%attr(755,root,root) %{_libdir}/samba/libshares-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmbclient-raw-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmbd-base-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmbd-conn-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmbd-shim-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmbldaphelper-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmbpasswdparser-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsmb-transport-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsocket-blocking-samba4.so
%attr(755,root,root) %{_libdir}/samba/libsys-rw-samba4.so
%attr(755,root,root) %{_libdir}/samba/libtalloc-report-samba4.so
%attr(755,root,root) %{_libdir}/samba/libtdb-wrap-samba4.so
%attr(755,root,root) %{_libdir}/samba/libtime-basic-samba4.so
%attr(755,root,root) %{_libdir}/samba/libtrusts-util-samba4.so
%attr(755,root,root) %{_libdir}/samba/libutil-cmdline-samba4.so
%attr(755,root,root) %{_libdir}/samba/libutil-reg-samba4.so
%attr(755,root,root) %{_libdir}/samba/libutil-setid-samba4.so
%attr(755,root,root) %{_libdir}/samba/libutil-tdb-samba4.so
%attr(755,root,root) %{_libdir}/samba/libxattr-tdb-samba4.so

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
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
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
%{_includedir}/samba-4.0/util/byteorder.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/discard.h
%{_includedir}/samba-4.0/util/fault.h
%{_includedir}/samba-4.0/util/genrand.h
%{_includedir}/samba-4.0/util/idtree.h
%{_includedir}/samba-4.0/util/idtree_random.h
%{_includedir}/samba-4.0/util/signal.h
%{_includedir}/samba-4.0/util/string_wrappers.h
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
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%attr(755,root,root) %{_libdir}/libdcerpc-binding.so
%attr(755,root,root) %{_libdir}/libdcerpc-samr.so
%attr(755,root,root) %{_libdir}/libdcerpc-server.so
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
%if %{with python2}
%attr(755,root,root) %{_libdir}/libsamba-policy.so
%endif
%attr(755,root,root) %{_libdir}/libsamba-policy.cpython-3*.so
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
%if %{with python2}
%{_pkgconfigdir}/samba-policy.pc
%endif
%{_pkgconfigdir}/samba-policy.cpython-3*.pc
%{_pkgconfigdir}/samba-util.pc
%{_pkgconfigdir}/samdb.pc

%files pidl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pidl
%{_mandir}/man1/pidl.1*
%{_mandir}/man3/Parse::Pidl*.3*
%{perl_vendorlib}/Parse/Pidl*

%if %{with python2}
%files -n python-samba
%defattr(644,root,root,755)
%dir %{py_sitedir}/samba
%attr(755,root,root) %{py_sitedir}/samba/*.so
%{py_sitedir}/samba/*.py[co]
%dir %{py_sitedir}/samba/dcerpc
%{py_sitedir}/samba/dcerpc/*.py[co]
%attr(755,root,root) %{py_sitedir}/samba/dcerpc/*.so
%dir %{py_sitedir}/samba/emulate
%{py_sitedir}/samba/emulate/*.py[co]
%dir %{py_sitedir}/samba/gp_parse
%{py_sitedir}/samba/gp_parse/*.py[co]
%dir %{py_sitedir}/samba/kcc
%{py_sitedir}/samba/kcc/*.py[co]
%dir %{py_sitedir}/samba/netcmd
%{py_sitedir}/samba/netcmd/*.py[co]
%dir %{py_sitedir}/samba/provision
%{py_sitedir}/samba/provision/*.py[co]
%dir %{py_sitedir}/samba/samba3
%attr(755,root,root) %{py_sitedir}/samba/samba3/*.so
%{py_sitedir}/samba/samba3/*.py[co]
%dir %{py_sitedir}/samba/subunit
%{py_sitedir}/samba/subunit/*.py[co]
%dir %{py_sitedir}/samba/tests
%{py_sitedir}/samba/tests/*.py[co]
%dir %{py_sitedir}/samba/tests/blackbox
%{py_sitedir}/samba/tests/blackbox/*.py[co]
%dir %{py_sitedir}/samba/tests/dcerpc
%{py_sitedir}/samba/tests/dcerpc/*.py[co]
%dir %{py_sitedir}/samba/tests/dns_forwarder_helpers
%{py_sitedir}/samba/tests/dns_forwarder_helpers/*.py[co]
%dir %{py_sitedir}/samba/tests/kcc
%{py_sitedir}/samba/tests/kcc/*.py[co]
%dir %{py_sitedir}/samba/tests/samba_tool
%{py_sitedir}/samba/tests/samba_tool/*.py[co]
%dir %{py_sitedir}/samba/tests/emulate
%{py_sitedir}/samba/tests/emulate/*.py[co]
%dir %{py_sitedir}/samba/web_server
%{py_sitedir}/samba/web_server/*.py[co]
%if %{without system_libs}
%attr(755,root,root) %{py_sitedir}/ldb.so
%attr(755,root,root) %{py_sitedir}/talloc.so
%attr(755,root,root) %{py_sitedir}/tdb.so
%attr(755,root,root) %{py_sitedir}/_tevent.so
%{py_sitedir}/tevent.py[co]
%endif
%endif

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
%dir %{py3_sitedir}/samba/emulate
%{py3_sitedir}/samba/emulate/*.py
%{py3_sitedir}/samba/emulate/__pycache__
%dir %{py3_sitedir}/samba/gp_parse
%{py3_sitedir}/samba/gp_parse/*.py
%{py3_sitedir}/samba/gp_parse/__pycache__
%dir %{py3_sitedir}/samba/kcc
%{py3_sitedir}/samba/kcc/*.py
%{py3_sitedir}/samba/kcc/__pycache__
%dir %{py3_sitedir}/samba/netcmd
%{py3_sitedir}/samba/netcmd/*.py
%{py3_sitedir}/samba/netcmd/__pycache__
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
%dir %{py3_sitedir}/samba/tests/samba_tool
%{py3_sitedir}/samba/tests/samba_tool/*.py
%{py3_sitedir}/samba/tests/samba_tool/__pycache__
%dir %{py3_sitedir}/samba/tests/emulate
%{py3_sitedir}/samba/tests/emulate/*.py
%{py3_sitedir}/samba/tests/emulate/__pycache__
%dir %{py3_sitedir}/samba/third_party
%{py3_sitedir}/samba/third_party/*.py
%{py3_sitedir}/samba/third_party/__pycache__
%dir %{py3_sitedir}/samba/web_server
%{py3_sitedir}/samba/web_server/*.py
%{py3_sitedir}/samba/web_server/__pycache__
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
%attr(755,root,root) %{_libdir}/samba/libdlz-bind9-for-torture-samba4.so
%attr(755,root,root) %{_libdir}/samba/libtorture-samba4.so
%{_mandir}/man1/gentest.1*
%{_mandir}/man1/locktest.1*
%{_mandir}/man1/masktest.1*
%{_mandir}/man1/ndrdump.1*
%{_mandir}/man1/smbtorture.1*

%files -n libsmbclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so.*
%attr(755,root,root) %{_libdir}/libwbclient.so.*
%attr(755,root,root) %{_libdir}/samba/libwinbind-client-samba4.so
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
%{_sysconfdir}/ctdb/ctdb-crash-cleanup.sh
%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/debug_locks.sh
%dir %{_localstatedir}/lib/ctdb

%{systemdunitdir}/ctdb.service

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sudoers.d/ctdb
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
%{_datadir}/ctdb/events/legacy/06.nfs.script
%{_datadir}/ctdb/events/legacy/10.interface.script
%{_datadir}/ctdb/events/legacy/11.natgw.script
%{_datadir}/ctdb/events/legacy/11.routing.script
%{_datadir}/ctdb/events/legacy/13.per_ip_routing.script
%{_datadir}/ctdb/events/legacy/20.multipathd.script
%{_datadir}/ctdb/events/legacy/31.clamd.script
%{_datadir}/ctdb/events/legacy/40.vsftpd.script
%{_datadir}/ctdb/events/legacy/41.httpd.script
%{_datadir}/ctdb/events/legacy/49.winbind.script
%{_datadir}/ctdb/events/legacy/50.samba.script
%{_datadir}/ctdb/events/legacy/60.nfs.script
%{_datadir}/ctdb/events/legacy/70.iscsi.script
%{_datadir}/ctdb/events/legacy/91.lvs.script
%{systemdtmpfilesdir}/ctdb.conf
%attr(755,root,root) %{_sbindir}/ctdbd
%attr(755,root,root) %{_sbindir}/ctdbd_wrapper
%attr(755,root,root) %{_bindir}/ctdb
%attr(755,root,root) %{_bindir}/ctdb_local_daemons
%attr(755,root,root) %{_bindir}/ping_pong
%attr(755,root,root) %{_bindir}/ltdbtool
%attr(755,root,root) %{_bindir}/ctdb_diagnostics
%attr(755,root,root) %{_bindir}/onnode
%dir %{_libexecdir}/ctdb
%{_libexecdir}/ctdb/ctdb_natgw
%{_libexecdir}/ctdb/ctdb_recovery_helper
%{_libexecdir}/ctdb/smnotify
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-config
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-event
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-eventd
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_killtcp
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_lock_helper
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_lvs
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_mutex_fcntl_helper
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb-path
%attr(755,root,root) %{_libexecdir}/ctdb/ctdb_takeover_helper

%{_mandir}/man1/ctdb.1*
%{_mandir}/man1/ctdb_diagnostics.1*
%{_mandir}/man1/ctdbd.1*
%{_mandir}/man1/onnode.1*
%{_mandir}/man1/ltdbtool.1*
%{_mandir}/man1/ping_pong.1*
%{_mandir}/man1/ctdbd_wrapper.1*
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
