%bcond_without check

%global debug_package %{nil}

# https://github.com/cpuguy83/go-md2man
%global provider github
%global provider_tld com
%global project cpuguy83
%global repo go-md2man
%global import_path github.com/cpuguy83/go-md2man
%global commit0 af8da765f0460ccb1d91003b4945a792363a94ca
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global common_description %{expand:
Converts markdown into roff (man pages).}

%global golicenses      LICENSE.md
%global godocs          README.md go-md2man.1.md

Name: golang-github-cpuguy83-md2man
Version: 2.0.0
Release: 10%{?dist}
Summary: Converts markdown into roff (man pages)
License: MIT
URL: https://%{import_path}
ExcludeArch: %{ix86}
Source0: %{url}/archive/%{commit0}.tar.gz
BuildRequires: golang
BuildRequires: git-core
Provides: %{repo} = %{version}-%{release}
Provides: golang-%{provider}-%{project}-%{repo} = %{version}-%{release}

%description
%{common_description}

%prep
%autosetup -Sgit -n %{repo}-%{commit0}

%build
%{__make}

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%endif

%files
%license %{golicenses}
%doc %{godocs}
%{_bindir}/*

%changelog
* Mon Feb 28 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2.0.0-10
- centos 8 doesn't like autospec
