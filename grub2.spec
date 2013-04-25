%define libdir32 %{_exec_prefix}/lib
%define platform pc
%define efi 1
#%define		unifont		%(echo %{_datadir}/fonts/TTF/unifont/unifont-*.ttf)

%global efi %{ix86} x86_64
%global optflags %{optflags} -Os

%bcond_with talpo

Name:		grub2
Version:	2.00
Release:	20
Summary:	GNU GRUB is a Multiboot boot loader

Group:		System/Kernel and hardware
License:	GPLv3+
URL:		http://www.gnu.org/software/grub/
Source0:	http://ftp.gnu.org/pub/gnu/grub/grub-%{version}.tar.xz
Source1:	90_persistent
Source2:	grub2.default
Source3:	grub.melt
# www.4shared.com/archive/lFCl6wxL/grub_guidetar.html
Source4:	grub_guide.tar.gz
Source5:	DroidSansMonoLicense.txt
Source6:	DroidSansMono.ttf
Source7:	rosa-theme.tar.gz
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
Patch13:	grub2-remove-rosa-logo-from-theme.patch
Patch14:	grub-2.00-try-link-against-libncursesw-also.patch
Patch15:	grub-fix-texinfo-page.patch
# Fix parallel build
Patch16:	grub2-2.00-parallel-build.patch
# Fix autoreconf warnings
Patch17:	grub2-2.00-mga-fix_AM_PROG_MKDIR_P-configure.ac.patch

# Fedora patches
Patch20:	grub2-linuxefi.patch
Patch21:	grub2-cdpath.patch
Patch22:	grub2-use-linuxefi.patch
Patch23:	grub-2.00-dont-decrease-mmap-size.patch
Patch24:	grub-2.00-no-insmod-on-sb.patch
Patch25:	grub-2.00-efidisk-ahci-workaround.patch
Patch26:	grub-2.00-increase-the-ieee1275-device-path-buffer-size.patch
Patch27:	grub-2.00-Handle-escapes-in-labels.patch
Patch28:	grub-2.00-fix-http-crash.patch
Patch29:	grub-2.00-Issue-separate-DNS-queries-for-ipv4-and-ipv6.patch
Patch30:	grub-2.00-cas-reboot-support.patch
Patch31:	grub-2.00-for-ppc-include-all-modules-in-the-core-image.patch
Patch32:	add-vlan-tag-support.patch
Patch33:	follow-the-symbolic-link-ieee1275.patch
Patch34:	grub-2.00-add-X-option-to-printf-functions.patch
Patch35:	grub-2.00-dhcp-client-id-and-uuid-options-added.patch
Patch36:	grub-2.00-search-for-specific-config-file-for-netboot.patch
Patch37:	grub2-add-bootpath-device-to-the-list.patch
Patch38:	grub-2.00-add-GRUB-DISABLE-SUBMENU-option.patch
Patch39:	grub-2.00-support-bls-config.patch

# openSuSE patches
Patch100:	grub2-fix-locale-en.mo.gz-not-found-error-message.patch
Patch101:	grub2-fix-error-terminal-gfxterm-isn-t-found.patch

BuildRequires:	bison
BuildRequires:	flex
#BuildRequires:	fonts-ttf-unifont
Buildrequires:	distro-theme-Moondrake
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	glibc-static-devel
BuildRequires:	help2man
BuildRequires:	liblzo-devel
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:	autogen
%if %{with talpo}
BuildRequires:	talpo
%endif

Requires:	xorriso
Requires(post):	os-prober
Suggests:	%{name}-theme

Provides:	bootloader
Provides:	grub2bootloader = %{EVRD}

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
Provides:	grub2bootloader = %{EVRD}
Suggests:	%{name}-theme

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture. 

It support rich variety of kernel formats, file systems, computer 
architectures and hardware devices.  This subpackage provides support 
for EFI systems.
%endif

%package	moondrake-theme
Summary:	Provides a graphical theme with a custom Moondrake background for grub2
Group:		System/Kernel and hardware
Requires:	grub2bootloader = %{EVRD}
Provides:	%{name}-theme = %{EVRD}

%description	moondrake-theme
This package provides a custom Moondrake graphical theme.

%package	rosa-theme
Summary:	Provides a graphical theme with a custom ROSA background for grub2
Group:		System/Kernel and hardware
Requires:	grub2bootloader = %{EVRD}
Provides:	%{name}-theme = %{EVRD}

%description	rosa-theme
This package provides a custom ROSA graphical theme.

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
%prep
%setup -q -n grub-%{version} -a7 -a12
%apply_patches
cp %{SOURCE10} .

perl -pi -e 's/(\@image\{font_char_metrics,,,,)\.(png\})/$1$2/;'	\
	docs/grub-dev.texi

perl -pi -e "s|(^FONT_SOURCE=)|\$1%{SOURCE6}|;" configure configure.ac

sed -ri -e 's/-g"/"/g' -e "s/-Werror//g" configure.ac

perl -pi -e 's/-Werror//;' grub-core/Makefile.am
mkdir grub-extras
mv lua grub-extras
export GRUB_CONTRIB=./grub-extras
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
%configure                                              \
%if %{with talpo}
	CC=talpo                                        \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%else
	CFLAGS=""                                       \
%endif
	TARGET_LDFLAGS=-static                          \
	--with-platform=efi                             \
	--program-transform-name=s,grub,%{name}-efi,    \
	--libdir=%{libdir32}                            \
	--libexecdir=%{libdir32}                        \
	--with-grubdir=grub2                            \
	--disable-werror                                \
	--enable-device-mapper                          \
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
pushd pc
%configure                                              \
%if %{with talpo}
	CC=talpo                                        \
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE3} \
%else
	CFLAGS=""                                       \
%endif
	TARGET_LDFLAGS=-static                          \
	--with-platform=pc                              \
    %ifarch x86_64
	--enable-efiemu                                 \
    %endif
	--program-transform-name=s,grub,%{name},        \
	--libdir=%{libdir32}                            \
	--libexecdir=%{libdir32}                        \
	--with-grubdir=grub2                            \
	--disable-werror                                \
	--enable-device-mapper                          \
	--enable-grub-mkfont
%make all

make html pdf
popd

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

#Add more useful update-grub2 script
install -m755 %{SOURCE9} -D %{buildroot}%{_sbindir}

# Install filetriggers to update grub.cfg on kernel add or remove
install -d %{buildroot}%{_filetriggers_dir}
cat > %{buildroot}%{_filetriggers_dir}/%{name}.filter << EOF
^./boot/vmlinuz-
EOF
cat > %{buildroot}%{_filetriggers_dir}/%{name}.script << EOF
#!/bin/sh
%{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg
EOF
chmod 755 %{buildroot}%{_filetriggers_dir}/%{name}.script

install -d %{buildroot}/boot/%{name}/themes/moondrake
cp -a rosa %{buildroot}/boot/%{name}/themes/
ln %{buildroot}/boot/%{name}/themes/rosa/* %{buildroot}/boot/%{name}/themes/moondrake
rm %{buildroot}/boot/%{name}/themes/moondrake/background.png %{buildroot}/boot/%{name}/themes/moondrake/Logo_Rosa.png
cp %{_datadir}/gfxboot/themes/Moondrake/back.jpg %{buildroot}/boot/%{name}/themes/moondrake/background.jpg

#mv -f %{buildroot}/%{libdir32}/grub %{buildroot}/%{libdir32}/%{name}
#mv -f %{buildroot}/%{_datadir}/grub %{buildroot}/%{_datadir}/%{name}

%find_lang grub

#drop all zero-length file
#find %{buildroot} -size 0 -delete

%post
exec > /var/log/%{name}_post.log 2>&1
# Create device.map or reuse one from GRUB Legacy
[ -f /boot/grub/device.map ] && cp -u /boot/grub/device.map /boot/%{name}/device.map
# Do not install grub2 if running in a chroot
# http://stackoverflow.com/questions/75182/detecting-a-chroot-jail-from-within
if [ -z "$DURING_INSTALL" -a "$(stat -c %d:%i /)" = "$(stat -c %d:%i /proc/1/root/.)" ]; then
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
exec > /var/log/%{name}_preun.log 2>&1
if [ $1 = 0 ]; then
    # XXX Ugly
    rm -f /boot/%{name}/*.mod
    rm -f /boot/%{name}/*.img
    rm -f /boot/%{name}/*.lst
    rm -f /boot/%{name}/*.o
    rm -f /boot/%{name}/device.map
fi

%post moondrake-theme
if [ $1 -eq 1 ] ; then
sed 	-e 's#\(GRUB_THEME=\).*#\1"/boot/%{name}/themes/moondrake/theme.txt"#g' \
	-e 's#\(GRUB_BACKGROUND=\).*#\1"/boot/grub2/themes/moondrake/terminal_background.png"#g' \
	-i %{_sysconfdir}/default/grub
fi

%post rosa-theme
# Don't install if updating
if [ $1 -eq 1 ] ; then
sed 	-e 's#\(GRUB_THEME=\).*#\1"/boot/%{name}/themes/rosa/theme.txt"#g' \
	-e 's#\(GRUB_BACKGROUND=\).*#\1"/boot/grub2/themes/rosaa/terminal_background.png"#g' \
	-i %{_sysconfdir}/default/grub
fi

#-----------------------------------------------------------------------
%files -f grub.lang
%doc NEWS README THANKS TODO ChangeLog
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

%files moondrake-theme
/boot/%{name}/themes/moondrake

%files rosa-theme
/boot/%{name}/themes/rosa

%changelog
* Sat Apr  6 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.00-17
- Do not install grub2 in post if running in a chroot.

* Fri Dec 21 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.00-12
- when linking against ncurses, make sure to try libncursesw also (P14)
- use pkgconfig() deps for buildrequires
- add missing pkgconfig(fuse) buildrequire for grub2-mount to build
- fix merge with ROSA package
- cleanups

* Sat Sep 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.00-1
+ Revision: 817955
- add br on texinfo
- don't error out on gets()... (P1, from fedora)
- indent
- fix path to dejavu fonts (P0)
- filter out certain rpmlint errors
- set grubdir properly
- add lua support
- enable Linux device-mapper support
- build with bfd linker for now as using gold will break stuff
- new version

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Update grub2 theme test script to work in a current cooker system.

* Tue Jan 03 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.99-4
+ Revision: 750375
- Rework sample theme test script to work on a fresh svn checkout.
- Add documentation and script to test grub2 themes
- Add talpo build and melt config file for debug build (thanks to alissy)

* Thu Aug 25 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.99-3
+ Revision: 696543
- Add a very simple sample grub2 mandriva theme
- Build and install pdf and html documentation.

* Thu Jul 07 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.99-2
+ Revision: 689083
- build with xz support

* Thu Jun 02 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.99-1
+ Revision: 682534
- Cleanup to better match upstream, and update to latest upstream release

* Sat Oct 23 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 1.98-2mdv2011.0
+ Revision: 587770
- add menu entry "Chainload GRUB2" to default bootloader on first install
  create default grub.cfg on first install
- use filetriggers instead of standard triggers to update grub.cfg on
  kernel add/remove. Every kernel package has unique name in Mandriva
  and plain triggers do not support wildcards
- source2: update /etc/defaut/grub
  * set distributor to Mandriva
  * use splash=silent instead of "guiet rhgb" in GRUB_CMDLINE_LINUX_DEFAULT,
  not GRUB_CMDLINE_LINUX
  * do not generate rescue line by default, it is not done in grub1

* Mon Oct 11 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 1.98-1mdv2011.0
+ Revision: 584979
- buildrequires help2man
- buildrequires texinfo for makeinfo
- package info and man pages

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - new release: 1.98
      * partially sync with fedora
    - add missing buildrequires

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Jérôme Soyer <saispo@mandriva.org>
    - New upstream release

