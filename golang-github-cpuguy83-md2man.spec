%bcond_without check

%if ! 0%{?gobuild:1}
%define gobuild(o:) \
GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -linkmode=external -compressdwarf=false -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v %{?**};
%endif

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
ln -s vendor src
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{import_path}
export GOPATH=$(pwd)
export CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
%ifarch x86_64
export CGO_CFLAGS+=" -fcf-protection=full"
%endif
%gobuild -o bin/go-md2man %{import_path}

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
