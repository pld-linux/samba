Summary:	SMB client and server
Summary(pl):	Klient i serwer SMB
Name:		samba
Version:	2.0.3
Release:	1
Copyright:	GPL
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://samba.anu.edu.au/pub/samba/%{name}-%{version}.tar.gz
Source1:	%{name}.PLD.tar.gz
Patch0:		%{name}.%{version}.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-cap.patch
Prereq:		/sbin/chkconfig 
Prereq:		fileutils
Requires:	pam >= 0.66 
#Requires:	krb5-lib >= 1.0.5
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
Samba udostêpnia serwer SMB, który mo¿e byæ u¿yty w celu 
dostarczenia us³ug sieciowych (potocznie zwanych "Lan Manager"),
dla klientów takich jak M$ Windows, OS/2 a tak¿e maszyn linuxowych. 
W pakiecie znajduje siê równie¿ oprogramowanie klienckie. Samba u¿ywa 
protoko³u NetBIOS po TCP/IP (NetBT) i nie wymaga ¶miesznego protoko³u 
NetBEUI. Ta wersja ma pe³ne wsparcie dla blokowania plików, a tak¿e 
wsparcie dla kodowania hase³ w standardzie MS i zarzadzania baz± WINS.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd source
autoconf
CFLAGS=$RPM_OPT_FLAGS LDFLAGS=-s \
    ./configure \
	--sysconfdir=/etc/samba \
	--with-smbmount \
	--with-smb-wrapper \
	--with-quotas \
	--prefix=/usr \
	--with-privatedir=/etc/samba \
	--libdir=/etc/samba \
	--localstatedir=/var \
	--sbindir=/usr/sbin \
	--bindir=/usr/bin \
	--with-swatdir=/usr/share/swat
#	--with-krb5=/usr \
	
make all smbwrapper

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/samba/codepages/src
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,pam.d}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/home/samba
install -d $RPM_BUILD_ROOT/lib/security
install -d $RPM_BUILD_ROOT/usr/{bin,sbin}
install -d $RPM_BUILD_ROOT/usr/man/{man1,man5,man7,man8}
install -d $RPM_BUILD_ROOT/var/lock/samba
install -d $RPM_BUILD_ROOT/var/log/samba
install -d $RPM_BUILD_ROOT/var/spool/samba
install -d $RPM_BUILD_ROOT/usr/share/swat/{include,images,help}

( cd source;
make prefix=$RPM_BUILD_ROOT/usr \
    BASEDIR=$RPM_BUILD_ROOT/usr \
    BINDIR=$RPM_BUILD_ROOT/usr/bin \
    SBINDIR=$RPM_BUILD_ROOT/usr/sbin \
    LIBDIR=$RPM_BUILD_ROOT/etc/samba \
    PRIVATEDIR=$RPM_BUILD_ROOT/etc/samba \
    SWATDIR=$RPM_BUILD_ROOT/usr/share/swat \
    VARDIR=$RPM_BUILD_ROOT/var \
    install
)

install  source/codepages/codepage_def.* \
    $RPM_BUILD_ROOT/etc/samba/codepages/src

install  docs/manpages/*.1 $RPM_BUILD_ROOT/usr/man/man1
install  docs/manpages/*.5 $RPM_BUILD_ROOT/usr/man/man5
install  docs/manpages/*.7 $RPM_BUILD_ROOT/usr/man/man7
install  docs/manpages/*.8 $RPM_BUILD_ROOT/usr/man/man8

install  packaging/PLD/smb.conf		$RPM_BUILD_ROOT/etc/samba
install  packaging/PLD/smbusers		$RPM_BUILD_ROOT/etc/samba
install  packaging/PLD/smbprint		$RPM_BUILD_ROOT/usr/bin
install  packaging/PLD/smbadduser	$RPM_BUILD_ROOT/usr/bin
install  packaging/PLD/findsmb		$RPM_BUILD_ROOT/usr/bin
install  packaging/PLD/smb.init		$RPM_BUILD_ROOT/etc/rc.d/init.d/smb
install  packaging/PLD/samba.pam	$RPM_BUILD_ROOT/etc/pam.d/samba
install  packaging/PLD/samba.log	$RPM_BUILD_ROOT/etc/logrotate.d/samba

install swat/help/*.html docs/htmldocs/*.html \
    $RPM_BUILD_ROOT/usr/share/swat/help
install swat/images/*.gif $RPM_BUILD_ROOT/usr/share/swat/images
install swat/include/*.html $RPM_BUILD_ROOT/usr/share/swat/include

mv swat/README swat/README.swat

install -s source/bin/*.so $RPM_BUILD_ROOT/lib/security

touch $RPM_BUILD_ROOT/var/lock/samba/{STATUS..LCK,wins.dat,browse.dat}

echo 127.0.0.1 > $RPM_BUILD_ROOT/etc/samba/lmhosts

for i in 437 737 850 852 861 866 932 949 950 936; do
$RPM_BUILD_ROOT/usr/bin/make_smbcodepage c $i \
$RPM_BUILD_ROOT/etc/samba/codepages/src/codepage_def.$i \
$RPM_BUILD_ROOT/etc/samba/codepages/codepage.$i; done

gzip -9fn $RPM_BUILD_ROOT/usr/man/man[1578]/*
gzip -9  README Manifest WHATSNEW.txt Roadmap docs/*.reg swat/README.swat

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smb

# Not for PLD
#if !( grep ^[:space:]*swat /etc/services > /dev/null ) then
#echo 'swat	901/tcp		# Swat service used via inetd' >> /etc/services
#fi

# Not for PLD 
#if !( grep ^[:space:]*swat /etc/inetd.conf > /dev/null ) then
#echo 'swat	stream	tcp	nowait.400	root	/usr/sbin/swat swat' >> /etc/inetd.conf
#killall -HUP inetd >&2
#fi

%preun
if [ $1 = 0 ]; then
    /etc/rc.d/init.d/smb stop >&2
    /sbin/chkconfig --del smb
fi
# Not for PLD 
#    cd /etc
#    tmpfile=/etc/tmp.$$
#    sed -e '/^[:space:]*swat.*$/d' /etc/inetd.conf > $tmpfile
#    mv $tmpfile inetd.conf
#    sed -e '/^[:space:]*swat.*$/d' /etc/services > $tmpfile
#    mv $tmpfile services
#fi

%files
%defattr(644,root,root,755)
%doc README.gz Manifest.gz WHATSNEW.txt.gz swat/README.swat.gz
%doc Roadmap.gz docs/faq/*.html docs/*.reg.gz 

%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/*

%dir /etc/samba
%config(noreplace) %verify(not size mtime md5) /etc/samba/smb.conf
%attr(600,root,root) %config %verify(not size mtime md5) /etc/samba/smbusers
%attr(640,root,root) %config %verify(not size mtime md5) /etc/samba/lmhosts

%attr(750,root,root) %config /etc/rc.d/init.d/smb
%attr(640,root,root) /etc/logrotate.d/samba
%attr(640,root,root) /etc/pam.d/samba

%attr(755,root,root) /lib/security/*.so

%attr(644,root, man) /usr/man/man[1578]/*

%dir /home/samba
%dir /etc/samba/codepages
/etc/samba/codepages/*

%dir /usr/share/swat

%dir /usr/share/swat/help
/usr/share/swat/help/*.html

%dir /usr/share/swat/include
/usr/share/swat/include/*.html

%dir /usr/share/swat/images
/usr/share/swat/images/*.gif

%attr(750,root,root) %dir /var/lock/samba
%attr(640,root,root) /var/lock/samba/*

%attr(0750,root, root) %dir /var/log/samba
%attr(1777,root, root) %dir /var/spool/samba

%changelog
* Sun Mar 28 1999 Ziemek Borowski <zmb@ziembor.waw.pl>
[2.0.3] 
- updated to 2.0.3 (change in samba.2.0.3.patch file)
- removed kerberos support

* Tue Jan 26 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.2.0-1d]
- updated to new version,
- added Group(pl),
- added patch against GNU libc-2.1 -- prepared by Paul Laufer
  http://www.cspupomona.edu/~pelaufer/samba,
- some other changes ...

* Wed Aug 05 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.9.18p8-1d]
- build against glibc-2.1,
  patch prepared by Paul Laufer <PELaufer@csupomona.edu>
  http://www.netcom.com/~mlaufer/samba,
- translation modified for pl,
- build with Kerberos V support,
- moved %changelog at the end of spec,
- build from non root's acccount,
- changed permisions of binaries to 755,
- moved config files to /etc/samba instead /etc,
- added a sticky bit on /var/spool/samba,
- minor modifications of spec.

* Sat Jul 4 1998 John H Terpstra <jht@samba.anu.edu.au>
  - changed classification of codepage source files
  - altered installation of samba system files
  - modified doc handling (removed attribute setting parameters)

* Sat Jun 13 1998 John H Terpstra <jht@samba.anu.edu.au>
  - Added code pages 737 and 861 to files section
  - Added auto-generation of empty /etc/lmhosts file if not exist
  - Always zap and create empty /var/lock/samba/STATUS..LCK file

* Wed Jun 10 1998 John H Terpstra <jht@samba.anu.edu.au>
  - Updated version info for 1.9.18p8 release
  - updated codepage support for pages 737 861

* Sun Apr 26 1998 John H Terpstra <jht@samba.anu.edu.au>
  - minor tidy up in preparation for release of 1.9.18p5
  - added findsmb utility from SGI package

* Wed Mar 18 1998 John H Terpstra <jht@samba.anu.edu.au>
  - Updated version and codepage info.
  - Release to test name resolve order

* Sat Jan 24 1998 John H Terpstra <jht@samba.anu.edu.au>
 - Many optimisations (some suggested by Manoj Kasichainula <manojk@io.com>
  - Use of chkconfig in place of individual symlinks to /etc/rc.d/init/smb
  - Compounded make line
  - Updated smb.init restart mechanism
  - Use compound mkdir -p line instead of individual calls to mkdir
  - Fixed smb.conf file path for log files
  - Fixed smb.conf file path for incoming smb print spool directory
  - Added a number of options to smb.conf file
  - Added smbadduser command (missed from all previous RPMs) - Doooh!
  - Added smbuser file and smb.conf file updates for username map
