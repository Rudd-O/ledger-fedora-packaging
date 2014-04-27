%global commit 7be70aab59051aa358547a3e530cc95490c04232

Name:             ledger
Version:          3.0.2
Release:          1%{?dist}
Summary:          A powerful command-line double-entry accounting system
Group:            Applications/Productivity
License:          BSD
URL:              http://ledger-cli.org/
Source0:          https://github.com/ledger/ledger/archive/%{commit}/%{name}-%{version}.tar.gz

# This requires boost 1.55 which is not yet available for Fedora.
Patch0:           %{name}-3.0.2-Revert-Require-the-use-of-C-11.patch

BuildRequires:    boost-devel
BuildRequires:    cmake
BuildRequires:    emacs(bin)
BuildRequires:    gettext-devel
BuildRequires:    gmp-devel
BuildRequires:    libedit-devel
BuildRequires:    mpfr-devel
BuildRequires:    python
BuildRequires:    utf8cpp-devel

# For building documentation.
BuildRequires:    doxygen
BuildRequires:    graphviz
BuildRequires:    man2html
BuildRequires:    texinfo
BuildRequires:    texlive-cm-super
BuildRequires:    texlive-ec
BuildRequires:    texlive-eurosym
BuildRequires:    texinfo-tex

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post):   info
Requires(preun):  info

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
Development files for the ledger library libledger.

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
%setup -q -n %{name}-%{commit}
%patch0 -p1


%build
./acprep --prefix=%{_prefix} update
%cmake . \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_WEB_DOCS=1 \
    -DBUILD_EMACSLISP:BOOL=ON \
    -DCMAKE_SKIP_RPATH:BOOL=ON
make %{?_smp_mflags}
make doc

# Build info files.
pushd doc
makeinfo ledger3.texi
makeinfo ledger-mode.texi
popd


%install
make install DESTDIR=%{buildroot}

# Install documentation manually
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_infodir}/*

cp -p doc/ledger3.info* %{buildroot}%{_infodir}
cp -p doc/ledger-mode.info %{buildroot}%{_infodir}


%check
# Tests all fail when removing rpath.
# make check


%postun -p /sbin/ldconfig
%post
/sbin/ldconfig
install-info %{_infodir}/ledger3.info %{_infodir}/dir || :
install-info %{_infodir}/ledger-mode.info %{_infodir}/dir || :
%preun
if [ $1 = 0 ]; then
  install-info --delete %{_infodir}/ledger3.info %{_infodir}/dir || :
  install-info --delete %{_infodir}/ledger-mode.info %{_infodir}/dir || :
fi


%files
%doc README.md
%doc doc/GLOSSARY.md doc/LICENSE doc/NEWS
%doc doc/ledger3.html doc/ledger-mode.html
%doc doc/ledger3.pdf  doc/ledger-mode.pdf
%doc test/input/drewr3.dat test/input/drewr.dat test/input/sample.dat
%{_bindir}/ledger
%{_infodir}/ledger3.info*
%{_infodir}/ledger-mode.info*
%{_libdir}/libledger.so.3
%{_mandir}/man1/ledger.1*

%files -n emacs-%{name}
%dir %{_emacs_sitelispdir}/ledger-mode
%{_emacs_sitelispdir}/ledger-mode/*.elc

%files -n emacs-%{name}-el
%dir %{_emacs_sitelispdir}/ledger-mode
%{_emacs_sitelispdir}/ledger-mode/*.el

%files devel
%{_includedir}/ledger
%{_libdir}/libledger.so


%changelog
* Sun Apr 27 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 3.0.2-1
- update to upstream release 3.0.2
- remove EL6 related macros
- update URL
- use specific commit hash to obtain sources from GitHub
- update BuildRequires and build using CMake
- build HTML/PDF documentation
- revert a patch from upstream that requires boost 1.55 (not yet available
  on Fedora)
- libamounts now known as libledger
- use man page that is now built by upstream

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-9.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
