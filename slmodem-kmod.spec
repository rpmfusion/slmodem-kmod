# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

%define   filever 2.9.11-20080817
%define   datetag 20080817
%define   ungrab_datetag 20080126


Name:           slmodem-kmod
Version:        2.9.11
Release:        27%{?dist}.34
Summary:        Proprietary SmartLink softmodem kernel drivers

Group:          System Environment/Kernel
License:        Distributable
# Outdated
# URL:          http://www.smlink.com/content.aspx?id=132
URL:            http://linmodems.technion.ac.il/packages/smartlink/
Source0:        http://linmodems.technion.ac.il/packages/smartlink/slmodem-%{filever}.tar.gz
Source1:        http://linmodems.technion.ac.il/packages/smartlink/ungrab-winmodem-%{ungrab_datetag}.tar.gz

Patch0:         slmodem-kmod-Makefile.patch
Patch10:        slmodem-kmod-ungrab.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# ppc and ppc64 disabled -- upstream package only contains 32bit-x86 blob
# Kernel module can be built for x86_64 but a 32bit userland is necessary
# This is not done though, as it is rather hackish.
ExclusiveArch:  i586 i686

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
%{summary}

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
%setup -q -D -T -a 1

# apply patches and do other stuff here
# pushd foo-%{version}
# #patch0 -p1 -b .suffix
# popd
pushd slmodem-%{filever}
%patch0 -p 1 -b .Make
popd

pushd ungrab-winmodem-%{ungrab_datetag}
%patch10 -p 1 -b .Make
popd

for kernel_version  in %{?kernel_versions} ; do
    cp -a slmodem-%{filever} _kmod_build_${kernel_version%%___*}
    cp -a ungrab-winmodem-%{ungrab_datetag} _kmod_build_${kernel_version%%___*}/ungrab-winmodem
done


%build
for kernel_version  in %{?kernel_versions} ; do
    pushd  _kmod_build_${kernel_version%%___*}/drivers
    make %{?_smp_mflags} \
        KSRC=${kernel_version##*___} \
        KVERS=${kernel_version%%___*}
    popd

    pushd _kmod_build_${kernel_version%%___*}/ungrab-winmodem
    make %{?_smp_mflags} \
        KSRC="${kernel_version##*___}" \
        KVERS=%${kernel_version%%___*}
    popd
done


%install
rm -rf %{buildroot}
for kernel_version  in %{?kernel_versions} ; do
    install -p -D -m 0755 _kmod_build_${kernel_version%%___*}/drivers/slamr.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/slamr.ko
    test -f _kmod_build_${kernel_version%%___*}/drivers/slusb.ko && install -p -D -m 0755 _kmod_build_${kernel_version%%___*}/drivers/slusb.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/slusb.ko
    install -p -D -m 0755 _kmod_build_${kernel_version%%___*}/ungrab-winmodem/ungrab-winmodem.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ungrab-winmodem.ko
done

%{?akmod_install}


%clean
rm -rf %{buildroot}


%changelog
* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.34
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.33
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.32
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.31
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.30
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.29
- rebuild for new kernels

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.28
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.27
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.26
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.25
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.24
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.23
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.22
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.21
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.20
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-27.19
- rebuild for new F11 features

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.19
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.18
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.17
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.16
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.15
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.14
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.13
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.12
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.11
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.10
- rebuilt

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.9
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.8
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.3
- rebuild for latest rawhide kernel

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.9.11-26.2
- rebuild for latest rawhide kernel

* Thu Oct 16 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-26
- small adjustments for the kmod stuff

* Thu Oct 16 2008 Andreas Thienemann <andreas@bawue.net> - 2.9.11-25
- Updated to recent upstream kernel
- Prevent build failure on kernels > 2.6.24

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-24
- rebuild for new kmodtools, akmod adjustments

* Mon Jan 21 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-23
- build akmods package

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-22
- rebuilt for 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-21
- rebuilt for 2.6.23.8-63.fc8 2.6.21-2952.fc8xen

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-20
- rebuilt for 2.6.23.1-49.fc8

* Mon Nov 05 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-19
- rebuilt for F8 kernels

* Wed Oct 31 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-18
- rebuilt for latest kernels

* Tue Oct 30 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-17
- rebuilt for latest kernels

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-16
- rebuilt for latest kernels
- adjust to rpmfusion and new kmodtool

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-15
- rebuilt for latest kernels

* Tue Oct 23 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-14
- rebuilt for latest kernels

* Mon Oct 22 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-13
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-12
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-11
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-10
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-9
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.9.11-8
- rebuilt for latest kernels

* Tue Oct 09 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 2.9.11-7
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> 
- build for rawhide kernels as of today

* Wed Oct 03 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 2.9.11-5.20070813
- update for new kmod-helper stuff
- build for newest kernels

* Sun Sep 09 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 2.9.11-4.20070813
- Convert to new kmods stuff from livna for testing it
- Rebuild for F8T2 and rawhide

* Sat Sep 08 2007 Andreas Thienemann <andreas@bawue.net> - 2.9.11-3.20070813
- Updated to the newest snapshot

* Wed Feb 07 2007 Andreas Thienemann <andreas@bawue.net> - 2.9.11-2.20070204
- Updated to the newest snapshot
- Cleaned up the .spec and incorporated some changes from thl
- Used new kmodtool script as suggested by thl

* Fri Apr 28 2006 Andreas Thienemann <andreas@bawue.net> - 2.9.11-1
- Initial Package, inspired by fglrx-kmod
