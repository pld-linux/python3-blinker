#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define 	module	blinker
Summary:	Fast, simple object-to-object and broadcast signaling
Summary(pl.UTF-8):	Szybkie, proste przesyłanie sygnałów pomiędzy obiektami
Name:		python3-%{module}
Version:	1.9.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/blinker/
Source0:	https://files.pythonhosted.org/packages/source/b/blinker/%{module}-%{version}.tar.gz
# Source0-md5:	1ffce54aca3d568ab18ee921d479274f
URL:		https://pythonhosted.org/blinker/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.5
%if %{with tests}
BuildRequires:	python3-nose
%endif
%if %{with doc}
BuildRequires:	python3-flask_sphinx_themes
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blinker provides a fast dispatching system that allows any number of
interested parties to subscribe to events, or "signals". Signal
receivers can subscribe to specific senders or receive signals sent by
any sender.

%description -l pl.UTF-8
Blinker dostarcza szybki system rozporowadzania sygnałów, który
pozwala na dowolną liczbę odbiorców zdarzeń czy sygnałów. Odbiorcy
sygnałów mogą zapisywać się do wybranych nadawców lub odbierać sygnały
nadadane przez wszystkich nadawców.

%package apidocs
Summary:	Blinker API documentation
Summary(pl.UTF-8):	Dokumentacja API modułu Blinker
Group:		Documentation

%description apidocs
API documentation for Blinker.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Blinker.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=asyncio \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,*.html,*.js}
%endif
