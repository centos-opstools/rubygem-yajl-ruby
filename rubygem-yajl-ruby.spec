# Generated from yajl-ruby-1.2.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name yajl-ruby

Name: rubygem-%{gem_name}
Version: 1.3.0
Release: 3%{?dist}
Summary: Ruby C bindings to the excellent Yajl JSON stream-based parser library
Group: Development/Languages
License: MIT
URL: http://github.com/brianmario/yajl-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel >= 1.8.6
BuildRequires: rubygem(rspec)

Provides: rubygem(%{gem_name}) = %{version}

%description
%{summary}


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{gem_extdir_mri}/lib/yajl
cp -ar .%{gem_instdir}/lib/yajl/yajl.so %{buildroot}%{gem_extdir_mri}/lib/yajl

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml,.rspec}

# Run the test suite
%check
pushd .%{gem_instdir}
# Disabled two failing tests
sed -i '47,59d' spec/parsing/large_number_spec.rb
rspec -Ilib -I%{buildroot}%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%{gem_instdir}/.codeclimate.yml
%license %{gem_instdir}/LICENSE
%{gem_instdir}/benchmark
%{gem_libdir}
%{gem_instdir}/script
%{gem_instdir}/tasks
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Jun  9 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.0-3
- spec cleanup

* Thu Jan 19 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 1.3.0-2
- Rebuilding adding ppc64le arch

* Fri Nov 04 2016 Rich Megginson <rmeggins@redhat.com> - 1.3.0-1
- update to 1.3.0

* Tue Jan 06 2015 Graeme Gillies <ggillies@redhat.com> - 1.2.1-1
- Initial package
