%{?scl:%scl_package perl-Module-Implementation}

#TODO: BR: Test::CleanNamespaces when available

Name:		%{?scl_prefix}perl-Module-Implementation
Version:	0.09
Release:	9%{?dist}
Summary:	Loads one of several alternate underlying implementations for a module
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/perl-Module-Implementation/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Module-Implementation-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
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
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(IO::Handle)
BuildRequires:	%{?scl_prefix}perl(IPC::Open3)
BuildRequires:	%{?scl_prefix}perl(lib)
BuildRequires:	%{?scl_prefix}perl(Test::Fatal) >= 0.006
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.96
BuildRequires:	%{?scl_prefix}perl(Test::Requires)
# ===================================================================
# Optional test requirements
# ===================================================================
BuildRequires:	%{?scl_prefix}perl(CPAN::Meta) >= 2.120900
%if !%{defined perl_small}
BuildRequires:	%{?scl_prefix}perl(Test::Taint)
# ===================================================================
# Author/Release test requirements
# ===================================================================
# Release tests include circular dependencies, so don't do them when bootstrapping:
%if ! %{defined perl_bootstrap}
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Changes) >= 0.19
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod) >= 1.41
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	%{?scl_prefix}perl(Test::Portability::Files)
# Can't use EPEL packages as BR: for RHEL package
%if ! 0%{?rhel}
BuildRequires:	aspell-en
BuildRequires:	%{?scl_prefix}perl(Pod::Wordlist)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::LinkCheck)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::No404s)
BuildRequires:	%{?scl_prefix}perl(Test::Spelling) >= 0.12
%endif
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:	%{?scl_prefix}perl(Carp)

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

# Can't try namespace-cleanliness.t until we have Test::CleanNamespaces
sed -i -e '/namespace-cleanliness.t/d' MANIFEST t/00-report-prereqs.t t/author-no-tabs.t
rm t/namespace-cleanliness.t

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc LICENSE
%doc Changes README.md
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Implementation.3pm*

%changelog
* Wed Jul 13 2016 Petr Pisar <ppisar@redhat.com> - 0.09-9
- SCL

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-8
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-4
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Implemented and then reverted a change to use Sub::Name (CPAN RT#98097)
- Modernize spec
- Hack out references to currently-unavailable Test::CleanNamespaces

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-6
- Perl 5.20 rebuild

* Tue Aug 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-5
- Do not run release and author tests on bootstrap

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
