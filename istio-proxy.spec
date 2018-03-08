# don't strip binaries at all
%global __strip			/bin/true
%global debug_package		%{nil}

# don't byte compile the ./examples ...
%global __spec_install_post	/usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
				/usr/lib/rpm/brp-compress

# they warn against doing this ... :-\
%define _disable_source_fetch 0

Name:		istio-proxy
Version:	0.6.0
Release:	1%{?dist}
Summary:	The Istio proxy component

License:	ASL 2.0
URL:		https://github.com/istio/proxy
Source0:	https://github.com/istio/proxy/archive/%{version}.tar.gz

# see https://copr.fedorainfracloud.org/coprs/vbatts/bazel/
BuildRequires:	bazel

BuildRequires:	wget
BuildRequires:	rsync
BuildRequires:	make
BuildRequires:	git
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	bc
BuildRequires:	libtool
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:	gdb
BuildRequires:	strace
BuildRequires:	python-virtualenv
BuildRequires:	which
BuildRequires:	golang
BuildRequires:	clang
BuildRequires:	cmake3
BuildRequires:	coreutils

BuildRequires:	centos-release-scl
BuildRequires:	devtoolset-4-gcc
BuildRequires:	devtoolset-4-gcc-c++
BuildRequires:	devtoolset-4-libatomic-devel
BuildRequires:	devtoolset-4-libstdc++-devel
BuildRequires:	devtoolset-4-runtime

%description
%{summary}.

%prep
%setup -q -n proxy-%{version}

%build

ln -s /usr/bin/cmake3 cmake
export PATH=$(pwd):$PATH

scl enable devtoolset-4 -- bazel --batch --bazelrc=/dev/null build --verbose_failures --config=release //...

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp -pav bazel-bin/src/envoy/envoy $RPM_BUILD_ROOT/%{_bindir}/envoy

%files
%license LICENSE
%{_bindir}/envoy


%changelog
* Thu Mar 08 2018 Jonh Wendell <jonh.wendell@redhat.com> 0.6.0-1
- First package
