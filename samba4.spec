# TODO:
#	- unbundle ntdb (no external release as of 16.Oct.2013)
#
# Conditional build:
%bcond_without	ads		# ActiveDirectory support
%bcond_without	cups		# CUPS support
%bcond_without	ldap		# LDAP support
%bcond_without	avahi		# Avahi support
%bcond_without	system_libs	# system libraries (talloc,tdb,tevent,ldb)

%if %{with system_libs}
%define		talloc_ver	2.0.7
%define		tdb_ver		2:1.2.11
%define		ldb_ver		1.1.16
%define		tevent_ver	0.9.18
%define		ntdb_ver	0.9
%endif

%include	/usr/lib/rpm/macros.perl

%define		virusfilter_version 0.1.3
Summary:	Active Directory server
Summary(pl.UTF-8):	Serwer Active Directory
Name:		samba4
Version:	4.1.3
Release:	2
Epoch:		1
License:	GPL v3
Group:		Networking/Daemons
Source0:	http://www.samba.org/samba/ftp/stable/samba-%{version}.tar.gz
# Source0-md5:	a5dbfe87f4cb3d9d91e15e5df99a59a1
Source1:	smb.init
Source2:	samba.pamd
Source4:	samba.sysconfig
Source5:	samba.logrotate
Source6:	smb.conf
Source7:	winbind.init
Source8:	winbind.sysconfig
Source9:	samba.init
Source10:	https://github.com/downloads/fumiyas/samba-virusfilter/samba-virusfilter-%{virusfilter_version}.tar.bz2
# Source10-md5:	a3a30d5fbf309d356e8c5833db680c17
Source11:	samba3.logrotate
Patch0:		system-heimdal.patch
Patch1:		samba-c++-nofail.patch
Patch4:		samba-lprng-no-dot-printers.patch
Patch5:		systemd-pid-dir.patch
Patch6:		unicodePwd-nthash-values-over-LDAP.patch
Patch7:		link.patch
URL:		http://www.samba.org/
BuildRequires:	acl-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_avahi:BuildRequires:	avahi-devel}
#BuildRequires:	ceph-devel
BuildRequires:	ctdb-devel
%{?with_cups:BuildRequires:	cups-devel >= 1:1.2.0}
BuildRequires:	dmapi-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	gamin-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	glusterfs-devel
BuildRequires:	gnutls-devel
BuildRequires:	heimdal-devel >= 1.5.3-1
BuildRequires:	iconv
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	libcom_err-devel
BuildRequires:	libmagic-devel
BuildRequires:	libnscd-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	make >= 3.81
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	ncurses-ext-devel >= 5.2
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
BuildRequires:	pam-devel >= 0.99.8.1
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Parse-Yapp
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	python-devel
BuildRequires:	python-dns
BuildRequires:	python-modules
BuildRequires:	python-testtools
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
%if %{with system_libs}
BuildRequires:	ldb-devel >= %{ldb_ver}
#BuildRequires:	ntdb-devel >= %{ntdb_ver}
BuildRequires:	python-ldb-devel >= %{ldb_ver}
BuildRequires:	python-talloc-devel >= %{talloc_ver}
BuildRequires:	python-tevent >= %{tevent_ver}
BuildRequires:	talloc-devel >= %{talloc_ver}
BuildRequires:	tdb-devel >= %{tdb_ver}
BuildRequires:	tevent-devel >= %{tevent_ver}
%endif
BuildRequires:	xfsprogs-devel
BuildConflicts:	libbsd-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common-server = %{epoch}:%{version}-%{release}
Requires:	python-samba4 = %{epoch}:%{version}-%{release}
Requires:	logrotate >= 3.7-4
Requires:	pam >= 0.99.8.1
Requires:	rc-scripts >= 0.4.0.12
Requires:	setup >= 2.4.6-7
Requires:	systemd-units >= 38
# smbd links with libcups
%{?with_cups:Requires:	cups-lib >= 1:1.2.0}
Obsoletes:	samba-doc-html
Obsoletes:	samba-doc-pdf
Obsoletes:	samba-pdb-xml
Obsoletes:	samba-vfs-block
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

This package contains main Active Directory server daemon.

%description -l pl.UTF-8
Samba udostępnia serwer SMB, który może być użyty w celu dostarczenia
usług sieciowych (potocznie zwanych "Lan Manager"), dla klientów
takich jak MS Windows, OS/2 a także maszyn linuksowych. W pakiecie
znajduje się również oprogramowanie klienckie. Samba używa protokołu
NetBIOS po TCP/IP (NetBT) i nie wymaga protokołu NetBEUI. Ta wersja ma
pełne wsparcie dla blokowania plików, a także wsparcie dla kodowania
haseł w standardzie MS i zarządzania bazą WINS.

Ten pakiet dostarcza główny demon Active Directory.

%package client
Summary:	Samba AD client programs
Summary(pl.UTF-8):	Klienci serwera Samba AD
Group:		Applications/Networking
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	python-samba4 = %{epoch}:%{version}-%{release}
Requires:	heimdal-libs >= 1.5.3-1
Suggests:	cifs-utils
Obsoletes:	smbfs

%description client
Samba-client provides some SMB clients, which complement the build-in
SMB filesystem in Linux. These allow accessing of SMB shares and
printing to SMB printers.

%description client -l pl.UTF-8
Samba-client dostarcza programy uzupełniające obsługę systemu plików
SMB zawartą w jądrze. Pozwalają one na współdzielenie zasobów SMB i
drukowanie w sieci SMB.

%package common
Summary:	Files used by both Samba servers and clients
Summary(pl.UTF-8):	Pliki używane przez serwer i klientów Samby
Group:		Networking/Daemons
Requires:	python-samba4 = %{epoch}:%{version}-%{release}
%if %{with system_libs}
Requires:	ldb >= %{ldb_ver}
#Requires:	ntdb >= %{ntdb_ver}
Requires:	talloc >= %{talloc_ver}
Requires:	tdb >= %{tdb_ver}
Requires:	tevent >= %{tevent_ver}
%endif

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description common -l pl.UTF-8
Samba-common dostarcza pliki niezbędne zarówno dla serwera jak i
klientów Samby.

%package common-server
Summary:	Files used by both Samba3 PDC and Samba4 AD servers
Summary(pl.UTF-8):	Pliki używane przez serwery Samba3 PDC i Samba4 AD
Group:		Networking/Daemons

%description common-server
Files used by both Samba3 PDC and Samba4 AD servers.

%description common-server -l pl.UTF-8
Pliki używane przez serwery Samba3 PDC i Samba4 AD.

%package winbind
Summary:	Samba-winbind daemon, utilities and documentation
Summary(pl.UTF-8):	Demon samba-winbind, narzędzia i dokumentacja
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description winbind
Provides the winbind daemon and testing tools to allow authentication
and group/user enumeration from a Windows or Samba domain controller.

%description winbind -l pl.UTF-8
Pakiet zawiera demona winbind oraz narzędzia testowe. Umożliwia
uwierzytelnianie i wyliczanie grup/użytkowników z kontrolera domeny
Windows lub Samba.

%package devel
Summary:	Header files for Samba
Summary(pl.UTF-8):	Pliki nagłówkowe Samby
Group:		Development/Libraries
Requires:	%{name}-common = %{epoch}:%{version}-%{release}

%description devel
Header files for Samba.

%description devel -l pl.UTF-8
Pliki nagłówkowe Samby.

%package -n pam-pam_smbpass3
Summary:	PAM Samba Password Module
Summary(pl.UTF-8):	Moduł PAM smbpass
Group:		Base
Obsoletes:	pam_smbpass
Obsoletes:	pam-pam_smbpass < 1:4.0.8-3

%description -n pam-pam_smbpass3
PAM module which can be used on conforming systems to keep the
smbpasswd (Samba password) database in sync with the Unix password
file.

%description -n pam-pam_smbpass3 -l pl.UTF-8
Moduł PAM, który może być używany do trzymania pliku smbpasswd (hasła
Samby) zsynchronizowanego z hasłami uniksowymi.

%package pidl
Summary:	Perl IDL compiler
Summary(pl.UTF-8):	Kompilator IDL w Perlu
Group:		Development/Tools
#Requires:	perl-Parse-Yapp

%description pidl
The samba4-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols.

%description pidl -l pl.UTF-8
Ten pakiet zawiera kompilator IDL napisany w Perlu, używany przez
Sambę oraz Wiresharka to analizy IDL i podobnych protokołów.

%package -n python-samba4
Summary:	Samba Module for Python
Summary(pl.UTF-8):	Moduł Samba dla Pythona
Group:		Development/Languages/Python
%pyrequires_eq	python
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	python-dns
Requires:	python-modules
%if %{with system_libs}
Requires:	python-ldb >= %{ldb_ver}
#Requires:	python-ntdb >= %{ntdb_ver}
Requires:	python-talloc >= %{talloc_ver}
Requires:	python-tevent >= %{tevent_ver}
%endif
Obsoletes:	python-samba

%description -n python-samba4
Samba Module for Python.

%description -n python-samba4 -l pl.UTF-8
Moduł Samba dla Pythona.

%package test
Summary:	Testing tools for Samba servers and clients
Summary(pl.UTF-8):	Narzędzia testowe dla serwerów i klientów Samby
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-winbind = %{epoch}:%{version}-%{release}

%description test
samba4-test provides testing tools for both the server and client
packages of Samba.

%description test -l pl.UTF-8
Narzędzia testowe dla serwerów i klientów Samby.

%package test-devel
Summary:	Testing development files for Samba servers and clients
Summary(pl.UTF-8):	Pliki programistyczne narzędzi testowych dla serwerów i klientów Samby
Group:		Applications/System
Requires:	%{name}-test = %{epoch}:%{version}-%{release}

%description test-devel
samba-test-devel provides development files for the library used by
testing tools for both the server and client packages of Samba.

%description test-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki wykorzystywanej
przez narzędzia testowe dla serwerów i klientów Samby.

%package -n samba3
Summary:	SMB server
Summary(pl.UTF-8):	Serwer SMB
Group:		Networking/Daemons
Requires:	samba3-common = %{epoch}:%{version}-%{release}
Requires:	%{name}-common-server = %{epoch}:%{version}-%{release}
# smbd links with libcups
%{?with_cups:Requires:	cups-lib >= 1:1.2.0}
Obsoletes:	samba-pdb-xml
Obsoletes:	samba-vfs-block

%description -n samba3
Samba provides an SMB server which can be used to provide network
services to SMB (sometimes called "Lan Manager") clients, including
various versions of MS Windows, OS/2, and other Linux machines. Samba
also provides some SMB clients, which complement the built-in SMB
filesystem in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame) protocol.

%description -n samba3 -l pl.UTF-8
Samba udostępnia serwer SMB, który może być użyty w celu dostarczenia
usług sieciowych (potocznie zwanych "Lan Manager"), dla klientów
takich jak MS Windows, OS/2 a także maszyn linuksowych. W pakiecie
znajduje się również oprogramowanie klienckie. Samba używa protokołu
NetBIOS po TCP/IP (NetBT) i nie wymaga protokołu NetBEUI. Ta wersja ma
pełne wsparcie dla blokowania plików, a także wsparcie dla kodowania
haseł w standardzie MS i zarządzania bazą WINS.

%package -n samba3-server
Summary:	SMB server initscripts
Summary(pl.UTF-8):	Skrypty startowe serwera SMB
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	samba3 = %{epoch}:%{version}-%{release}
Requires:	logrotate >= 3.7-4
Requires:	rc-scripts >= 0.4.0.12
Requires:	setup >= 2.4.6-7
Obsoletes:	samba < 1:4.0.0-1

%description -n samba3-server
This package contains startup scripts and services for old SMB server
daemons (smbd, nmbd).

%description -n samba3-server -l pl.UTF-8
Ten pakiet zawiera skrypty startowe dla starych usług serwera SMB
(smbd, nmbd).

%package -n samba3-client
Summary:	Samba client programs
Summary(pl.UTF-8):	Klienci serwera Samba
Group:		Applications/Networking
Requires:	samba3-common = %{epoch}:%{version}-%{release}
Requires:	samba3-libsmbclient = %{epoch}:%{version}-%{release}
Requires:	heimdal-libs
Obsoletes:	smbfs
Obsoletes:	samba-client < 1:4.0.0-1
Suggests:	cifs-utils

%description -n samba3-client
Samba-client provides some SMB clients, which complement the build-in
SMB filesystem in Linux. These allow accessing of SMB shares and
printing to SMB printers.

%description -n samba3-client -l pl.UTF-8
Samba-client dostarcza programy uzupełniające obsługę systemu plików
SMB zawartą w jądrze. Pozwalają one na współdzielenie zasobów SMB i
drukowanie w sieci SMB.

%package -n samba3-common
Summary:	Files used by both Samba servers and clients
Summary(pl.UTF-8):	Pliki używane przez serwer i klientów Samba
Group:		Networking/Daemons
Requires:	talloc >= %{libtalloc_ver}
Requires:	tdb >= %{libtdb_ver}
Obsoletes:	samba-common < 1:4.0.0-1

%description -n samba3-common
Samba-common provides files necessary for both the server and client
packages of Samba.

%description -n samba3-common -l pl.UTF-8
Samba-common dostarcza pliki niezbędne zarówno dla serwera jak i
klientów Samba.

%package -n samba3-devel
Summary:	Header files for Samba
Summary(pl.UTF-8):	Pliki nagłówkowe Samby
Group:		Development/Libraries
Requires:	samba3-common = %{epoch}:%{version}-%{release}
Obsoletes:	samba-devel < 1:4.0.0-1

%description -n samba3-devel
Header files for Samba.

%description -n samba3-devel -l pl.UTF-8
Pliki nagłówkowe Samby.

%package -n samba3-vfs-audit
Summary:	VFS module to audit file access
Summary(pl.UTF-8):	Moduł VFS do monitorowania operacji na plikach
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-audit < 1:4.0.0-1

%description -n samba3-vfs-audit
A simple modules (audit, extd_audit, full_audit) to audit file access
to the syslog facility. The following operations are logged:
 - share connect/disconnect,
 - directory opens/create/remove,
 - file open/close/rename/unlink/chmod.

%description -n samba3-vfs-audit -l pl.UTF-8
Proste moduły (audit, extd_audit, full_audit) do monitorowania dostępu
do plików na serwerze Samba do sysloga. Monitorowane są następujące
operacje:
 - podłączenie do/odłączenie od zasobu,
 - otwarcie/utworzenie/zmiana nazwy katalogu,
 - otwarcie/zamknięcie/zmiana nazwy/skasowanie/zmiana praw plików.

%package -n samba3-vfs-cap
Summary:	VFS module for CAP and samba compatibility
Summary(pl.UTF-8):	Moduł VFS zgodności z CAP (Columbia AppleTalk Program)
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-cap < 1:4.0.0-1

%description -n samba3-vfs-cap
Convert an incoming Shift-JIS character to the 3 byte hex
representation used by the Columbia AppleTalk Program (CAP), i.e. :AB.
This is used for compatibility between Samba and CAP.

%description -n samba3-vfs-cap -l pl.UTF-8
Zamienia znaki kodowane Shift-JIS do trzybajowej szestnastkowej
reprezentacji używanej przez program Columbia AppleTalk Program (CAP).

%package -n samba3-vfs-catia
Summary:	VFS module to fix Catia CAD filenames
Summary(pl.UTF-8):	Moduł VFS poprawiający nazwy plików z pakietu CAD Catia
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-catia < 1:4.0.0-1

%description -n samba3-vfs-catia
The Catia CAD package commonly creates filenames that use characters
that are illegal in CIFS filenames. The vfs_catia VFS module
implements a fixed character mapping so that these files can be shared
with CIFS clients.

%description -n samba3-vfs-catia -l pl.UTF-8
Pakiet CAD Catia często tworzy nazwy plików, wykorzystujące znaki,
które nie są dozwolone w nazwach plików CIFS. Moduł VFS vfs_catia
implementuje stałe odwzorowanie znaków, pozwalające na współdzielenie
plików z innymi klientami CIFS.

%package -n samba3-vfs-default_quota
Summary:	VFS module to store default quotas in a specified quota record
Summary(pl.UTF-8):	Moduł VFS do zapisywania domyślnych limitów w określonym rekordzie
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-default_quota < 1:4.0.0-1

%description -n samba3-vfs-default_quota
This VFS modules stores default quotas in a specified quota record.

%description -n samba3-vfs-default_quota -l pl.UTF-8
Ten moduł VFS zapisuje domyślne limity (quoty) w określonym rekordzie
limitów.

%package -n samba3-vfs-expand_msdfs
Summary:	VFS module for hosting a Microsoft Distributed File System Tree
Summary(pl.UTF-8):	Moduł VFS obsługi Microsoft Distributed File System
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-expand_msdfs < 1:4.0.0-1

%description -n samba3-vfs-expand_msdfs
A VFS module for hosting a Microsoft Distributed File System Tree.

The Distributed File System (DFS) provides a means of separating the
logical view of files and directories that users see from the actual
physical locations of these resources on the network. It allows for
higher availability, smoother storage expansion, load balancing, and
so on.

%description -n samba3-vfs-expand_msdfs -l pl.UTF-8
Moduł VFS do udostępniania drzewa systemu plików Microsoft Distributed
File System.

Distributed File System (DFS) umożliwia rozdzielanie logicznego widoku
plików i katalogów widocznych przez użytkowników z fizycznego
umiejscowienia tych zasobów w sieci. Pozwala to na wyższą dostępność,
płynniejsze powiększanie przestrzeni, rozdzielanie obciążenia itp.

%package -n samba3-vfs-fake_perms
Summary:	VFS module to report read-only fires as writable
Summary(pl.UTF-8):	Moduł VFS udający, że pliki tylko do odczytu są zapisywalne
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-fake_perms < 1:4.0.0-1

%description -n samba3-vfs-fake_perms
This module allow Roaming Profile files and directories to be set (on
the Samba server under UNIX) as read only. This module will, if
installed on the Profiles share, report to the client that the Profile
files and directories are writeable. This satisfies the client even
though the files will never be overwritten as the client logs out or
shuts down.

%description -n samba3-vfs-fake_perms -l pl.UTF-8
Ten moduł pozwala na ustawienie plików i katalogów z wędrujących
profili (Roaming Profiles) jako tylko do odczytu. Moduł ten w
przypadku zainstalowania na udziale z profilami będzie zgłaszał
klientom, że pliki i katalogi z profilu są zapisywane. To wystarczy
klientom pomimo, że pliki nie zostaną nigdy nadpisane przy logowaniu
lub wylogowywaniu klienta.

%package -n samba3-vfs-notify_fam
Summary:	VFS module to implement file change notifications
Summary(pl.UTF-8):	Moduł VFS implementujący informowanie o zmianach w plikach
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-notify_fam < 1:4.0.0-1

%description -n samba3-vfs-notify_fam
The vfs_notify_fam module makes use of the system FAM (File Alteration
Monitor) daemon to implement file change notifications for Windows
clients.

%description -n samba3-vfs-notify_fam -l pl.UTF-8
Ten moduł używa demona FAM (File Alteration Monitor) do implementacji
informowania o zmianach w plikach dla klientów Windows.

%package -n samba3-vfs-netatalk
Summary:	VFS module for ease co-existence of Samba and netatalk
Summary(pl.UTF-8):	Moduł VFS ułatwiający współpracę usług Samba i netatalk
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-netatalk < 1:4.0.0-1

%description -n samba3-vfs-netatalk
Package contains a netatalk VFS module for ease co-existence of Samba
and netatalk file sharing services.

%description -n samba3-vfs-netatalk -l pl.UTF-8
Pakiet zawiera moduł VFS netatalk umożliwiający współpracę usług Samba
i netatalk przy udostępnianiu zasobów.

%package -n samba3-vfs-recycle
Summary:	VFS module to add recycle bin facility to a Samba share
Summary(pl.UTF-8):	Moduł VFS dodający funkcję kosza do zasobu Samby
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-recycle < 1:4.0.0-1

%description -n samba3-vfs-recycle
VFS module to add recycle bin facility to a Samba share.

%description -n samba3-vfs-recycle -l pl.UTF-8
Moduł VFS dodający funkcję kosza do zasobu Samby.

%package -n samba3-vfs-readahead
Summary:	VFS module for pre-loading the kernel buffer cache
Summary(pl.UTF-8):	Moduł VFS do wczesnego odczytu danych do bufora cache jądra
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-readahead < 1:4.0.0-1

%description -n samba3-vfs-readahead
This VFS module detects read requests at multiples of a given offset
(hex 0x80000 by default) and then tells the kernel via either the
readahead system call (on Linux) or the posix_fadvise system call to
pre-fetch this data into the buffer cache.

This module is useful for Windows Vista clients reading data using the
Windows Explorer program, which asynchronously does multiple file read
requests at offset boundaries of 0x80000 bytes.

%description -n samba3-vfs-readahead -l pl.UTF-8
Ten moduł VFS wykrywa żądania odczytu spod wielokrotności podanych
pozycji (domyślnie 0x80000 szesnastkowo) i instruuje jądro poprzez
wywołanie systemowe readahead (pod Linuksem) lub posix_fadvise do
wczesnego odczytu tych danych do bufora cache.

Ten moduł jest przydatny dla klientów Windows Vista odczytujących dane
przy użyciu programu Windows Explorer, który asynchronicznie wykonuje
wiele żądań odczytu plików spod pozycji o wielokrotnościach 0x80000
bajtów.

%package -n samba3-vfs-readonly
Summary:	VFS module for read-only limitation for specified share
Summary(pl.UTF-8):	Moduł VFS do ograniczania określonego udziału tylko do odczytu
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-readonly < 1:4.0.0-1

%description -n samba3-vfs-readonly
This module performs a read-only limitation for specified share (or
all of them if it is loaded in a [global] section) based on period
definition in smb.conf.

%description -n samba3-vfs-readonly -l pl.UTF-8
Ten moduł wprowadza ograniczenie tylko do odczytu dla określonego
udziału (lub wszystkich, jeśli jest wczytywany w sekcji [global]) w
oparciu o definicje okresów w smb.conf.

%package -n samba3-vfs-scannedonly
Summary:	Anti-virus solution as VFS module
Summary(pl.UTF-8):	Rozwiązanie antywirusowe jako moduł VFS
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-scannedonly < 1:4.0.0-1

%description -n samba3-vfs-scannedonly
The vfs_scannedonly VFS module ensures that only files that have been
scanned for viruses are visible and accessible to the end user. If
non-scanned files are found an anti-virus scanning daemon is notified.

%description -n samba3-vfs-scannedonly -l pl.UTF-8
Moduł VFS vfs_scannedonly zapewnia, że tylko pliki, które zostały
wcześniej przeskanowane pod kątem wirusów, są widoczne i dostępne dla
użytkownika końcowego. Jeśli zostaną znalezione pliki nie
przeskanowane, powiadamiany jest antywirusowy demon skanujący.

%package -n samba3-vfs-shadow_copy
Summary:	VFS module to make automatic copy of data in Samba share
Summary(pl.UTF-8):	Moduł VFS do tworzenia automatycznych kopii danych w zasobach Samby
Group:		Networking/Daemons
Requires:	samba3 = %{epoch}:%{version}-%{release}
Obsoletes:	samba-vfs-shadow_copy < 1:4.0.0-1

%description -n samba3-vfs-shadow_copy
VFS module to make automatic copy of data in Samba share.

%description -n samba3-vfs-shadow_copy -l pl.UTF-8
Moduł VFS do tworzenia automatycznych kopii danych w zasobach Samby.

%package -n smbget3
Summary:	A utility for retrieving files using the SMB protocol
Summary(pl.UTF-8):	Narzędzie do pobierania plików protokołem SMB
Group:		Applications/Networking
Obsoletes:	smbget < 1:4.0.8-3

%description -n smbget3
wget-like utility for downloading files over SMB.

%description -n smbget3 -l pl.UTF-8
Narzędzie podobne do wgeta do pobierania plików protokołem SMB
używanym w sieciach MS Windows.

%package -n cups-backend-smb3
Summary:	CUPS backend for printing to SMB printers
Summary(pl.UTF-8):	Backend CUPS-a drukujący na drukarkach SMB
Group:		Applications/Printing
Requires:	samba3-client = %{epoch}:%{version}-%{release}
Requires:	cups >= 1:1.2.0
Obsoletes:	cups-backend-smb < 1:4.0.8-3

%description -n cups-backend-smb3
CUPS backend for printing to SMB printers.

%description -n cups-backend-smb3 -l pl.UTF-8
Backend CUPS-a drukujący na drukarkach SMB.

%package -n samba3-winbind
Summary:	Samba-winbind daemon, utilities and documentation
Summary(pl.UTF-8):	Demon samba-winbind, narzędzia i dokumentacja
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	samba3-common = %{epoch}:%{version}-%{release}
Requires:	systemd-units >= 38
Obsoletes:	samba-winbind < 1:4.0.0-1

%description -n samba3-winbind
Provides the winbind daemon and testing tools to allow authentication
and group/user enumeration from a Windows or Samba domain controller.

%description -n samba3-winbind -l pl.UTF-8
Pakiet zawiera demona winbind oraz narzędzia testowe. Umożliwia
uwierzytelnianie i wyliczanie grup/użytkowników z kontrolera domeny
Windows lub Samba.

%package -n nss_wins3
Summary:	Name Service Switch service for WINS
Summary(pl.UTF-8):	Usługa Name Service Switch dla WINS
Group:		Base
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	nss_wins < 1:4.0.8-3

%description -n nss_wins3
Provides the libnss_wins shared library which resolves NetBIOS names
to IP addresses.

%description -n nss_wins3 -l pl.UTF-8
Biblioteka dzielona libnss_wins rozwiązująca nazwy NetBIOS na adresy
IP.

%package -n samba3-libsmbclient
Summary:	libsmbclient and libwbclient - Samba client libraries
Summary(pl.UTF-8):	libsmbclient i libwbclient - biblioteki klienckie Samby
Group:		Libraries
Obsoletes:	libsmbclient

%description -n samba3-libsmbclient
libsmbclient and libwbclient - libraries that allow to use Samba
client functions.

%description -n samba3-libsmbclient -l pl.UTF-8
libsmbclient i libwbclient - biblioteki pozwalające korzystać z funcji
klienta Samby.

%package -n samba3-libsmbclient-devel
Summary:	Development files for Samba client libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek klienta Samby
Group:		Development/Libraries
Requires:	samba3-libsmbclient = %{epoch}:%{version}-%{release}
Provides:	libsmbclient-devel
Obsoletes:	libsmbclient-devel
Obsoletes:	libsmbclient-static

%description -n samba3-libsmbclient-devel
Header files for libsmbclient and libwbclient libraries.

%description -n samba3-libsmbclient-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libsmbclient i libwbclient.

%package -n openldap-schema-samba3
Summary:	Samba LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla Samby
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
Obsoletes:	openldap-schema-samba < 1:4.0.0-1

%description -n openldap-schema-samba3
This package contains samba.schema for OpenLDAP.

%description -n openldap-schema-samba3 -l pl.UTF-8
Ten pakiet zawiera schemat Samby (samba.schema) dla OpenLDAP-a.

%prep
%setup -q -n samba-%{version}
%patch0 -p1
%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python|' source4/scripting/bin/samba*
sed -i -e 's|#!/usr/bin/env perl|#!/usr/bin/perl|' pidl/pidl

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
	--disable-rpath-install \
	--builtin-libraries=replace,ccan \
	--bundled-libraries=NONE,subunit,iniparser,ntdb,%{!?with_system_libs:talloc,tdb,ldb,tevent,pytalloc,pytalloc-util,pytdb,pytevent,pyldb,pyldb-util} \
	--private-libraries=smbclient,smbsharemodes,wbclient \
	--with-shared-modules=idmap_ad,idmap_rid,idmap_adex,idmap_hash,idmap_tdb2,pdb_tdbsam,pdb_ldap,pdb_ads,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4,auth_unix,auth_wbc,auth_server,auth_netlogond,auth_script,auth_samba4 \
	--with-acl-support \
	--with%{!?with_ads:out}-ads \
	--with-aio-support \
	--with-automount \
	--with-dmapi \
	--with-dnsupdate \
	--with-iconv \
	--with%{!?with_ldap:out}-ldap \
	--with-pam \
	--with-pam_smbpass \
	--with-quotas \
	--with-regedit \
	--with-sendfile-support \
	--with-syslog \
	--with-utmp \
	--with-winbind \
	--%{?with_avahi:en}%{!?with_avahi:dis}able-avahi \
	--enable-cups \
	--enable-iprint

%{__make}

# Build PIDL for installation into vendor directories before
# 'make proto' gets to it.
cd pidl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

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
%{__rm} -r $RPM_BUILD_ROOT/%{_datadir}/perl5

# Install PIDL
cd pidl
%{__make} install \
	PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
cd ..

# Clean out crap left behind by the PIDL install
%{__rm} $RPM_BUILD_ROOT%{perl_vendorlib}/wscript_build
%{__rm} -r $RPM_BUILD_ROOT%{perl_vendorlib}/Parse/Yapp
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Parse/Pidl/.packlist

# not ready for production, and no MIT kerberos in PLD
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mit_samba.so

install -p source3/script/mksmbpasswd.sh $RPM_BUILD_ROOT%{_sbindir}

install packaging/systemd/samba.conf.tmp $RPM_BUILD_ROOT%{systemdtmpfilesdir}/samba.conf
install packaging/systemd/nmb.service $RPM_BUILD_ROOT%{systemdunitdir}
install packaging/systemd/samba.service $RPM_BUILD_ROOT%{systemdunitdir}
install packaging/systemd/smb.service $RPM_BUILD_ROOT%{systemdunitdir}
install packaging/systemd/winbind.service $RPM_BUILD_ROOT%{systemdunitdir}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/smb
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/samba
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/samba
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/samba
cp -p %{SOURCE11} $RPM_BUILD_ROOT/etc/logrotate.d/samba3
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/samba/smb.conf
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/winbind
cp -p %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/winbind
install -p %{SOURCE9} $RPM_BUILD_ROOT/etc/rc.d/init.d/samba

echo "LDB_MODULES_PATH=%{_libdir}/samba/ldb" > $RPM_BUILD_ROOT/etc/env.d/LDB_MODULES_PATH

# move lib{smb,wb}client where they always were for compatibility
%{__mv} $RPM_BUILD_ROOT%{_libdir}/samba/libsmbclient.so.* $RPM_BUILD_ROOT%{_libdir}
ln -s libsmbclient.so.0 $RPM_BUILD_ROOT%{_libdir}/libsmbclient.so
ln -s libwbclient.so.0 $RPM_BUILD_ROOT%{_libdir}/libwbclient.so
%{__mv} $RPM_BUILD_ROOT%{_libdir}/samba/libwbclient.so.* $RPM_BUILD_ROOT%{_libdir}
%{__mv} $RPM_BUILD_ROOT%{_includedir}/samba-4.0/libsmbclient.h $RPM_BUILD_ROOT%{_includedir}
%{__mv} $RPM_BUILD_ROOT%{_includedir}/samba-4.0/wbclient.h $RPM_BUILD_ROOT%{_includedir}

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libnss_winbind.so* $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libnss_wins.so* $RPM_BUILD_ROOT/%{_lib}
install -p bin/vfstest $RPM_BUILD_ROOT%{_bindir}

touch $RPM_BUILD_ROOT/var/lib/samba/{wins.dat,browse.dat}

echo '127.0.0.1 localhost' > $RPM_BUILD_ROOT%{_sysconfdir}/samba/lmhosts

echo "%{_libdir}/samba" >$RPM_BUILD_ROOT/etc/ld.so.conf.d/samba.conf

%if %{with cups}
install -d $RPM_BUILD_ROOT%{cups_serverbin}/backend
ln -s %{_bindir}/smbspool $RPM_BUILD_ROOT%{cups_serverbin}/backend/smb
%endif

> $RPM_BUILD_ROOT%{_sysconfdir}/samba/smbusers
> $RPM_BUILD_ROOT/etc/security/blacklist.samba

%if %{with ldap}
install examples/LDAP/samba.schema $RPM_BUILD_ROOT%{schemadir}
%endif

# remove man pages for not installed commands
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/log2pcap.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_cacheprime.8*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_gpfs.8*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_prealloc.8*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/vfs_tsmsm.8*

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add samba
%service samba restart "Samba AD daemon"
%systemd_post samba.service

%preun
if [ "$1" = "0" ]; then
	%service samba stop
	/sbin/chkconfig --del samba
fi
%systemd_preun samba.service

%postun
%systemd_reload

%post common -p /sbin/ldconfig
%postun common -p /sbin/ldconfig

%post -n python-samba4 -p /sbin/ldconfig
%postun -n python-samba4 -p /sbin/ldconfig

%post -n samba3-server
/sbin/chkconfig --add smb
%service smb restart "Samba3 daemons"
%systemd_post smb.service nmb.service

%preun -n samba3-server
if [ "$1" = "0" ]; then
	%service smb stop
	/sbin/chkconfig --del smb
fi
%systemd_preun smb.service nmb.service

%postun -n samba3-server
%systemd_reload

%triggerpostun -n samba3-server -- samba < 1:4.0.0-1
/sbin/chkconfig --add smb
%service smb restart "Samba3 daemons"
%systemd_post smb.service nmb.service

%post -n samba3-winbind
/sbin/chkconfig --add winbind
%service winbind restart "Winbind daemon"
%systemd_post winbind.service

%preun -n samba3-winbind
if [ "$1" = "0" ]; then
	%service winbind stop
	/sbin/chkconfig --del winbind
fi
%systemd_preun winbind.service

%postun -n samba3-winbind
%systemd_reload

%triggerpostun -n samba3-winbind -- samba-winbind < 1:4.0.0-1
/sbin/chkconfig --add winbind
%service winbind restart "Winbind daemon"
%systemd_post winbind.service

%post -n openldap-schema-samba3
# dependant schemas: cosine(uid) inetorgperson(displayName) nis(gidNumber)
%openldap_schema_register %{schemadir}/samba.schema -d cosine,inetorgperson,nis
%service -q ldap restart

%postun -n openldap-schema-samba3
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/samba.schema
	%service -q ldap restart
fi

%triggerpostun -n openldap-schema-samba3 -- openldap-schema-samba < 1:4.0.0-1
# dependant schemas: cosine(uid) inetorgperson(displayName) nis(gidNumber)
%openldap_schema_register %{schemadir}/samba.schema -d cosine,inetorgperson,nis
%service -q ldap restart

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/env.d/LDB_MODULES_PATH
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/samba
%attr(754,root,root) /etc/rc.d/init.d/samba
%{systemdunitdir}/samba.service
%{systemdtmpfilesdir}/samba.conf
%attr(755,root,root) %{_bindir}/oLschema2ldif
%attr(755,root,root) %{_sbindir}/samba
%attr(755,root,root) %{_sbindir}/samba_dnsupdate
%attr(755,root,root) %{_sbindir}/samba_kcc
%attr(755,root,root) %{_sbindir}/samba_spnupdate
%attr(755,root,root) %{_sbindir}/samba_upgradedns
%attr(755,root,root) %{_libdir}/samba/libdsdb-module.so
%attr(755,root,root) %{_libdir}/samba/libpac.so
%dir %{_libdir}/samba/bind9
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9.so
%attr(755,root,root) %{_libdir}/samba/bind9/dlz_bind9_9.so
%dir %{_libdir}/samba/hdb
%attr(755,root,root) %{_libdir}/samba/hdb/hdb_samba4.so
%dir %{_libdir}/samba/gensec
%attr(755,root,root) %{_libdir}/samba/gensec/krb5.so
%dir %{_libdir}/samba/ldb
%attr(755,root,root) %{_libdir}/samba/ldb/aclread.so
%attr(755,root,root) %{_libdir}/samba/ldb/acl.so
%attr(755,root,root) %{_libdir}/samba/ldb/anr.so
%attr(755,root,root) %{_libdir}/samba/ldb/descriptor.so
%attr(755,root,root) %{_libdir}/samba/ldb/dirsync.so
%attr(755,root,root) %{_libdir}/samba/ldb/extended_dn_in.so
%attr(755,root,root) %{_libdir}/samba/ldb/extended_dn_out.so
%attr(755,root,root) %{_libdir}/samba/ldb/extended_dn_store.so
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
%attr(755,root,root) %{_libdir}/samba/ldb/update_keytab.so
%attr(755,root,root) %{_libdir}/samba/ldb/wins_ldb.so
%dir %{_libdir}/samba/process_model
%attr(755,root,root) %{_libdir}/samba/process_model/onefork.so
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
%attr(755,root,root) %{_libdir}/samba/service/smb.so
%attr(755,root,root) %{_libdir}/samba/service/web.so
%attr(755,root,root) %{_libdir}/samba/service/winbind.so
%attr(755,root,root) %{_libdir}/samba/service/wrepl.so
%{_datadir}/samba/setup
%{_mandir}/man1/oLschema2ldif.1*
%{_mandir}/man8/samba.8*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cifsdd
%attr(755,root,root) %{_bindir}/nmblookup4
%attr(755,root,root) %{_bindir}/reg*
%attr(755,root,root) %{_bindir}/smbclient4
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/nmblookup4.1*
%{_mandir}/man1/reg*.1*

%files common
%defattr(644,root,root,755)
%doc README WHATSNEW.txt Roadmap
/etc/ld.so.conf.d/samba.conf
%attr(755,root,root) %{_bindir}/samba-regedit
%attr(755,root,root) %{_bindir}/samba-tool
%dir %{_sysconfdir}/samba
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samba/lmhosts
%attr(755,root,root) %{_libdir}/libdcerpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-atsvc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-atsvc.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-binding.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-binding.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-samr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-samr.so.0
%attr(755,root,root) %{_libdir}/libdcerpc-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcerpc-server.so.0
%attr(755,root,root) %{_libdir}/libgensec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgensec.so.0
%attr(755,root,root) %{_libdir}/libndr-nbt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-nbt.so.0
%attr(755,root,root) %{_libdir}/libndr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr.so.0
%attr(755,root,root) %{_libdir}/libndr-krb5pac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-krb5pac.so.0
%attr(755,root,root) %{_libdir}/libregistry.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libregistry.so.0
%attr(755,root,root) %{_libdir}/libndr-standard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libndr-standard.so.0
%attr(755,root,root) %{_libdir}/libsamba-credentials.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-credentials.so.0
%attr(755,root,root) %{_libdir}/libsamba-hostconfig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-hostconfig.so.0
%attr(755,root,root) %{_libdir}/libsamba-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-util.so.0
%attr(755,root,root) %{_libdir}/libsamdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamdb.so.0
%attr(755,root,root) %{_libdir}/libsmbclient-raw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsmbclient-raw.so.0
%attr(755,root,root) %{_libdir}/libtevent-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtevent-util.so.0
%attr(755,root,root) %{_libdir}/libnetapi.so.0
%attr(755,root,root) %{_libdir}/libpdb.so.0
%attr(755,root,root) %{_libdir}/libsmbconf.so.0
%attr(755,root,root) %{_libdir}/libsmbldap.so.0
%dir %{_libdir}/samba
%attr(755,root,root) %{_libdir}/samba/libCHARSET3.so
%attr(755,root,root) %{_libdir}/samba/libLIBWBCLIENT_OLD.so
%attr(755,root,root) %{_libdir}/samba/libMESSAGING.so
%attr(755,root,root) %{_libdir}/samba/libaddns.so
%attr(755,root,root) %{_libdir}/samba/libads.so
%attr(755,root,root) %{_libdir}/samba/libasn1util.so
%attr(755,root,root) %{_libdir}/samba/libauth.so
%attr(755,root,root) %{_libdir}/samba/libauth4.so
%attr(755,root,root) %{_libdir}/samba/libauth_sam_reply.so
%attr(755,root,root) %{_libdir}/samba/libauth_unix_token.so
%attr(755,root,root) %{_libdir}/samba/libauthkrb5.so
%attr(755,root,root) %{_libdir}/samba/libcli-ldap-common.so
%attr(755,root,root) %{_libdir}/samba/libcli-ldap.so
%attr(755,root,root) %{_libdir}/samba/libcli-nbt.so
%attr(755,root,root) %{_libdir}/samba/libcli_cldap.so
%attr(755,root,root) %{_libdir}/samba/libcli_smb_common.so
%attr(755,root,root) %{_libdir}/samba/libcli_spoolss.so
%attr(755,root,root) %{_libdir}/samba/libcliauth.so
%attr(755,root,root) %{_libdir}/samba/libcluster.so
%attr(755,root,root) %{_libdir}/samba/libcmdline-credentials.so
%attr(755,root,root) %{_libdir}/samba/libdbwrap.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-samba.so
%attr(755,root,root) %{_libdir}/samba/libdcerpc-samba4.so
%attr(755,root,root) %{_libdir}/samba/libdfs_server_ad.so
%attr(755,root,root) %{_libdir}/samba/liberrors.so
%attr(755,root,root) %{_libdir}/samba/libevents.so
%attr(755,root,root) %{_libdir}/samba/libflag_mapping.so
%attr(755,root,root) %{_libdir}/samba/libgse.so
%attr(755,root,root) %{_libdir}/samba/libiniparser.so
%attr(755,root,root) %{_libdir}/samba/libinterfaces.so
%attr(755,root,root) %{_libdir}/samba/libkrb5samba.so
%attr(755,root,root) %{_libdir}/samba/libldb-cmdline.so
%attr(755,root,root) %{_libdir}/samba/libldbsamba.so
%attr(755,root,root) %{_libdir}/samba/liblibcli_lsa3.so
%attr(755,root,root) %{_libdir}/samba/liblibcli_netlogon3.so
%attr(755,root,root) %{_libdir}/samba/liblibsmb.so
%attr(755,root,root) %{_libdir}/samba/libmsrpc3.so
%attr(755,root,root) %{_libdir}/samba/libndr-samba.so
%attr(755,root,root) %{_libdir}/samba/libndr-samba4.so
%attr(755,root,root) %{_libdir}/samba/libnetif.so
%attr(755,root,root) %{_libdir}/samba/libnon_posix_acls.so
%attr(755,root,root) %{_libdir}/samba/libnpa_tstream.so
%attr(755,root,root) %{_libdir}/samba/libntvfs.so
%attr(755,root,root) %{_libdir}/samba/libposix_eadb.so
%attr(755,root,root) %{_libdir}/samba/libprinting_migrate.so
%attr(755,root,root) %{_libdir}/samba/libprocess_model.so
%attr(755,root,root) %{_libdir}/samba/libsamba-modules.so
%attr(755,root,root) %{_libdir}/samba/libsamba-security.so
%attr(755,root,root) %{_libdir}/samba/libsamba-sockets.so
%attr(755,root,root) %{_libdir}/samba/libsamba3-util.so
%attr(755,root,root) %{_libdir}/samba/libsamdb-common.so
%attr(755,root,root) %{_libdir}/samba/libsecrets3.so
%attr(755,root,root) %{_libdir}/samba/libserver-role.so
%attr(755,root,root) %{_libdir}/samba/libservice.so
%attr(755,root,root) %{_libdir}/samba/libshares.so
%attr(755,root,root) %{_libdir}/samba/libsmb_transport.so
%attr(755,root,root) %{_libdir}/samba/libsmbd_base.so
%attr(755,root,root) %{_libdir}/samba/libsmbd_conn.so
%attr(755,root,root) %{_libdir}/samba/libsmbd_shim.so
%attr(755,root,root) %{_libdir}/samba/libsmbpasswdparser.so
%attr(755,root,root) %{_libdir}/samba/libsmbregistry.so
%attr(755,root,root) %{_libdir}/samba/libtdb-wrap.so
%attr(755,root,root) %{_libdir}/samba/libtdb_compat.so
%attr(755,root,root) %{_libdir}/samba/libutil_cmdline.so
%attr(755,root,root) %{_libdir}/samba/libutil_ntdb.so
%attr(755,root,root) %{_libdir}/samba/libutil_reg.so
%attr(755,root,root) %{_libdir}/samba/libutil_setid.so
%attr(755,root,root) %{_libdir}/samba/libutil_tdb.so
%attr(755,root,root) %{_libdir}/samba/libwinbind-client.so
%attr(755,root,root) %{_libdir}/samba/libxattr_tdb.so
%dir %{_libdir}/samba/vfs
%attr(755,root,root) %{_libdir}/samba/vfs/acl_xattr.so
%attr(755,root,root) %{_libdir}/samba/vfs/btrfs.so
#%attr(755,root,root) %{_libdir}/samba/vfs/ceph.so
%attr(755,root,root) %{_libdir}/samba/vfs/fileid.so
%attr(755,root,root) %{_libdir}/samba/vfs/glusterfs.so
%attr(755,root,root) %{_libdir}/samba/vfs/posix_eadb.so
%attr(755,root,root) %{_libdir}/samba/vfs/xattr_tdb.so
%dir %{_datadir}/samba
%dir %{_datadir}/samba/codepages
%{_datadir}/samba/codepages/lowcase.dat
%{_datadir}/samba/codepages/upcase.dat
%{_datadir}/samba/codepages/valid.dat
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/samba-tool.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_xattr_tdb.8*

# TODO
%attr(755,root,root) %{_bindir}/ntdbbackup
%attr(755,root,root) %{_bindir}/ntdbdump
%attr(755,root,root) %{_bindir}/ntdbrestore
%attr(755,root,root) %{_bindir}/ntdbtool
%attr(755,root,root) %{_libdir}/samba/libntdb.so.*
%{_mandir}/man8/ntdbbackup.8*
%{_mandir}/man8/ntdbdump.8*
%{_mandir}/man8/ntdbrestore.8*
%{_mandir}/man8/ntdbtool.8*
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

%files common-server
%defattr(644,root,root,755)
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samba/smbusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/samba
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/samba
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.samba

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
%if %{with ldap}
%doc examples/LDAP
%endif

%files winbind
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wbinfo
%attr(755,root,root) /%{_lib}/security/pam_winbind*
%attr(755,root,root) /%{_lib}/libnss_winbind*
%attr(755,root,root) %{_libdir}/winbind_krb5_locator.so
%{_mandir}/man1/wbinfo*.1*
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man7/winbind_krb5_locator.7*
%{_mandir}/man8/pam_winbind.8*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/samba-4.0
%{_includedir}/samba-4.0/charset.h
%dir %{_includedir}/samba-4.0/core
%{_includedir}/samba-4.0/core/doserr.h
%{_includedir}/samba-4.0/core/error.h
%{_includedir}/samba-4.0/core/ntstatus.h
%{_includedir}/samba-4.0/core/werror.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/dcerpc_server.h
%{_includedir}/samba-4.0/dlinklist.h
%{_includedir}/samba-4.0/domain_credentials.h
%dir %{_includedir}/samba-4.0/gen_ndr
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
%{_includedir}/samba-4.0/gen_ndr/dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/epmapper.h
%{_includedir}/samba-4.0/gen_ndr/krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/lsa.h
%{_includedir}/samba-4.0/gen_ndr/mgmt.h
%{_includedir}/samba-4.0/gen_ndr/misc.h
%{_includedir}/samba-4.0/gen_ndr/nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_epmapper.h
%{_includedir}/samba-4.0/gen_ndr/ndr_epmapper_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/ndr_mgmt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_mgmt_c.h
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
%{_includedir}/samba-4.0/gensec.h
%{_includedir}/samba-4.0/ldap-util.h
%{_includedir}/samba-4.0/ldap_errors.h
%{_includedir}/samba-4.0/ldap_message.h
%{_includedir}/samba-4.0/ldap_ndr.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/ndr/ndr_nbt.h
%{_includedir}/samba-4.0/ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/read_smb.h
%{_includedir}/samba-4.0/registry.h
%{_includedir}/samba-4.0/roles.h
%{_includedir}/samba-4.0/rpc_common.h
%dir %{_includedir}/samba-4.0/samba
%{_includedir}/samba-4.0/samba/session.h
%{_includedir}/samba-4.0/samba/version.h
%{_includedir}/samba-4.0/samba_util.h
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2.h
%{_includedir}/samba-4.0/smb2_constants.h
%{_includedir}/samba-4.0/smb2_create_blob.h
%{_includedir}/samba-4.0/smb2_lease.h
%{_includedir}/samba-4.0/smb2_signing.h
%{_includedir}/samba-4.0/smb_cli.h
%{_includedir}/samba-4.0/smb_cliraw.h
%{_includedir}/samba-4.0/smb_common.h
%{_includedir}/samba-4.0/smb_composite.h
%{_includedir}/samba-4.0/smb_constants.h
%{_includedir}/samba-4.0/smb_raw.h
%{_includedir}/samba-4.0/smb_raw_interfaces.h
%{_includedir}/samba-4.0/smb_raw_signing.h
%{_includedir}/samba-4.0/smb_raw_trans2.h
%{_includedir}/samba-4.0/smb_request.h
%{_includedir}/samba-4.0/smb_seal.h
%{_includedir}/samba-4.0/smb_signing.h
%{_includedir}/samba-4.0/smb_unix_ext.h
%{_includedir}/samba-4.0/smb_util.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/attr.h
%{_includedir}/samba-4.0/util/byteorder.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/memory.h
%{_includedir}/samba-4.0/util/safe_string.h
%{_includedir}/samba-4.0/util/string_wrappers.h
%{_includedir}/samba-4.0/util/talloc_stack.h
%{_includedir}/samba-4.0/util/tevent_ntstatus.h
%{_includedir}/samba-4.0/util/tevent_unix.h
%{_includedir}/samba-4.0/util/tevent_werror.h
%{_includedir}/samba-4.0/util/time.h
%{_includedir}/samba-4.0/util/xfile.h
%{_includedir}/samba-4.0/util_ldb.h
%attr(755,root,root) %{_libdir}/libdcerpc-atsvc.so
%attr(755,root,root) %{_libdir}/libdcerpc-binding.so
%attr(755,root,root) %{_libdir}/libdcerpc-samr.so
%attr(755,root,root) %{_libdir}/libdcerpc-server.so
%attr(755,root,root) %{_libdir}/libdcerpc.so
%attr(755,root,root) %{_libdir}/libgensec.so
%attr(755,root,root) %{_libdir}/libndr-krb5pac.so
%attr(755,root,root) %{_libdir}/libndr-nbt.so
%attr(755,root,root) %{_libdir}/libndr-standard.so
%attr(755,root,root) %{_libdir}/libndr.so
%attr(755,root,root) %{_libdir}/libregistry.so
%attr(755,root,root) %{_libdir}/libsamba-credentials.so
%attr(755,root,root) %{_libdir}/libsamba-hostconfig.so
%attr(755,root,root) %{_libdir}/libsamba-policy.so
%attr(755,root,root) %{_libdir}/libsamba-util.so
%attr(755,root,root) %{_libdir}/libsamdb.so
%attr(755,root,root) %{_libdir}/libsmbclient-raw.so
%attr(755,root,root) %{_libdir}/libsmbconf.so
%attr(755,root,root) %{_libdir}/libtevent-util.so
%{_pkgconfigdir}/dcerpc.pc
%{_pkgconfigdir}/dcerpc_atsvc.pc
%{_pkgconfigdir}/dcerpc_samr.pc
%{_pkgconfigdir}/dcerpc_server.pc
%{_pkgconfigdir}/gensec.pc
%{_pkgconfigdir}/ndr.pc
%{_pkgconfigdir}/ndr_krb5pac.pc
%{_pkgconfigdir}/ndr_nbt.pc
%{_pkgconfigdir}/ndr_standard.pc
%{_pkgconfigdir}/registry.pc
%{_pkgconfigdir}/samba-credentials.pc
%{_pkgconfigdir}/samba-hostconfig.pc
%{_pkgconfigdir}/samba-policy.pc
%{_pkgconfigdir}/samba-util.pc
%{_pkgconfigdir}/samdb.pc
%{_pkgconfigdir}/smbclient-raw.pc
# TODO
#%if %{without system_libs}
%{_mandir}/man3/ntdb.3*
#%endif

%files -n pam-pam_smbpass3
%defattr(644,root,root,755)
%doc source3/pam_smbpass/{CHAN*,README,TODO} source3/pam_smbpass/samples
%attr(755,root,root) /%{_lib}/security/pam_smbpass.so

%files pidl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pidl
%{_mandir}/man1/pidl.1*
%{_mandir}/man3/Parse::Pidl*.3*
%{perl_vendorlib}/Parse/Pidl*

%files -n python-samba4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsamba-policy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsamba-policy.so.0
%attr(755,root,root) %{_libdir}/samba/libHDB_SAMBA4.so
%attr(755,root,root) %{_libdir}/samba/libdb-glue.so
%attr(755,root,root) %{_libdir}/samba/libsamba-net.so
%attr(755,root,root) %{_libdir}/samba/libsamba_python.so
%dir %{py_sitedir}/samba
%attr(755,root,root) %{py_sitedir}/samba/*.so
%{py_sitedir}/samba/*.py[co]
%dir %{py_sitedir}/samba/dcerpc
%{py_sitedir}/samba/dcerpc/*.py[co]
%attr(755,root,root) %{py_sitedir}/samba/dcerpc/*.so
%dir %{py_sitedir}/samba/external
%{py_sitedir}/samba/external/*.py[co]
%dir %{py_sitedir}/samba/external/subunit
%{py_sitedir}/samba/external/subunit/*.py[co]
%dir %{py_sitedir}/samba/external/subunit/tests
%{py_sitedir}/samba/external/subunit/tests/*.py[co]
%dir %{py_sitedir}/samba/netcmd
%{py_sitedir}/samba/netcmd/*.py[co]
%dir %{py_sitedir}/samba/provision
%{py_sitedir}/samba/provision/*.py[co]
%dir %{py_sitedir}/samba/samba3
%attr(755,root,root) %{py_sitedir}/samba/samba3/*.so
%{py_sitedir}/samba/samba3/*.py[co]
%dir %{py_sitedir}/samba/tests
%{py_sitedir}/samba/tests/*.py[co]
%dir %{py_sitedir}/samba/tests/blackbox
%{py_sitedir}/samba/tests/blackbox/*.py[co]
%dir %{py_sitedir}/samba/tests/samba_tool
%{py_sitedir}/samba/tests/samba_tool/*.py[co]
%dir %{py_sitedir}/samba/tests/dcerpc
%{py_sitedir}/samba/tests/dcerpc/*.py[co]
%dir %{py_sitedir}/samba/web_server
%{py_sitedir}/samba/web_server/*.py[co]
# TODO
%attr(755,root,root) %{py_sitedir}/ntdb.so
%if %{without system_libs}
%attr(755,root,root) %{py_sitedir}/ldb.so
%attr(755,root,root) %{py_sitedir}/talloc.so
%attr(755,root,root) %{py_sitedir}/tdb.so
%attr(755,root,root) %{py_sitedir}/_tevent.so
%{py_sitedir}/tevent.py[co]
%endif

%files test
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gentest
%attr(755,root,root) %{_bindir}/locktest
%attr(755,root,root) %{_bindir}/masktest
%attr(755,root,root) %{_bindir}/ndrdump
%attr(755,root,root) %{_bindir}/smbtorture
%attr(755,root,root) %{_libdir}/libtorture.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtorture.so.0
%attr(755,root,root) %{_libdir}/samba/libsubunit.so
%attr(755,root,root) %{_libdir}/samba/libdlz_bind9_for_torture.so
%{_mandir}/man1/gentest.1*
%{_mandir}/man1/locktest.1*
%{_mandir}/man1/masktest.1*
%{_mandir}/man1/ndrdump.1*
%{_mandir}/man1/smbtorture.1*

%files test-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtorture.so
%{_includedir}/samba-4.0/torture.h
%{_pkgconfigdir}/torture.pc

%files -n samba3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbwrap_tool
%attr(755,root,root) %{_bindir}/smbcontrol
%attr(755,root,root) %{_bindir}/smbpasswd
%attr(755,root,root) %{_bindir}/smbstatus
%attr(755,root,root) %{_bindir}/smbta-util
%attr(755,root,root) %{_sbindir}/mksmbpasswd.sh
%attr(755,root,root) %{_sbindir}/nmbd
%attr(755,root,root) %{_sbindir}/smbd
%attr(755,root,root) %{_libdir}/samba/auth/samba4.so
%attr(755,root,root) %{_libdir}/samba/auth/unix.so
%attr(755,root,root) %{_libdir}/samba/auth/wbc.so
%attr(755,root,root) %{_libdir}/samba/libsmbsharemodes.so.0
%dir %{_libdir}/samba/idmap
%attr(755,root,root) %{_libdir}/samba/idmap/ad.so
%attr(755,root,root) %{_libdir}/samba/idmap/autorid.so
%attr(755,root,root) %{_libdir}/samba/idmap/hash.so
%attr(755,root,root) %{_libdir}/samba/idmap/rfc2307.so
%attr(755,root,root) %{_libdir}/samba/idmap/rid.so
%attr(755,root,root) %{_libdir}/samba/idmap/tdb2.so
%attr(755,root,root) %{_libdir}/samba/vfs/acl_tdb.so
%attr(755,root,root) %{_libdir}/samba/vfs/aio_fork.so
%attr(755,root,root) %{_libdir}/samba/vfs/aio_linux.so
%attr(755,root,root) %{_libdir}/samba/vfs/aio_posix.so
%attr(755,root,root) %{_libdir}/samba/vfs/aio_pthread.so
%attr(755,root,root) %{_libdir}/samba/vfs/commit.so
%attr(755,root,root) %{_libdir}/samba/vfs/crossrename.so
%attr(755,root,root) %{_libdir}/samba/vfs/dirsort.so
%attr(755,root,root) %{_libdir}/samba/vfs/linux_xfs_sgid.so
%attr(755,root,root) %{_libdir}/samba/vfs/media_harmony.so
%attr(755,root,root) %{_libdir}/samba/vfs/preopen.so
%attr(755,root,root) %{_libdir}/samba/vfs/shadow_copy2.so
%attr(755,root,root) %{_libdir}/samba/vfs/smb_traffic_analyzer.so
%attr(755,root,root) %{_libdir}/samba/vfs/streams_depot.so
%attr(755,root,root) %{_libdir}/samba/vfs/streams_xattr.so
%attr(755,root,root) %{_libdir}/samba/vfs/syncops.so
%attr(755,root,root) %{_libdir}/samba/vfs/time_audit.so
%dir %{_libdir}/samba/pdb
%attr(755,root,root) %{_libdir}/samba/pdb/ldapsam.so
%attr(755,root,root) %{_libdir}/samba/pdb/smbpasswd.so
%attr(755,root,root) %{_libdir}/samba/pdb/tdbsam.so
%attr(755,root,root) %{_libdir}/samba/pdb/wbc_sam.so
%dir %{_libdir}/samba/nss_info
%attr(755,root,root) %{_libdir}/samba/nss_info/hash.so
%attr(755,root,root) %{_libdir}/samba/nss_info/rfc2307.so
%attr(755,root,root) %{_libdir}/samba/nss_info/sfu20.so
%attr(755,root,root) %{_libdir}/samba/nss_info/sfu.so
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man8/idmap_ad.8*
%{_mandir}/man8/idmap_autorid.8*
%{_mandir}/man8/idmap_hash.8*
%{_mandir}/man8/idmap_ldap.8*
%{_mandir}/man8/idmap_nss.8*
%{_mandir}/man8/idmap_rfc2307.8*
%{_mandir}/man8/idmap_rid.8*
%{_mandir}/man8/idmap_tdb2.8*
%{_mandir}/man8/idmap_tdb.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/smbta-util.8*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_aio_fork.8*
%{_mandir}/man8/vfs_aio_linux.8*
%{_mandir}/man8/vfs_aio_pthread.8*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_media_harmony.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_smb_traffic_analyzer.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_time_audit.8*

%files -n samba3-server
%defattr(644,root,root,755)
%attr(664,root,fileshare) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/samba/smb.conf
%attr(754,root,root) /etc/rc.d/init.d/smb
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/samba3
%{systemdunitdir}/nmb.service
%{systemdunitdir}/smb.service

%files -n samba3-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/net
%attr(755,root,root) %{_bindir}/nmblookup
%attr(755,root,root) %{_bindir}/rpcclient
%attr(755,root,root) %{_bindir}/sharesec
%attr(755,root,root) %{_bindir}/smbcacls
%attr(755,root,root) %{_bindir}/smbclient
%attr(755,root,root) %{_bindir}/smbtar
%attr(755,root,root) %{_bindir}/smbtree
%attr(755,root,root) %{_libdir}/samba/libgpo.so
%attr(755,root,root) %{_libdir}/samba/libnet_keytab.so
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man8/net.8*

%files -n samba3-common
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eventlogadm
%attr(755,root,root) %{_bindir}/ntlm_auth
%attr(755,root,root) %{_bindir}/pdbedit
%attr(755,root,root) %{_bindir}/profiles
%attr(755,root,root) %{_bindir}/smbcquotas
%attr(755,root,root) %{_bindir}/testparm
%attr(755,root,root) %{_bindir}/vfstest
%attr(755,root,root) %{_libdir}/samba/libsmbldaphelper.so
%attr(755,root,root) %{_libdir}/samba/libnss_info.so
%attr(755,root,root) %{_libdir}/samba/libidmap.so
%attr(755,root,root) %{_libdir}/samba/libtrusts_util.so
%attr(755,root,root) %{_libdir}/samba/libpopt_samba3.so
%dir %{_libdir}/samba/auth
%attr(755,root,root) %{_libdir}/samba/auth/script.so
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man1/vfstest.1*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/pdbedit.8*

%files -n samba3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetapi.so
%attr(755,root,root) %{_libdir}/libpdb.so
%attr(755,root,root) %{_libdir}/libsmbldap.so
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/netapi.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%{_includedir}/samba-4.0/smb_share_modes.h
%{_pkgconfigdir}/netapi.pc

%files -n samba3-vfs-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/audit.so
%attr(755,root,root) %{_libdir}/samba/vfs/extd_audit.so
%attr(755,root,root) %{_libdir}/samba/vfs/full_audit.so
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_full_audit.8*

%files -n samba3-vfs-cap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/cap.so
%{_mandir}/man8/vfs_cap.8*

%files -n samba3-vfs-catia
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/catia.so
%{_mandir}/man8/vfs_catia.8*

%files -n samba3-vfs-default_quota
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/default_quota.so
%{_mandir}/man8/vfs_default_quota.8*

%files -n samba3-vfs-expand_msdfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/expand_msdfs.so

%files -n samba3-vfs-fake_perms
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/fake_perms.so
%{_mandir}/man8/vfs_fake_perms.8*

%files -n samba3-vfs-notify_fam
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/notify_fam.so
%{_mandir}/man8/vfs_notify_fam.8*

%files -n samba3-vfs-netatalk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/netatalk.so
%{_mandir}/man8/vfs_netatalk.8*

%files -n samba3-vfs-readahead
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/readahead.so
%{_mandir}/man8/vfs_readahead.8*

%files -n samba3-vfs-readonly
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/readonly.so
%{_mandir}/man8/vfs_readonly.8*

%files -n samba3-vfs-recycle
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/recycle.so
%{_mandir}/man8/vfs_recycle.8*

%files -n samba3-vfs-scannedonly
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/scannedonly.so
%{_mandir}/man8/vfs_scannedonly.8*

%files -n samba3-vfs-shadow_copy
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/samba/vfs/shadow_copy.so
%{_mandir}/man8/vfs_shadow_copy.8*

%files -n smbget3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smbget
%{_mandir}/man1/smbget.1*
%{_mandir}/man5/smbgetrc.5*

%if %{with cups}
%files -n cups-backend-smb3
%defattr(644,root,root,755)
%attr(755,root,root) %{cups_serverbin}/backend/smb
%attr(755,root,root) %{_bindir}/smbspool
%{_mandir}/man8/smbspool.8*
%endif

%files -n samba3-winbind
%attr(755,root,root) %{_sbindir}/winbindd
%attr(754,root,root) /etc/rc.d/init.d/winbind
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/winbind
%{systemdunitdir}/winbind.service
%{_mandir}/man8/winbindd*.8*

%files -n nss_wins3
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_wins*

%files -n samba3-libsmbclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so.*
%attr(755,root,root) %{_libdir}/libwbclient.so.*
%{_mandir}/man7/libsmbclient.7*

%files -n samba3-libsmbclient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so
%attr(755,root,root) %{_libdir}/libwbclient.so
%{_includedir}/libsmbclient.h
%{_includedir}/wbclient.h

%if %{with ldap}
%files -n openldap-schema-samba3
%defattr(644,root,root,755)
%{schemadir}/samba.schema
%endif
