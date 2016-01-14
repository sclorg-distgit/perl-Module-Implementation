%{?scl:%scl_package perl-Module-Implementation}
%{!?scl:%global pkg_name %{name}}

# Test::CPAN::Changes isn't available in EPEL < 7, due to requirement of perl(version) ≥ 0.79
%global cpan_changes_available %(expr 0%{?fedora} + 0%{?rhel} '>' 6)

#TODO: BR: Test::Pod::No404s when available
#TODO: BR: Test::Pod::LinkCheck when available

Name:		%{?scl_prefix}perl-Module-Implementation
Version:	0.07
Release:	6.sc1%{?dist}
Summary:	Loads one of several alternate underlying implementations for a module
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/perl-Module-Implementation/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Module-Implementation-%{version}.tar.gz
Patch1:		Module-Implementation-0.07-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.30
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(Module::Runtime) >= 0.012
BuildRequires:	%{?scl_prefix}perl(Try::Tiny)
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(warnings)
# ===================================================================
# Test suite requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(File::Find)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(lib)
BuildRequires:	%{?scl_prefix}perl(Test::Fatal) >= 0.006
BuildRequires:	%{?scl_prefix}perl(Test::More)
BuildRequires:	%{?scl_prefix}perl(Test::Requires)
BuildRequires:	%{?scl_prefix}perl(Test::Taint)
# ===================================================================
# Author/Release test requirements
# ===================================================================
%if ! 0%{?scl:1}
%if %{cpan_changes_available}
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Changes) >= 0.19
%endif
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage)
# Can't use aspell-en from EPEL as BR: for RHEL-7+ package, and older EL
# releases don't have recent enough Test::Spelling so skip author tests
# there
%if ! 0%{?rhel}
BuildRequires:	%{?scl_prefix}aspell-en
BuildRequires:	%{?scl_prefix}perl(Pod::Wordlist::hanekomu)
BuildRequires:	%{?scl_prefix}perl(Test::Spelling) >= 0.12
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:	%{?scl_prefix}perl(Carp)

# We need to patch the test suite if we have an old version of Test::More
%{?scl:%global old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.96) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.96 ? 1 : 0);' 2>/dev/null || echo 0)}

%description
This module abstracts out the process of choosing one of several underlying
implementations for a module. This can be used to provide XS and pure Perl
implementations of a module, or it could be used to load an implementation
for a given OS or any other case of needing to provide multiple
implementations.

This module is only useful when you know all the implementations ahead of
time. If you want to load arbitrary implementations then you probably want
something like a plugin system, not this module.

%prep
%setup -q -n Module-Implementation-%{version}

# We have to patch the test suite if we have an old Test::More
%if 00%{old_test_more}
%patch1 -p1
%endif

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
# Don't run the author/release tests for SCL builds
%if 0%{?scl:1}
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}
%else
# Don't run the author tests for EL builds (see above)
%if ! 0%{?rhel}
%{?scl:scl enable %{scl} "}
make test AUTHOR_TESTING=1 RELEASE_TESTING=1
%{?scl:"}
%else
%{?scl:scl enable %{scl} "}
make test RELEASE_TESTING=1
%{?scl:"}
%endif
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Implementation.3pm*

%changelog
* Tue Feb 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-6
- Fixed getting of %%old_test_more
- Resolves: rhbz#1063206

* Mon Feb 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-5
- Get correct value for %%old_test_more on SCL
- Resolves: rhbz#1063206

* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-4
- Rebuilt for SCL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.07-2
- Perl 5.18 rebuild

* Mon Jul 15 2013 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Require Test::Fatal ≥ 0.006 to avoid test failures (CPAN RT#76809)
- Explicitly run author tests, except for EL builds
- Add buildreqs for new tests
- Apply old Test::More patch if we have Test::More < 0.96

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.06-4
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.06-3
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from buildroot
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-2
- Conditionalize aspell-en dependency

* Sun Feb 12 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Require Module::Runtime 0.012, which has a number of useful bug fixes

* Fri Feb 10 2012 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Make Test::Taint an optional dependency; it requires XS, and requiring a
    compiler for Module::Implementation defeats its purpose (CPAN RT#74817)
- BR: perl(Test::Requires)
- Update patch for building with old Test::More versions

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - This module no longer installs an _implementation() subroutine in callers;
    instead, you can call Module::Implementation::implementation_for($package)
    to get the implementation used for a given package
- Update patch for building with old Test::More versions

* Wed Feb  8 2012 Paul Howarth <paul@city-fan.org> - 0.03-3
- Incorporate feedback from package review (#788258)
  - Correct License tag, which should be Artistic 2.0
  - BR: perl(lib) for test suite
  - Explicitly require perl(Carp), not automatically detected

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Sanitize for Fedora submission

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
