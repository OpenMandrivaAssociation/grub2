%define libdir32 %{_exec_prefix}/lib
%define platform pc
%define efi 1
#%define		unifont		%(echo %{_datadir}/fonts/TTF/unifont/unifont-*.ttf)

%global efi %{ix86} x86_64
%global optflags %{optflags} -Os

%bcond_with talpo

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
Version:	2.00
Release:	32
Group:		System/Kernel and hardware
License:	GPLv3+
Url:		http://www.gnu.org/software/grub/
Source0:	http://ftp.gnu.org/pub/gnu/grub/grub-%{version}.tar.xz
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
Source12:	grub-lua-rev24.tar.xz
# documentation and simple test script for testing grub2 themes
Source13:	mandriva-grub2-theme-test.sh

Patch0:		grub2-locales.patch
Patch1:		grub2-00_header.patch
Patch2:		grub2-custom-color.patch
Patch3:		grub2-move-terminal.patch
Patch4:		grub2-read-cfg.patch
Patch5:		grub2-symlink-is-garbage.patch
Patch6:		grub2-name-corrections.patch
Patch7:		grub2-10_linux.patch
Patch8:		grub2-theme-not_selected_item_box.patch
Patch9:		grub-2.00.Linux.remove.patch
Patch10:	grub2-mkfont-fix.patch
Patch11:	grub-2.00-fix-dejavu-font.patch
Patch12:	grub-2.00-ignore-gnulib-gets-stupidity.patch
Patch14:	grub-2.00-try-link-against-libncursesw-also.patch
Patch15:	grub-fix-texinfo-page.patch
Patch16:	grub2-2.00-class-via-os-prober.patch
Patch17:	grub-2.00-autoreconf-sucks.patch
Patch18:	0468-Don-t-write-messages-to-the-screen.patch
BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
#BuildRequires:	fonts-ttf-unifont
BuildRequires:	help2man
BuildRequires:	texinfo
BuildRequires:	texlive-latex
BuildRequires:	texlive-epsf
BuildRequires:	glibc-static-devel
BuildRequires:	liblzo-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(ncursesw)
%if %{with talpo}
BuildRequires:	talpo
%endif
Requires:	xorriso
Provides:	bootloader
Requires:	os-prober

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

#-----------------------------------------------------------------------

%prep
%setup -qn grub-%{version} -a12
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
./autogen.sh

tar -xf %{SOURCE8}
pushd po-update; sh ./update.sh; popd

#-----------------------------------------------------------------------
%build
export GRUB_CONTRIB="$PWD/grub-extras"
export CONFIGURE_TOP="$PWD"

#(proyvind): debugedit will fail on some binaries if linked using gold
mkdir -p bfd
ln -sf %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH

%ifarch %{efi}
mkdir -p efi
pushd efi
%configure \
%if %{with talpo}
	CC=talpo \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%else
	CFLAGS="-O2" \
%endif
	TARGET_LDFLAGS="-static" \
	--with-platform=efi \
	--program-transform-name=s,grub,%{name}-efi, \
	--libdir=%{libdir32} \
	--libexecdir=%{libdir32} \
	--with-grubdir=grub2 \
	--disable-werror \
	--enable-device-mapper \
	--enable-grub-mkfont

%make all

%ifarch %{ix86}
%define grubefiarch i386-efi
%else
%define grubefiarch %{_arch}-efi
%endif
./grub-mkimage -O %{grubefiarch} -p /EFI/rosa/%{name}-efi -o grub.efi -d grub-core part_gpt hfsplus fat \
        ext2 btrfs normal chain boot configfile linux appleldr minicmd \
        loadbios reboot halt search font gfxterm echo video efi_gop efi_uga
popd
%endif

mkdir -p pc
cd pc
%configure \
%if %{with talpo}
	CC=talpo  \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%else
	CFLAGS="-O2" \
%endif
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
	--enable-grub-mkfont

%make all

%make html pdf

#-----------------------------------------------------------------------
%install
%ifarch %{efi}
%makeinstall_std -C efi
mv %{buildroot}%{_sysconfdir}/bash_completion.d/grub %{buildroot}%{_sysconfdir}/bash_completion.d/grub-efi

install -m755 efi/grub.efi -D %{buildroot}/boot/efi/EFI/rosa/%{name}-efi/grub.efi
# Ghost config file
touch %{buildroot}/boot/efi/EFI/rosa/%{name}-efi/grub.cfg
ln -s ../boot/efi/EFI/rosa/%{name}-efi/grub.cfg %{buildroot}%{_sysconfdir}/%{name}-efi.cfg

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
%makeinstall_std -C pc
%makeinstall_std -C pc/docs install-pdf install-html PACKAGE_TARNAME=%{name}

# (bor) grub.info is harcoded in sources
mv %{buildroot}%{_infodir}/grub.info %{buildroot}%{_infodir}/%{name}.info

# Script that makes part of grub.cfg persist across updates
install -m755 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/grub.d/90_persistent

# Ghost config file
install -d %{buildroot}/boot/%{name}
install -d %{buildroot}/boot/%{name}/locale
touch %{buildroot}/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg %{buildroot}%{_sysconfdir}/%{name}.cfg

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
# Defaults
install -m755 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/default/grub
# (tpg) use default distro name
sed -i -e 's#TMP_DISTRO#%{distribution}#' %{buildroot}%{_sysconfdir}/default/grub

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

#mv -f %{buildroot}/%{libdir32}/grub %{buildroot}/%{libdir32}/%{name}
#mv -f %{buildroot}/%{_datadir}/grub %{buildroot}/%{_datadir}/%{name}

#bugfix: error message before loading of grub2 menu on boot
mkdir -p %{buildroot}/%{_datadir}/locale/en/LC_MESSAGES
cp %{buildroot}/%{_datadir}/locale/en@quot/LC_MESSAGES/grub.mo %{buildroot}/%{_datadir}/locale/en/LC_MESSAGES

%find_lang grub

#drop all zero-length file
#find %{buildroot} -size 0 -delete

# Workaround for non-identical binaries getting the same build-id
%__strip --strip-unneeded %buildroot%_bindir/grub2-efi-fstest \
	%buildroot%_bindir/grub2-efi-editenv \
	%buildroot%_bindir/grub2-efi-menulst2cfg \
	%buildroot%_bindir/grub2-efi-mkfont \
	%buildroot%_bindir/grub2-efi-mkimage \
	%buildroot%_bindir/grub2-efi-mklayout \
	%buildroot%_bindir/grub2-efi-mkpasswd-pbkdf2 \
	%buildroot%_bindir/grub2-efi-mkrelpath \
	%buildroot%_bindir/grub2-efi-mount \
	%buildroot%_bindir/grub2-efi-script-check \
	%buildroot%_bindir/grub2-fstest \
	%buildroot%_bindir/grub2-editenv \
	%buildroot%_bindir/grub2-menulst2cfg \
	%buildroot%_bindir/grub2-mkfont \
	%buildroot%_bindir/grub2-mkimage \
	%buildroot%_bindir/grub2-mklayout \
	%buildroot%_bindir/grub2-mkpasswd-pbkdf2 \
	%buildroot%_bindir/grub2-mkrelpath \
	%buildroot%_bindir/grub2-mount \
	%buildroot%_bindir/grub2-script-check \
	%buildroot%_sbindir/grub2-efi-ofpathname \
	%buildroot%_sbindir/grub2-efi-bios-setup \
	%buildroot%_sbindir/grub2-efi-probe \
	%buildroot%_sbindir/grub2-efi-sparc64-setup \
	%buildroot%_sbindir/grub2-bios-setup \
	%buildroot%_sbindir/grub2-ofpathname \
	%buildroot%_sbindir/grub2-probe \
	%buildroot%_sbindir/grub2-sparc64-setup



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
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-mknetdir
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-sparc64-setup
#%{_datadir}/%{name}
%{_datadir}/grub
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%{_sysconfdir}/grub.d/README
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/%{name}.cfg
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/bash_completion.d/grub
%dir /boot/%{name}
%dir /boot/%{name}/locale
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
%files efi
%attr(0755,root,root) %dir /boot/efi/EFI/rosa/grub2-efi
%attr(0755,root,root) /boot/efi/EFI/rosa/grub2-efi/grub.efi
%attr(0755,root,root) %ghost %config(noreplace) /boot/efi/EFI/rosa/grub2-efi/grub.cfg
%{_sysconfdir}/bash_completion.d/grub-efi
%{libdir32}/grub/%{_arch}-efi/
%{_sbindir}/%{name}-efi*
%{_bindir}/%{name}-efi*
#%{_datadir}/grub
#%{_sysconfdir}/grub.d
%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg

# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
#%config(noreplace) /boot/efi/EFI/rosa/%{name}-efi/grub.cfg
# RPM filetriggers
#%{_filetriggers_dir}/%{name}.*
%endif

