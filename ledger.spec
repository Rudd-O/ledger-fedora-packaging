Name:           ledger
Version:        2.6.3
Release:        8%{?dist}.2
Summary:        A powerful command-line double-entry accounting system
Group:          Applications/Productivity
License:        BSD
URL:            http://www.newartisans.com/software/ledger.html
Source0:        http://ftp.newartisans.com/pub/ledger/%{name}-%{version}.tar.gz
Source1:        ledger.1
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gmp-devel, pcre-devel, expat-devel, libofx-devel, emacs(bin), texinfo
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post):  info
Requires(preun): info

%description
Ledger is a powerful, double-entry accounting system that is accessed
from the UNIX command-line. This may put off some users — as there is
no flashy UI — but for those who want unparalleled reporting access to
their data, there really is no alternative.

%package devel
Summary: Libraries and header files for %{name} development
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
Development files for the ledger library libamounts.

%package -n emacs-%{name}
Summary: Emacs mode for %{name}
Requires: %{name} = %{version}-%{release}
Requires: emacs(bin) >= %{_emacs_version}
%description -n emacs-%{name}
Emacs mode for %{name}.

%package -n emacs-%{name}-el
Summary: Emacs elisp source for %{name}
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: emacs-%{name} = %{version}-%{release}
%description -n emacs-%{name}-el
This package contains the elisp source files for using %{name} under
emacs. You do not need to install this package; use
emacs-%{name} instead.

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 ledger.texi > _ledger.texi
sed -e 's/@documentencoding iso-8859-1/@documentencoding utf-8/' _ledger.texi > ledger.texi
chmod -x scripts/*

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_infodir}/dir
rm %{buildroot}%{_libdir}/*.la

install -v -m 644 -D %{SOURCE1} %{buildroot}/%{_mandir}/man1/%{name}.1

%clean
rm -rf %{buildroot}

%postun -p /sbin/ldconfig
%post
ldconfig
install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
%preun
if [ $1 = 0 ]; then
  install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE NEWS README TODO sample.dat scripts/
%{_bindir}/*
%{_infodir}/%{name}*
%{_libdir}/lib*.so.*
%{_mandir}/man*/*

%files -n emacs-%{name}
%defattr(-,root,root,-)
%{_emacs_sitelispdir}/*.elc

%files -n emacs-%{name}-el
%defattr(-,root,root,-)
%{_emacs_sitelispdir}/*.el

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/lib*.a

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.6.3-6.2
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.3-4.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-4.1
- rebuild with new gmp

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 2.6.3-3
- Rebuilt for gcc bug 634757

* Tue Jul  6 2010 Jim Radford <radford@blackbean.org> - 2.6.3-2
- Only support emacs until someone tests xemacs

* Tue Jul  6 2010 Jim Radford <radford@blackbean.org> - 2.6.3-1
- Upgrade to 2.6.2

* Thu Jan  1 2009 Jim Radford <radford@blackbean.org> - 2.6.1-1
- Initial release
