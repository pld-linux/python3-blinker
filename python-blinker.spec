#
# Conditional build:
%bcond_with	doc		# don't build doc (not provided by package)
%bcond_with	tests	# do not perform "make test" (not provided by package)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	blinker
Summary:	Fast, simple object-to-object and broadcast signaling
Summary(pl.UTF-8):	Szybkie, proste przesyłanie sygnałów pomiędzy obiektami
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	1.3
Release:	5
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/b/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	66e9688f2d287593a0e698cd8a5fbc57
URL:		http://pythonhosted.org/blinker/
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.710
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
# Below Rs only work for main package (python2)
#Requires:		python-libs
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blinker provides a fast dispatching system that allows any number of
interested parties to subscribe to events, or "signals". Signal
receivers can subscribe to specific senders or receive signals sent by
any sender.

%description -l pl.UTF-8
Blinker dostarcza szybki system rozporowadzania sygnałów który
pozawala na dowolną liczbe odbiorców zdarzeń czy szygnałów. Odbiorcy
sygnałów mogą zapisywac się do wybranych nadawców czy odbierać sygnały
nadadane przez wszystkich nadawców.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Blinker provides a fast dispatching system that allows any number of
interested parties to subscribe to events, or "signals". Signal
receivers can subscribe to specific senders or receive signals sent by
any sender.

%description -n python3-%{module} -l pl.UTF-8
Blinker dostarcza szybki system rozporowadzania sygnałów który
pozawala na dowolną liczbe odbiorców zdarzeń czy szygnałów. Odbiorcy
sygnałów mogą zapisywac się do wybranych nadawców czy odbierać sygnały
nadadane przez wszystkich nadawców.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README LICENSE
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README LICENSE
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
