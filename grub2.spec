%define Werror_cflags %nil

# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif
#sparc is always compile 64 bit
%ifarch %{sparc}
%define _target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif

Name:           grub2
Version:        1.98
Release:        %mkrel 1
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System/Kernel and hardware
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Source0:        http://alpha.gnu.org/pub/gnu/grub/grub-%{version}.tar.gz
Source1:        90_persistent
Source2:        grub.default
Source3:        README.Mandriva
Patch0:         grub-1.95-grubdir.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  flex bison ruby binutils glibc-static-devel
BuildRequires:  ncurses-devel liblzo-devel
BuildRequires:  freetype2-devel libusb-devel

# grubby
Requires(pre):  mkinitrd
Requires(post): mkinitrd

# TODO: ppc and sparc
ExclusiveArch:  %{ix86} x86_64

%description
This is the second version of the GRUB (Grand Unified Bootloader),
a highly configurable and customizable bootloader with modular
architecture.  It support rich scale of kernel formats, file systems,
computer architectures and hardware devices.

PLEASE NOTE: This is a development snapshot, and as such will not
replace grub if you install it, but will be merely added as another
kernel to your existing GRUB menu. Do not replace GRUB (grub package)
with it unless you know what are you doing. Refer to README.Mandriva
file that is part of this package's documentation for more information.


%prep
%setup -q -n grub-%{version}

%patch0 -p1 -b .grubdir

# README.Mandriva
cp %{SOURCE3} .


%build
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%configure TARGET_LDFLAGS=-static       \
%ifarch %{sparc}
        --with-platform=ieee1275        \
%else
        --with-platform=pc              \
%endif
        --enable-grub-emu-usb           \
        --program-transform-name=s,grub,%{name},
# TODO: Other platforms. Use alternatives system?
#       --with-platform=ieee1275        \
#       --with-platform=efi             \
#       --with-platform=i386-pc         \


#make %{?_smp_mflags}
#gcc -Inormal -I./normal -I. -Iinclude -I./include -Wall -W -DGRUB_LIBDIR=\"/usr/lib/`echo grub/i386-pc | sed 's&^&&;s,grub,grub2,'`\" -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -DGRUB_UTIL=1  -MD -c -o grub_emu-normal_lexer.o normal/lexer.c
#In file included from normal/lexer.c:23:
#include/grub/script.h:26:29: error: grub_script.tab.h: No such file or directory
%make


%install
set -e
rm -fr $RPM_BUILD_ROOT
%makeinstall_std

# Script that makes part of grub.cfg persist across updates
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d/

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg

# Install ELF files modules and images were created from into
# the shadow root, where debuginfo generator will grab them from
find $RPM_BUILD_ROOT -name '*.mod' -o -name '*.img' |
while read MODULE
do
        BASE=$(echo $MODULE |sed -r "s,.*/([^/]*)\.(mod|img),\1,")
        # Symbols from .img files are in .exec files, while .mod
        # modules store symbols in .elf. This is just because we
        # have both boot.img and boot.mod ...
        EXT=$(echo $MODULE |grep -q '.mod' && echo '.elf' || echo '.exec')
        TGT=$(echo $MODULE |sed "s,$RPM_BUILD_ROOT,.debugroot,")
#        install -m 755 -D $BASE$EXT $TGT
done

# Defaults
install -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/grub

%find_lang grub

%clean
rm -rf $RPM_BUILD_ROOT

%post
exec >/dev/null 2>&1
# Create device.map or reuse one from GRUB Legacy
cp -u /boot/grub/device.map /boot/%{name}/device.map 2>/dev/null ||
        %{name}-mkdevicemap
# Determine the partition with /boot
BOOT_PARTITION=$(df -h /boot |(read; awk '{print $1; exit}'))
# Generate core.img, but don't let it be installed in boot sector
%{name}-install --grub-setup=/bin/true $BOOT_PARTITION


%preun
exec >/dev/null
/sbin/grubby --remove-kernel=/boot/%{name}/core.img
# XXX Ugly
rm -f /boot/%{name}/*.mod
rm -f /boot/%{name}/*.img
rm -f /boot/%{name}/*.lst
rm -f /boot/%{name}/device.map


%triggerin -- kernel, kernel-PAE
exec >/dev/null 2>&1
# Generate grub.cfg
grub2-mkconfig -o /boot/%{name}/grub.cfg

%triggerun -- kernel, kernel-PAE
exec >/dev/null 2>&1
# Generate grub.cfg
grub2-mkconfig -o /boot/%{name}/grub.cfg


%files -f grub.lang
%defattr(-,root,root,-)
%{_libdir}/%{name}
%dir %{_prefix}/lib/grub
%{_prefix}/lib/grub/grub-mkconfig_lib
%{_prefix}/lib/grub/update-grub_lib
%{_sbindir}/%{name}-mkdevicemap
%{_sbindir}/%{name}-install
#%{_sbindir}/%{name}-emu # FIXME?
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-setup
#%{_sbindir}/update-%{name}
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mkelfimage
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%else
%{_sbindir}/%{name}-ofpathname
%endif
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-bin2h
%{_bindir}/%{name}-mkisofs
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-script-check
%dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%{_sysconfdir}/%{name}.cfg
%{_sysconfdir}/default/grub
%dir /boot/%{name}
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/%{name}/grub.cfg
%doc COPYING INSTALL NEWS README THANKS TODO ChangeLog README.Mandriva
%exclude %{_mandir}
