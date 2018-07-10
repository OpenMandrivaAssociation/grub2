%define libdir32 %{_exec_prefix}/lib

%ifarch %{ix86} x86_64
%define platform pc
%endif

%ifarch armv7hnl
%define platform uboot
%endif

%ifarch aarch64
%define platform efi
%endif

%define debug_package %{nil}
%define snapshot 20180620

%global efi %{ix86} x86_64 aarch64
%define efidir openmandriva

%bcond_with talpo

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
Version:	2.02
Release:	9
Group:		System/Kernel and hardware
License:	GPLv3+
Url:		http://www.gnu.org/software/grub/
%if "%{snapshot}" == ""
Source0:	http://ftp.gnu.org/pub/gnu/grub/grub-%{version}.tar.xz
%else
# git clone git://git.sv.gnu.org/grub.git
# git archive --format=tar --prefix grub-2.02-$(date +%Y%m%d)/ HEAD | xz -vf > grub-2.02-$(date +%Y%m%d).tar.xz
Source0:	grub-%{version}-%{snapshot}.tar.xz
%endif
Source1:	90_persistent
Source2:	grub.default
Source3:	grub.melt
# www.4shared.com/archive/lFCl6wxL/grub_guidetar.html
Source4:	grub_guide.tar.gz
Source5:	DroidSansMonoLicense.txt
Source6:	DroidSansMono.ttf
Source8:	grub2-po-update.tar.gz
Source9:	update-grub2
Source10:	README.urpmi
Source11:	grub2.rpmlintrc
Source12:	grub-lua-rev30.tar.xz
# documentation and simple test script for testing grub2 themes
Source13:	mandriva-grub2-theme-test.sh
Source14:	linguas.tar.xz
# Used to generate source 14
Source15:	linguas.sh
Patch0:		grub2-locales.patch
Patch1:		grub2-00_header.patch
Patch2:		grub2-custom-color.patch
Patch3:		grub2-read-cfg.patch
Patch4:		grub2-symlink-is-garbage.patch
Patch5:		grub2-name-corrections.patch
# itchka not required for cooker as fuse3 is default named as fuse
#Patch6:		grub-2.02-fuse3.patch
Patch7:		grub-2.00.Linux.remove.patch
Patch8:		grub-2.00-fix-dejavu-font.patch
Patch9:		grub2-2.00-class-via-os-prober.patch
Patch10:	grub-2.00-autoreconf-sucks.patch
Patch11:	0468-Don-t-write-messages-to-the-screen.patch
Patch12:	grub-2.00-add-recovery_option.patch
Patch16:	grub-2.02-remove-efivar-kernel-module-requirement.patch
Patch17:	grub-2.02-beta2-custom-vendor-config.patch
# (tpg) add support for initrd generated by kernel-install
Patch18:	grub2-2.02-add-support-for-kernel-install.patch
# (tpg) latest v8 version of the F2FS patch
# https://lists.gnu.org/archive/html/grub-devel/2016-03/msg00080.html
# Maintained here:
# https://github.com/frap129/grub-f2fs/
# This is now in grub git and will be released in V2.04
#Patch19:	grub-add-f2fs-support-2017_05.patch
# (bero) Load Intel microcode if it exists
#Patch20:	grub-2.02-load-microcode.patch
Patch21:	fix-microcode-os-prober-initrd-line-parsing.patch
Patch22:	grub-2.02-20180620-disable-docs.patch
# Revert http://git.savannah.gnu.org/cgit/grub.git/patch/?id=0ba90a7f017889d32a47897d9107ef45cc50a049
# because of http://savannah.gnu.org/bugs/?53517
Patch23:	revert-0ba90a7f017889d32a47897d9107ef45cc50a049.patch

BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fontpackages-devel
BuildRequires:	unifont
BuildRequires:	fonts-ttf-dejavu
# (tpg) these breaks build
#BuildRequires:	fonts-ttf-tamil
BuildRequires:	unifont-fonts
BuildRequires:	help2man
BuildRequires:	rsync
BuildRequires:	texinfo
BuildRequires:	texlive-tex.bin
BuildRequires:	glibc-static-devel
BuildRequires:	gettext-devel
BuildRequires:	lzo-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(ncursesw)

%if %{with talpo}
BuildRequires:	talpo
%endif
Provides:	bootloader
Suggests:	xorriso
Suggests:	os-prober
Suggests:	distro-theme-common
Suggests:	distro-theme-OpenMandriva-grub2
%ifarch %{ix86} x86_64
Suggests:	microcode-intel
%endif
Conflicts:	grub2-tools < 2.02-1.beta2.6
%rename		grub2-tools
Suggests:	%{name}-doc = %{EVRD}
Suggests:	%{name}-extra = %{EVRD}
%ifarch %{efi}
Requires:	%{name}-efi = %{EVRD}
%endif

%description
GNU GRUB is a Multiboot boot loader. It was derived from GRUB, the
GRand Unified Bootloader, which was originally designed and implemented
by Erich Stefan Boleyn.

Briefly, a boot loader is the first software program that runs when a
computer starts. It is responsible for loading and transferring control
to the operating system kernel software (such as the Hurd or Linux).
The kernel, in turn, initializes the rest of the operating system (e.g. GNU).

%ifarch %{efi}
%package efi
Summary:	GRUB for EFI systems
Group:		System/Kernel and hardware
# (tpg) this is needed to sign our EFI image
#BuildRequires:	pesign
Requires:	efibootmgr
Conflicts:	%{name} < 2.02-8

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture. 

It support rich variety of kernel formats, file systems, computer 
architectures and hardware devices.  This subpackage provides support 
for EFI systems.
%endif

%package extra
Summary:	Extra tools for GRUB
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 2.02-8

%description extra
Extra tools and files for GRUB.

%package starfield-theme
Summary:	An example theme for GRUB
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}

%description starfield-theme
Example 'starfield' theme for GRUB.

%package doc
Summary:	Documentation for GRUB
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 2.02-8

%description doc
Documentation for GRUB.

#-----------------------------------------------------------------------

%prep
%if "%{snapshot}" == ""
%setup -qn grub-%{version} -a12 -a14
%else
%setup -qn grub-%{version}-%{snapshot} -a12 -a14
%endif
%apply_patches

cp %{SOURCE10} .

perl -pi -e 's/(\@image\{font_char_metrics,,,,)\.(png\})/$1$2/;' \
	docs/grub-dev.texi

perl -pi -e "s|(^FONT_SOURCE=)|\$1%{SOURCE6}|;" configure configure.ac

sed -ri -e 's/-g"/"/g' -e "s/-Werror//g" configure.ac
perl -pi -e 's/-Werror//;' grub-core/Makefile.am
mkdir grub-extras
mv lua grub-extras
export GRUB_CONTRIB=./grub-extras
sed -i -e 's,-I m4,-I m4 --dont-fix,g' autogen.sh

tar -xf %{SOURCE8}
cd po-update; sh ./update.sh; cd -

#-----------------------------------------------------------------------
%build
%define _disable_ld_no_undefined 1
export GRUB_CONTRIB="$PWD/grub-extras"
export CONFIGURE_TOP="$PWD"

#(proyvind): debugedit will fail on some binaries if linked using gold
# https://savannah.gnu.org/bugs/?34539
# https://sourceware.org/bugzilla/show_bug.cgi?id=14187
./autogen.sh

#(proyvind): non-UEFI boot will fail with 'alloc magic broken' on x86_64
#            if built with clang
%if "%{platform}" != ""
mkdir -p %{platform}
pushd %{platform}
%configure CC=gcc BUILD_CC=gcc TARGET_CC=gcc \
%if %{with talpo}
	CC=talpo  \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%endif
	CFLAGS="-O2 -fuse-ld=bfd" \
	TARGET_LDFLAGS="-static" \
	--with-platform=%{platform} \
%ifarch x86_64
	--enable-efiemu \
%endif
	--program-transform-name=s,grub,%{name}, \
	--libdir=%{libdir32} \
	--libexecdir=%{libdir32} \
	--with-grubdir=grub2 \
	--disable-werror \
	--enable-device-mapper \
	--enable-grub-mkfont \
	--enable-device-mapper \
	--enable-grub-emu-sdl

%make -j1 all
popd
%endif

%ifarch %{efi}
mkdir -p efi
pushd efi
%configure BUILD_CC=%{__cc} TARGET_CC=%{__cc} \
%if %{with talpo}
	CC=talpo \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%else
	CFLAGS="-O2 -fuse-ld=bfd" \
%endif
	TARGET_LDFLAGS="-static" \
	--with-platform=efi \
	--program-transform-name=s,grub,%{name}-efi, \
	--libdir=%{libdir32} \
	--libexecdir=%{libdir32} \
	--with-grubdir=grub2 \
	--disable-werror \
	--enable-grub-mkfont \
	--enable-device-mapper \
	--enable-grub-emu-sdl

%make ascii.h widthspec.h
%make -C grub-core

%define grub_modules_default btrfs cat chain configfile echo efifwsetup efinet ext2 f2fs fat font gfxmenu gfxterm gfxterm_background gfxterm_menu grub-core gzio halt hfsplus iso9660 jpeg loadenv loopback linux lsefi lua lvm mdraid09 mdraid1x minicmd normal part_apple part_gpt part_msdos password_pbkdf2 png reboot regexp search search_fs_file search_fs_uuid search_label serial sleep sleep squash4 syslinuxcfg test tftp video xfs

%ifarch aarch64
%define grubefiarch arm64-efi
%define grub_modules %{grub_modules_default}
%else
%define grubefiarch %{_arch}-efi
%define grub_modules %{grub_modules_default} all_video boot multiboot multiboot2 linuxefi blscfg
%endif

#This line loads all the modules but makes the efi image unstable.
#./grub-mkimage -O %{grubefiarch} -p /EFI/openmandriva/%{name}-efi -o grub.efi -d grub-core `ls grub-core/*.mod | sed 's/.*\///g' | sed 's/\.mod//g' | xargs
#` In practice the grub.efi image is only required for the iso. when grub is installed it selects the modules it needs to boot the current install from the installed
#  OS.

#These lines produce a grub.efi suitable for an iso. Note the path in the -p option it points to the grub.cfg file on the iso.
../%{platform}/grub-mkimage -O %{grubefiarch} -C xz -p /EFI/BOOT -o grub.efi -d %{grub_modules}

# sign our EFI image
# %pesign -s -i grub.efi.org -o grub.efi

popd
%endif


#-----------------------------------------------------------------------
%install
######legacy
%if %{platform}
%makeinstall_std -C %{platform}

# Script that makes part of grub.cfg persist across updates
install -m755 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/grub.d/90_persistent

# Ghost config file
install -d %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
ln -s /boot/%{name}/grub.cfg %{buildroot}%{_sysconfdir}/%{name}.cfg
%endif

######EFI
%ifarch %{efi}
%makeinstall_std -C efi/grub-core

install -m755 efi/grub.efi -D %{buildroot}/boot/efi/EFI/%{efidir}/grub.efi

# Ghost config file
touch %{buildroot}/boot/efi/EFI/%{efidir}/grub.cfg
ln -s /boot/efi/EFI/%{efidir}/grub.cfg %{buildroot}%{_sysconfdir}/%{name}-efi.cfg
%endif

# Defaults
install -m755 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/default/grub
# (tpg) use default distro name
sed -e 's#TMP_DISTRO#%{distribution}#' -i %{buildroot}%{_sysconfdir}/default/grub

#Add more useful update-grub2 script
install -m755 %{SOURCE9} -D %{buildroot}%{_sbindir}

install -d %{buildroot}/boot/%{name}/themes/

#bugfix: error message before loading of grub2 menu on boot
mkdir -p %{buildroot}%{_localedir}/en/LC_MESSAGES
ln %{buildroot}%{_localedir}/en@quot/LC_MESSAGES/grub.mo %{buildroot}%{_localedir}/en/LC_MESSAGES

# (tpg) remove *.modules and leave *.mod
find %{buildroot}%{libdir32}/grub/*-%{platform} -name "*.module" -delete

rm %{buildroot}%{_sbindir}/%{name}-sparc64-setup
rm %{buildroot}%{_sbindir}/%{name}-ofpathname

%find_lang grub

%post
exec >/dev/null 2>&1

if [ -e /boot/grub/device.map ]; then
# Create device.map or reuse one from GRUB Legacy
    cp -u /boot/grub/device.map /boot/%{name}/device.map 2>/dev/null ||
    %{_sbindir}/%{name}-mkdevicemap
fi

# Do not install grub2 if running in a chroot
# http://stackoverflow.com/questions/75182/detecting-a-chroot-jail-from-within
if [ "$(stat -c %d:%i /)" = "$(stat -c %d:%i /proc/1/root/.)" ]; then
# Determine the partition with /boot
    BOOT_PARTITION=$(df -h /boot |(read; awk '{print $1; exit}'|sed 's/[[:digit:]]*$//'))
# (Re-)Generate core.img, but don't let it be installed in boot sector
    %{_sbindir}/%{name}-install $BOOT_PARTITION
# Generate grub.cfg and add GRUB2 chainloader to menu on initial install
    if [ $1 = 1 ]; then
	%{_sbindir}/update-grub2
    fi

# (tpg) run only on update
    if [ $1 -ge 2 ]; then
# (tpg) remove wrong line in boot options
	if [ -e %{_sysconfdir}/default/grub ]; then
	    if grep -q "init=/lib/systemd/systemd" %{_sysconfdir}/default/grub; then
		sed -i -e 's#init=/lib/systemd/systemd##g' %{_sysconfdir}/default/grub
	    fi
# (tpg) handle backlight parameter for varsious kernel versions
	    if grep -q "acpi_backlight=vendor" %{_sysconfdir}/default/grub && [[ $(uname -r | awk -F[-] '{print $1}') < "4.3.0" ]] ; then
		sed -e 's#acpi_backlight=vendor# video.use_native_backlight=1 #g' %{_sysconfdir}/default/grub
	    fi
	    if grep -q "video.use_native_backlight=1" %{_sysconfdir}/default/grub && [[ $(uname -r | awk -F[-] '{print $1}') > "4.3.0" ]] ; then
		sed -e 's#video.use_native_backlight=1# acpi_backlight=vendor #g' %{_sysconfdir}/default/grub
	    fi
# (tpg) disable audit messages
	    if ! grep -q "^GRUB_CMDLINE_LINUX_DEFAULT.*audit=0.*" %{_sysconfdir}/default/grub; then
		sed -i -e 's#^GRUB_CMDLINE_LINUX_DEFAULT\=\"#GRUB_CMDLINE_LINUX_DEFAULT\=\" audit=0 #' %{_sysconfdir}/default/grub
	    fi
# (tpg) remove resume= as it is not needed with tuxonice
	    if grep -q "resume=" %{_sysconfdir}/default/grub; then
		sed -i -e 's#resume=[Aa/-Zz/]*\s##g' %{_sysconfdir}/default/grub
	    fi
# (tpg) set GRUB_SAVEDEFAULT=false to fix bug https://issues.openmandriva.org/show_bug.cgi?id=1814
# (tpg) revert because of https://issues.openmandriva.org/show_bug.cgi?id=1915
	    if grep -q "GRUB_SAVEDEFAULT=" %{_sysconfdir}/default/grub; then
		sed -i -e 's#GRUB_SAVEDEFAULT=false#GRUB_SAVEDEFAULT=true#g' %{_sysconfdir}/default/grub
	    fi
# (tpg) set acpi_osi=Linux
	    if ! grep -q "acpi_osi=Linux" %{_sysconfdir}/default/grub; then
		sed -i -e 's#^GRUB_CMDLINE_LINUX_DEFAULT\=\"#GRUB_CMDLINE_LINUX_DEFAULT\=\" acpi_osi=Linux #' %{_sysconfdir}/default/grub
	    fi
# (tpg) set acpi_osi='!Windows 2012' for modern UEFI
	    if ! grep -q "acpi_osi='\!Windows 2012'" %{_sysconfdir}/default/grub; then
		sed -i -e "s#^GRUB_CMDLINE_LINUX_DEFAULT\=\"#GRUB_CMDLINE_LINUX_DEFAULT\=\" acpi_osi='\!Windows 2012' #" %{_sysconfdir}/default/grub
	    fi
# (tpg) enable Multi-Queue Block IO Queueing Mechanism
	    if ! grep -q "scsi_mod.use_blk_mq=1" %{_sysconfdir}/default/grub; then
		sed -i -e "s#^GRUB_CMDLINE_LINUX_DEFAULT\=\"#GRUB_CMDLINE_LINUX_DEFAULT\=\" scsi_mod.use_blk_mq=1 #" %{_sysconfdir}/default/grub
	    fi
# (tpg) regenerate grub2 at the end
	    %{_sbindir}/update-grub2
	fi
    fi
fi


%transfiletriggerin -p <lua> -- /boot/ /boot/grub2/themes/
os.execute("%{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg")

%transfiletriggerpostun -p <lua> -- /boot/ /boot/grub2/themes/
os.execute("%{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg")

%preun
exec >/dev/null
if [ $1 = 0 ]; then
# XXX Ugly
    rm -f /boot/%{name}/*.mod ||:
    rm -f /boot/%{name}/*.img ||:
    rm -f /boot/%{name}/*.lst ||:
    rm -f /boot/%{name}/*.o ||:
    rm -f /boot/%{name}/device.map ||:
fi

#-----------------------------------------------------------------------
%files  -f grub.lang
%{libdir32}/grub/*-%{platform}
#Files here are needed for install. Moved from efi package
%{libdir32}/grub/%{_arch}-efi/
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-mount
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-file
%{_sbindir}/update-grub2
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_datadir}/grub
%exclude %{_datadir}/grub/themes/*
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%{_sysconfdir}/grub.d/README
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/%{name}.cfg
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/bash_completion.d/grub
%dir /boot/%{name}
%dir /boot/%{name}/themes
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/%{name}/grub.cfg

%files extra
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkrescue
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-syslinux2cfg
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man8/%{name}-*.8*

%ifarch %{efi}
%attr(0755,root,root) %dir /boot/efi/EFI/%{efidir}
%attr(0755,root,root) %ghost %config(noreplace) /boot/efi/EFI/%{efidir}/grub.cfg
%files efi
# Files in this package are only required for the creation of iso's
# The install process creates all the files required to boot with grub via EFI
%attr(0755,root,root) /boot/efi/EFI/%{efidir}/grub.efi
#%attr(0755,root,root) %ghost %config(noreplace) /boot/efi/EFI/%{efidir}/grub.cfg
%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg
%{_bindir}/%{name}-render-label
%{_sbindir}/%{name}-macbless
%endif

%files starfield-theme
%{_datadir}/grub/themes/starfield

%files doc
%doc NEWS README THANKS TODO
#{_docdir}/%{name}
#{_infodir}/%{name}.info*
#{_infodir}/grub-dev.info*
