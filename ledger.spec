%define _emacs_sitelispdir %{_datadir}/emacs/site-lisp
Name:           ledger
Version:        2.6.3
Release:        3%{?dist}.1
Summary:        A powerful command-line double-entry accounting system
Group:          Applications/Productivity
License:        BSD
URL:            http://www.newartisans.com/software/ledger.html
Source0:        http://ftp.newartisans.com/pub/ledger/%{name}-%{version}.tar.gz
Source1:        ledger.1
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gmp-devel, pcre-devel, expat-devel, libofx-devel, emacs, texinfo
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
Group: Applications/Editors
Requires: %{name} = %{version}-%{release}
Requires: emacs-common >= %{_emacs_version}
%description -n emacs-%{name}
Emacs mode for %{name}.

%package -n emacs-%{name}-el
Summary: Emacs elisp source for %{name}
Group: Applications/Editors
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
* Mon Sep 13 2010 Jim Radford <radford@blackbean.org> - 2.6.3-3
- Add a Group to the emacs packages

* Tue Jul  6 2010 Jim Radford <radford@blackbean.org> - 2.6.3-2
- Only support emacs until someone tests xemacs

* Tue Jul  6 2010 Jim Radford <radford@blackbean.org> - 2.6.3-1
- Upgrade to 2.6.2

* Thu Jan  1 2009 Jim Radford <radford@blackbean.org> - 2.6.1-1
- Initial release
