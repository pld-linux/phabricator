Summary:	Phabricator, an open software engineering platform
Name:		phabricator
Version:	0.1
Release:	0.3
License:	Apache v2.0
Group:		Applications/WWW
Source0:	https://github.com/facebook/%{name}/archive/master/phabricator.tar.gz
# Source0-md5:	9a886bfc5a077e152d9e9b59fcbd19fe
Source1:	https://github.com/facebook/libphutil/archive/master/libphutil.tar.gz
# Source1-md5:	276ec0faafabc48ca08ecab54e504b19
Source2:	https://github.com/facebook/arcanist/archive/master/arcanist.tar.gz
# Source2-md5:	22f65983592de3d919e3d356904577a9
Source3:	apache.conf
Source4:	lighttpd.conf
URL:		http://www.phabricator.org/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	php(curl)
Requires:	php(iconv)
Requires:	php(mbstring)
Requires:	php(mysqli)
Requires:	php(pcntl)
Requires:	webapps
Requires:	webserver
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Requires:	webserver(rewrite)
Suggests:	git-core
Suggests:	php(apc)
Suggests:	php(gd)
Suggests:	php(xhprof)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Phabricator is a collection of open source web applications that help
software companies build better software.

%prep
%setup -qc -a1 -a2
mv arcanist{-*,}
mv libphutil{-*,}
mv phabricator{-*,}

grep -rlE '/usr/local/bin|bin/env' . | xargs sed -i -e ' 1 {
	s,/usr/local/bin/php,/usr/bin/php,
	s,/usr/bin/env .*php,/usr/bin/php,
}'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{php_data_dir}}

cp -a arcanist $RPM_BUILD_ROOT%{php_data_dir}
cp -a libphutil $RPM_BUILD_ROOT%{php_data_dir}

cp -a phabricator/* $RPM_BUILD_ROOT%{_appdir}
# in doc already
%{__rm} $RPM_BUILD_ROOT%{_appdir}/{LICENSE,NOTICE,README}

cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc phabricator/{README,NOTICE}
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf

# there's no easy way to control file execute bits, so use defattr
%defattr(-,root,root,-)

%dir %{_appdir}
%{_appdir}/bin
%{_appdir}/conf
%{_appdir}/externals
%{_appdir}/resources
%{_appdir}/scripts
%{_appdir}/src
%{_appdir}/support
%{_appdir}/webroot

%{php_data_dir}/arcanist
%{php_data_dir}/libphutil
