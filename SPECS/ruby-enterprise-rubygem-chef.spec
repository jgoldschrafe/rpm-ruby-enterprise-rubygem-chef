%define _prefix /opt/ruby-enterprise
%define _gem %{_prefix}/bin/gem
%define _ruby %{_prefix}/bin/ruby

# Generated from chef-0.10.0.beta.9.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(%{_ruby} -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{_ruby} -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name: ruby-enterprise-rubygem-%{gemname}
Version: 0.10.4
Release: 1%{?buildstamp}%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://wiki.opscode.com/display/chef
Source0: http://rubygems.org/downloads/%{gemname}-%{version}.gem
Source1: chef-client.init
Source2: chef-client.sysconfig
Source3: chef-client.logrotate

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby-enterprise-rubygems
Requires: ruby-enterprise-rubygem(mixlib-config) >= 1.1.2
Requires: ruby-enterprise-rubygem(mixlib-cli) >= 1.1.0
Requires: ruby-enterprise-rubygem(mixlib-log) >= 1.3.0
Requires: ruby-enterprise-rubygem(mixlib-authentication) >= 1.1.0
Requires: ruby-enterprise-rubygem(ohai) >= 0.6
Requires: ruby-enterprise-rubygem(rest-client) >= 1.0.4
Requires: ruby-enterprise-rubygem(rest-client) < 1.7.0
Requires: ruby-enterprise-rubygem(bunny) >= 0.6.0
Requires: ruby-enterprise-rubygem(json) >= 1.4.4
Requires: ruby-enterprise-rubygem(json) <= 1.4.6
Requires: ruby-enterprise-rubygem(treetop) >= 1.4.9
Requires: ruby-enterprise-rubygem(net-ssh) >= 2.1.3
Requires: ruby-enterprise-rubygem(net-ssh-multi) >= 1.0.1
Requires: ruby-enterprise-rubygem(erubis) >= 0
Requires: ruby-enterprise-rubygem(moneta) >= 0
Requires: ruby-enterprise-rubygem(highline) >= 0
Requires: ruby-enterprise-rubygem(uuidtools) >= 0
Requires: ruby-enterprise >= 1.8.7
BuildRequires: ruby-enterprise-rubygems
BuildArch: noarch
Provides: ruby-enterprise-rubygem(%{gemname}) = %{version}
Obsoletes: chef

%description
A systems integration framework, built to bring the benefits of configuration
management to your entire infrastructure.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/log/chef
mkdir -p %{buildroot}%{_sysconfdir}/chef
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/var/run/chef
mkdir -p %{buildroot}/var/log/chef
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
#chef needs /var/chef/cache in 0.10
mkdir -p %{buildroot}/var/chef/cache

%{_gem} install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

cp %{SOURCE1} %{buildroot}/etc/rc.d/init.d/chef-client
chmod +x %{buildroot}/etc/rc.d/init.d/chef-client
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/chef-client
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/chef-client

%clean
rm -rf %{buildroot}

%post
if [ ! -f "%{_bindir}/chef-client" ]; then
    ln -s %{_prefix}/bin/chef-client /usr/bin/chef-client
fi

if [ ! -f "%{_bindir}/chef-solo" ]; then
    ln -s %{_prefix}/bin/chef-solo /usr/bin/chef-solo
fi

# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add chef-client

%preun
if [ "$(readlink /usr/bin/chef-client)" == "%{_prefix}/bin/chef-client" ]; then
    rm -f /usr/bin/chef-client
fi

if [ "$(readlink /usr/bin/chef-solo)" == "%{_prefix}/bin/chef-solo" ]; then
    rm -f /usr/bin/chef-solo
fi

if [ $1 -eq 0 ] ; then
    /sbin/service chef-client stop >/dev/null 2>&1
    /sbin/chkconfig --del chef-client
fi

%files
%defattr(-, root, root, -)
%{_bindir}/chef-client
%{_bindir}/chef-solo
%{_bindir}/knife
%{_bindir}/shef
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%config(noreplace) %{_sysconfdir}/sysconfig/chef-client
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-client
%{_sysconfdir}/rc.d/init.d/chef-client
/var/log/chef/
/var/chef/cache/
%config(noreplace) %{_sysconfdir}/chef


%changelog
* Mon Oct  3 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.10.4-1.hhg
- Rebuild for Ruby Enterprise Edition

* Wed Jul 27 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.4-1
- preparing for 0.10.4 RC

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-3
- updated release version format

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-2
- added buildstamp to release

* Mon Jul 04 2011 Sergio Rubio <srubio@abiquo.com> - 0.10.2-1
- upstream update

* Fri Jun 10 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-5
- patch yum provider

* Fri May 06 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-4
- create /var/log/chef dir

* Thu May 05 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-3
- require ruby >= 1.8.7

* Thu May 05 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-2
- added init script
- added logrotate script
- added sysconfig file

* Tue May 03 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-1
- upstream update

* Mon May 02 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.2-1
- upstream update

* Thu Apr 28 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-1
- upstream update

* Wed Apr 20 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.0-2
- bumped release
- create /var/chef/cache

* Wed Apr 20 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.0-1
- bumped version

* Thu Apr 14 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.beta.10-3
- depend on ohai >= 0.6

* Thu Apr 14 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.beta.10-2
- obsoletes chef

* Thu Apr 13 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.beta.10-1
- bumped version

* Tue Apr 12 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.beta.9-1
- Initial package
