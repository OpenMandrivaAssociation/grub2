%define libdir32 %{_exec_prefix}/lib
%define platform pc
%define efi 1
%define debug_package %{nil}
%define snapshot 20150804

%global efi %{ix86} x86_64

%bcond_with talpo

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
Version:	2.02
Release:	1.beta2.24
Group:		System/Kernel and hardware
License:	GPLv3+
Url:		http://www.gnu.org/software/grub/
#Source0:	http://ftp.gnu.org/pub/gnu/grub/grub-%{version}.tar.xz
# git git://git.sv.gnu.org/grub.git
# git archive --format=tar --prefix grub-2.02-$(date +%Y%m%d)/ HEAD | xz -vf > grub-2.02-$(date +%Y%m%d).tar.xz
Source0:	grub-%{version}-%{snapshot}.tar.xz
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
Source14:	linguas.sh

Patch0:		grub2-locales.patch
Patch1:		grub2-00_header.patch
Patch2:		grub2-custom-color.patch
Patch3:		grub2-read-cfg.patch
Patch4:		grub2-symlink-is-garbage.patch
Patch5:		grub2-name-corrections.patch
Patch7:		grub-2.00.Linux.remove.patch
Patch8:		grub-2.00-fix-dejavu-font.patch
Patch9:		grub2-2.00-class-via-os-prober.patch
Patch10:	grub-2.00-autoreconf-sucks.patch
Patch11:	0468-Don-t-write-messages-to-the-screen.patch
Patch12:	grub-2.00-add-recovery_option.patch
Patch13:	grub2-2.02~beta2-class-via-os-prober.patch
Patch16:	grub-2.02-remove-efivar-kernel-module-requirement.patch
Patch17:	grub-2.02-beta2-custom-vendor-config.patch

BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fontpackages-devel
BuildRequires:	unifont
BuildRequires:	fonts-ttf-dejavu
BuildRequires:	fonts-ttf-tamil
BuildRequires:	unifont-fonts
BuildRequires:	help2man
BuildRequires:	rsync
BuildRequires:	texinfo
BuildRequires:	texlive-latex
BuildRequires:	texlive-epsf
BuildRequires:	texlive-kpathsea.bin
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
Suggests:	xorriso
Provides:	bootloader
Requires:	os-prober
Requires:	distro-theme-common
Conflicts:	grub2-tools < 2.02-1.beta2.6
%rename		grub2-tools
Requires(post):	grub2-theme

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

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture. 

It support rich variety of kernel formats, file systems, computer 
architectures and hardware devices.  This subpackage provides support 
for EFI systems.
%endif

%package	starfield-theme
Summary:	An example theme for GRUB
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}
Provides:	%{name}-theme

%description	starfield-theme
Example 'starfield' theme for GRUB.

#-----------------------------------------------------------------------

%prep
%setup -qn grub-%{version}-%{snapshot} -a12
%apply_patches

cp %{SOURCE10} .

perl -pi -e 's/(\@image\{font_char_metrics,,,,)\.(png\})/$1$2/;' \
	docs/grub-dev.texi

mkdir grub-extras
mv lua grub-extras
export GRUB_CONTRIB=./grub-extras
sed -i -e 's,-I m4,-I m4 --dont-fix,g' autogen.sh
cp %{SOURCE14} .
sh linguas.sh

tar -xf %{SOURCE8}
pushd po-update; sh ./update.sh; popd

./autogen.sh

perl -pi -e "s|(^FONT_SOURCE=)|\$1%{SOURCE6}|;" configure configure.ac
sed -ri -e 's/-g"/"/g' -e "s/-Werror//g" configure configure.ac
perl -pi -e 's/-Werror//;' grub-core/Makefile.am

#-----------------------------------------------------------------------
%build
%define _disable_ld_no_undefined 1
export GRUB_CONTRIB="$PWD/grub-extras"
export CONFIGURE_TOP="$PWD"

#(proyvind): debugedit will fail on some binaries if linked using gold
# https://savannah.gnu.org/bugs/?34539
# https://sourceware.org/bugzilla/show_bug.cgi?id=14187

#(proyvind): non-UEFI boot will fail with 'alloc magic broken' on x86_64
#            if built with clang
mkdir -p pc
pushd pc
%configure CC=gcc BUILD_CC=gcc TARGET_CC=gcc \
%if %{with talpo}
	CC=talpo  \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%endif
	CFLAGS="-O2 -fuse-ld=bfd" \
	TARGET_LDFLAGS="-static" \
	--with-platform=pc \
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

%make all html pdf
popd

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

%define grubefiarch %{_arch}-efi

#This line loads all the modules but makes the efi image unstable.
#./grub-mkimage -O %{grubefiarch} -p /EFI/openmandriva/%{name}-efi -o grub.efi -d grub-core `ls grub-core/*.mod | sed 's/.*\///g' | sed 's/\.mod//g' | xargs
#` In practice the grub.efi image is only required for the iso. when grub is installed it selects the modules it needs to boot the current install from the installed
#  OS.

#These lines produce a grub.efi suitable for an iso. Note the path in the -p option it points to the grub.cfg file on the iso.
../pc/grub-mkimage -O %{grubefiarch} -C xz -p /EFI/BOOT -o grub.efi -d grub-core linux multiboot multiboot2 all_video boot \
		btrfs cat chain configfile echo efifwsetup efinet ext2 fat font gfxmenu gfxterm gfxterm_menu gfxterm_background \
		gzio halt hfsplus iso9660 jpeg lvm mdraid09 mdraid1x minicmd normal part_apple part_msdos part_gpt password_pbkdf2 \
		png reboot regexp search search_fs_uuid search_fs_file search_label sleep test tftp video xfs mdraid09 mdraid1x lua loopback \
		squash4 syslinuxcfg
popd
%endif


#-----------------------------------------------------------------------
%install
######legacy
%makeinstall_std -C pc
%makeinstall_std -C pc/docs install-pdf install-html PACKAGE_TARNAME=%{name}

# (bor) grub.info is harcoded in sources
mv %{buildroot}%{_infodir}/grub.info %{buildroot}%{_infodir}/%{name}.info

# Script that makes part of grub.cfg persist across updates
install -m755 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/grub.d/90_persistent

# Ghost config file
install -d %{buildroot}/boot/%{name}
install -d %{buildroot}/boot/%{name}/locale
cp po/*.gmo %{buildroot}/boot/%{name}/locale/
touch %{buildroot}/boot/%{name}/grub.cfg
ln -s /boot/%{name}/grub.cfg %{buildroot}%{_sysconfdir}/%{name}.cfg

%if 0
# (proyvind): not sure what the purpose of this might've been, but it's no
#             longer made use of, so let's comment it out for now to avoid
#             time being spent on doing nothing untill it gets removed or made
#             use of again...
# Install ELF files modules and images were created from into
# the shadow root, where debuginfo generator will grab them from
find %{buildroot} -name '*.mod' -o -name '*.img' |
while read MODULE
do
        BASE=$(echo $MODULE |sed -r "s,.*/([^/]*)\.(mod|img),\1,")
        # Symbols from .img files are in .exec files, while .mod
        # modules store symbols in .elf. This is just because we
        # have both boot.img and boot.mod ...
        EXT=$(echo $MODULE |grep -q '.mod' && echo '.elf' || echo '.exec')
        TGT=$(echo $MODULE |sed "s,%{buildroot},.debugroot,")
#        install -m 755 -D $BASE$EXT $TGT
done
%endif

######EFI
%ifarch %{efi}
%makeinstall_std -C efi/grub-core

install -m755 efi/grub.efi -D %{buildroot}/boot/efi/EFI/openmandriva/grub.efi
# Ghost config file
touch %{buildroot}/boot/efi/EFI/openmandriva/grub.cfg
ln -s /boot/efi/EFI/openmandriva/grub.cfg %{buildroot}%{_sysconfdir}/%{name}-efi.cfg

%if 0
# (proyvind): not sure what the purpose of this might've been, but it's no
#             longer made use of, so let's comment it out for now to avoid
#             time being spent on doing nothing untill it gets removed or made
#             use of again...
# Install ELF files modules and images were created from into
# the shadow root, where debuginfo generator will grab them from
find %{buildroot} -name '*.mod' -o -name '*.img' |
while read MODULE
do
	BASE=$(echo $MODULE |sed -r "s,.*/([^/]*)\.(mod|img),\1,")
	# Symbols from .img files are in .exec files, while .mod
	# modules store symbols in .elf. This is just because we
	# have both boot.img and boot.mod ...
	EXT=$(echo $MODULE |grep -q '.mod' && echo '.elf' || echo '.exec')
	TGT=$(echo $MODULE |sed "s,%{buildroot},.debugroot,")
done
%endif
%endif

# Defaults
install -m755 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/default/grub
# (tpg) use default distro name
sed -e 's#TMP_DISTRO#%{distribution}#' -i %{buildroot}%{_sysconfdir}/default/grub

#Add more useful update-grub2 script
install -m755 %{SOURCE9} -D %{buildroot}%{_sbindir}

# Install filetriggers to update grub.cfg on kernel add or remove
install -d %{buildroot}%{_filetriggers_dir}
cat > %{buildroot}%{_filetriggers_dir}/%{name}.filter << EOF
^./boot/vmlinuz-
^./boot/grub2/themes/
EOF
cat > %{buildroot}%{_filetriggers_dir}/%{name}.script << EOF
#!/bin/sh
[ -e /boot/grub2/grub.cfg ] && %{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg
EOF
chmod 755 %{buildroot}%{_filetriggers_dir}/%{name}.script

install -d %{buildroot}/boot/%{name}/themes/


#bugfix: error message before loading of grub2 menu on boot
mkdir -p %{buildroot}%{_localedir}/en/LC_MESSAGES
ln %{buildroot}%{_localedir}/en@quot/LC_MESSAGES/grub.mo %{buildroot}%{_localedir}/en/LC_MESSAGES


%find_lang grub

#drop all zero-length file
#find %{buildroot} -size 0 -delete

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
        %{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg
    fi

# (tpg) run only on update
    if [ $1 -ge 2 ]; then
# (tpg) remove wrong line in boot options
	if [ -e %{_sysconfdir}/default/grub ]; then
	    if grep -q "init=/lib/systemd/systemd" %{_sysconfdir}/default/grub; then
		sed -i -e 's#init=/lib/systemd/systemd##g' %{_sysconfdir}/default/grub
	    fi

	    if grep -q "acpi_backlight=vendor" %{_sysconfdir}/default/grub; then
		sed -i -e 's#acpi_backlight=vendor#video.use_native_backlight=1#g' %{_sysconfdir}/default/grub
	    fi
# (tpg) disable audit messages
	    if ! grep -q "audit=0" %{_sysconfdir}/default/grub; then
    		sed -i -e 's#quiet#quiet audit=0 #' %{_sysconfdir}/default/grub
    	    fi
# (tpg) remove resume= as it is not needed with tuxonice
	    if ! grep -q "resume=" %{_sysconfdir}/default/grub; then
    		sed -i -e 's#resume=.*[ \t]##' %{_sysconfdir}/default/grub
    	    fi
# (tpg) regenerate grub2 at the end
	    update-grub2
	fi
    fi
fi

%preun
exec >/dev/null
if [ $1 = 0 ]; then
    # XXX Ugly
    rm -f /boot/%{name}/*.mod
    rm -f /boot/%{name}/*.img
    rm -f /boot/%{name}/*.lst
    rm -f /boot/%{name}/*.o
    rm -f /boot/%{name}/device.map
fi

#-----------------------------------------------------------------------
%files -f grub.lang
%doc NEWS README THANKS TODO
#%{libdir32}/%{name}
%{libdir32}/grub/*-%{platform}
#Files here are needed for install. Moved from efi package
%{libdir32}/grub/%{_arch}-efi/
#%{_sbindir}/%{name}-*
#%{_bindir}/%{name}-*
%{_sbindir}/update-grub2
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-mkrescue
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-mount
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-file
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-syslinux2cfg
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-sparc64-setup
%{_datadir}/grub
%exclude %{_datadir}/grub/themes/*
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%{_sysconfdir}/grub.d/README
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/%{name}.cfg
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/bash_completion.d/grub
%dir /boot/%{name}
%dir /boot/%{name}/locale
%dir /boot/%{name}/locale/*.gmo
%dir /boot/%{name}/themes
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/%{name}/grub.cfg
%{_infodir}/%{name}.info*
%{_infodir}/grub-dev.info*
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man8/%{name}-*.8*
# RPM filetriggers
%{_filetriggers_dir}/%{name}.*

%ifarch %{efi}
%attr(0755,root,root) %dir /boot/efi/EFI/openmandriva
%attr(0755,root,root) %ghost %config(noreplace) /boot/efi/EFI/openmandriva/grub.cfg

%files efi
# Files in this package are only required for the creation of iso's
# The install process creates all the files required to boot with grub via EFI
%attr(0755,root,root) /boot/efi/EFI/openmandriva/grub.efi
#%attr(0755,root,root) %ghost %config(noreplace) /boot/efi/EFI/openmandriva/grub.cfg

%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg

%endif

%files starfield-theme
%{_datadir}/grub/themes/starfield
