%define Werror_cflags %nil

# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif

# Hack to include debuginfo for files, that find-debuginfo.sh wouldn't
# have spot, because they're either no longer ELF images, such as
# boot images, or are brutally and insensitively stripped, such as
# modules. See %%install.
# It's certainly not the nicest thing you've ever seen.
# THAT IS NOT MY FAULT.
# We do not use find-debuginfo.sh -o here, as it's not supported in RHEL5
%define __debug_install_post                                            \
                                                                        \
        # Gather debuginfo as usual                                     \
        /usr/lib/rpm/find-debuginfo.sh                                \\\
                %{_builddir}/%{?buildsubdir}                            \
                mv debugfiles.list debug1.list                          \
                                                                        \
        # Gather debuginfo of modules from shadow build root            \
        RPM_BUILD_ROOT=%{_builddir}/%{?buildsubdir}/.debugroot        \\\
                /usr/lib/rpm/find-debuginfo.sh                        \\\
                %{_builddir}/%{?buildsubdir}                            \
                mv debugfiles.list debug2.list                          \
                                                                        \
        # Merge debuginfos                                              \
        cp -a %{_builddir}/%{?buildsubdir}/.debugroot/usr/lib/debug   \\\
                $RPM_BUILD_ROOT/usr/lib                                 \
        cp -a %{_builddir}/%{?buildsubdir}/.debugroot/usr/src/debug   \\\
                $RPM_BUILD_ROOT/usr/src                                 \
        sort debug1.list debug2.list |uniq >debugfiles.list             \
                                                                        \
        %{nil}

Name:           grub2
Version:        1.98
Release:        0.3.20080827svn.%mkrel 1
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System/Kernel and hardware
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
#Source0:        http://alpha.gnu.org/pub/gnu/grub/grub-%{version}.tar.gz
# svn -r1829 co svn://svn.sv.gnu.org/grub/trunk/grub2
# tar czf grub2.tar.gz --exclude .svn grub2
Source0:        grub2.tar.gz
Source1:        90_persistent
Source2:        grub.default
Source3:        README.Mandriva
Patch1:         grub-1.98-prototypes.patch
Patch2:         grub-1.98-transform.patch
Patch4:         grub-1.95-grubdir.patch
Patch5:         grub-1.98-os.patch
Patch6:         grub-1.97-cfgmode.patch
Patch7:         grub-1.96-garbage.patch
Patch8:         grub-1.98-persistent.patch
Patch9:         grub-1.98-linuxsort.patch
Patch10:        http://fedorapeople.org/~lkundrak/grub2/grub2-dlsym-v4.patch
#Patch13:        http://fedorapeople.org/~lkundrak/grub2/grub2-preserve-symbols-v4.patch
Patch13:        grub2-preserve-symbols-v4.1.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  flex bison ruby binutils
BuildRequires:  ncurses-devel liblzo-devel

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
%setup -q -n grub2

%patch1 -p0 -b .prototypes
%patch2 -p1 -b .transform
%patch4 -p1 -b .grubdir
%patch5 -p1 -b .os
%patch6 -p1 -b .cfgmode
%patch7 -p1 -b .garbage
%patch8 -p1 -b .persistent
%patch9 -p0 -b .linuxsort
%patch10 -p1 -b .dlsym
%patch13 -p1 -b .preserve-symbols

# README.Mandriva
cp %{SOURCE3} .


%build
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%configure TARGET_LDFLAGS=-static       \
        --with-platform=pc              \
        --enable-grub-emu               \
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
make DESTDIR=$RPM_BUILD_ROOT install

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
        install -m 755 -D $BASE$EXT $TGT
done

# Defaults
install -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/grub


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
# Remove stale menu.lst entries
/sbin/grubby --remove-kernel=/boot/%{name}/core.img
# Add core.img as multiboot kernel to GRUB Legacy menu
/sbin/grubby --add-kernel=/boot/%{name}/core.img --title="GNU GRUB 2, (%{version})"


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
update-%{name}


%triggerun -- kernel, kernel-PAE
exec >/dev/null 2>&1
# Generate grub.cfg
update-%{name}


%files
%defattr(-,root,root,-)
%{_libdir}/%{name}
%{_sbindir}/%{name}-mkdevicemap
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-emu
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-setup
%{_sbindir}/update-%{name}
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mkelfimage
%{_bindir}/%{name}-mkrescue
%{_bindir}/%{name}-editenv
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
