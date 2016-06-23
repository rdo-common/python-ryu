%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name ryu

Name:           python-%{pypi_name}
Version:        4.3
Release:        1%{?dist}
Summary:        Component-based Software-defined Networking Framework

License:        Apache-2.0
Url:            https://osrg.github.io/ryu
Source:         https://pypi.io/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
Ryu provides software components with well defined API that make it easy for developers to create new
network management and control applications.

%package -n     python2-%{pypi_name}
Summary:        Component-based Software-defined Networking Framework

Requires:  python-eventlet
Requires:  python-debtcollector
Requires:  python-lxml
Requires:  python-msgpack
Requires:  python-netaddr
Requires:  python-oslo-config
Requires:  python-paramiko
Requires:  python-routes
Requires:  python-six
Requires:  python-webob
Requires:  python-%{pypi_name}-common = %{version}-%{release}

BuildRequires:  pylint
BuildRequires:  python2-devel
BuildRequires:  python-coverage
BuildRequires:  python-debtcollector
BuildRequires:  python-eventlet
BuildRequires:  python-formencode
BuildRequires:  python-greenlet
BuildRequires:  python-lxml
BuildRequires:  python-mock
BuildRequires:  python-msgpack
BuildRequires:  python-nose
BuildRequires:  python-oslo-config
BuildRequires:  python-paramiko
BuildRequires:  python-pep8
BuildRequires:  python-repoze-lru
BuildRequires:  python-routes
BuildRequires:  python-sphinx
BuildRequires:  python-setuptools
BuildRequires:  python-webob

%description -n python2-%{pypi_name}
Ryu provides software components with well defined API that make it easy for developers to create new
network management and control applications.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Component-based Software-defined Networking Framework
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:  python3-eventlet
Requires:  python3-debtcollector
Requires:  python3-lxml
Requires:  python3-msgpack
Requires:  python3-netaddr
Requires:  python3-oslo-config
Requires:  python3-paramiko
Requires:  python3-routes
Requires:  python3-six
Requires:  python3-webob
Requires:  python-%{pypi_name}-common = %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-coverage
BuildRequires:  python3-debtcollector
BuildRequires:  python3-eventlet
BuildRequires:  python3-formencode
BuildRequires:  python3-greenlet
BuildRequires:  python3-lxml
BuildRequires:  python3-mock
BuildRequires:  python3-msgpack
BuildRequires:  python3-nose
BuildRequires:  python3-oslo-config
BuildRequires:  python3-paramiko
BuildRequires:  python3-pep8
BuildRequires:  python3-repoze-lru
BuildRequires:  python3-routes
BuildRequires:  python3-sphinx
BuildRequires:  python3-setuptools
BuildRequires:  python3-webob

%description -n python3-%{pypi_name}
Ryu provides software components with well defined API that make it easy for developers to create new
network management and control applications.

This is the Python 3 version.
%endif

%package -n python-%{pypi_name}-common
Summary:        Component-based Software-defined Networking Framework

%description -n python-%{pypi_name}-common
Ryu provides software components with well defined API that make it easy for developers to create new
network management and control applications.

This package contains common data between python 2 and 3 versions

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

# FIXME: pip tries to download a specific version of pylint when running tests
sed -i 's/==0.25.0//' tools/test-requires

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

cd doc && make man

%install
%if 0%{?with_python3}
%py3_install
for bin in %{pypi_name}{,-manager}; do
    mv %{buildroot}%{_bindir}/$bin  %{buildroot}%{_bindir}/$bin-%{python3_version}
    ln -s ./$bin-%{python3_version} %{buildroot}%{_bindir}/$bin-3
done;
%endif

%py2_install
for bin in %{pypi_name}{,-manager}; do
    mv %{buildroot}%{_bindir}/$bin  %{buildroot}%{_bindir}/$bin-%{python2_version}
    ln -s ./$bin-%{python2_version} %{buildroot}%{_bindir}/$bin-2
    ln -s ./$bin-%{python2_version} %{buildroot}%{_bindir}/$bin
done;

install -d -m 755 %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}%{_prefix}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf

%check
# FIXME: requires missing package tinyrpc
#%if 0%{?with_python3}
#%{__python3} setup.py test
#%endif
#%{__python2} setup.py test

%files -n     python2-%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{pypi_name}
%{_bindir}/%{pypi_name}
%{_bindir}/%{pypi_name}-2
%{_bindir}/%{pypi_name}-%{python2_version}
%{_bindir}/%{pypi_name}-manager
%{_bindir}/%{pypi_name}-manager-2
%{_bindir}/%{pypi_name}-manager-%{python2_version}


%if 0%{?with_python3}
%files -n     python3-%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{pypi_name}
%{_bindir}/%{pypi_name}
%{_bindir}/%{pypi_name}-3
%{_bindir}/%{pypi_name}-%{python3_version}
%{_bindir}/%{pypi_name}-manager
%{_bindir}/%{pypi_name}-manager-3
%{_bindir}/%{pypi_name}-manager-%{python3_version}
%endif

%files -n     python-%{pypi_name}-common
%doc AUTHORS ChangeLog README.rst
%license LICENSE
%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf



%changelog
* Thu Jun 23 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 4.3-1
- Upstream 4.3
- Enable python3 subpackage

* Thu Apr  7 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 3.30-1
- Upstream 3.30

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Arie Bregman <abregman@redhat.com> - 3.26-1
- Initial package.
