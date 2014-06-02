%define libdir32 %{_exec_prefix}/lib
%define platform pc
%define efi 1

%global efi %{ix86} x86_64
%global optflags %{optflags} -Os

%bcond_with	talpo
%bcond_with	uclibc

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
Version:	2.02
Release:	1.beta2.1
Group:		System/Kernel and hardware
License:	GPLv3+
Url:		http://www.gnu.org/software/grub/
Source0:	http://ftp.gnu.org/pub/gnu/grub/grub-2.02~beta2.tar.xz
Source1:	90_persistent
Source2:	grub.default
Source3:	grub.melt
# www.4shared.com/archive/lFCl6wxL/grub_guidetar.html
Source4:	grub_guide.tar.gz
Source8:	grub2-po-update.tar.gz
Source9:	update-grub2
Source10:	README.urpmi
Source11:	grub2.rpmlintrc
Source12:	grub-lua-rev30.tar.xz
# documentation and simple test script for testing grub2 themes
Source13:	mandriva-grub2-theme-test.sh
Source14:	ntldr-img-rev21.tar.xz
Source15:	gpxe-rev15.tar.xz
Source16:	linguas.sh

# fedora patches
Patch0001:	0001-fix-EFI-detection-on-Windows.patch
Patch0002:	0002-grub-core-kern-arm-cache_armv6.S-Remove-.arch-direct.patch
Patch0003:	0003-NEWS-First-draft-of-2.02-entry.patch
Patch0004:	0004-remove-unused-error.h-from-kern-emu-misc.c.patch
Patch0005:	0005-Don-t-abort-on-unavailable-coreboot-tables-if-not-ru.patch
Patch0006:	0006-NEWS-Add-few-missing-entries.-Correct-existing-ones.patch
Patch0007:	0007-strip-.eh_frame-section-from-arm64-efi-kernel.patch
Patch0008:	0008-use-grub-boot-aa64.efi-for-boot-images-on-AArch64.patch
Patch0009:	0009-fix-32-bit-compilation-on-MinGW-w64.patch
Patch0010:	0010-Change-grub-mkrescue-to-use-bootaa64.efi-too.patch
Patch0011:	0011-arm64-set-correct-length-of-device-path-end-entry.patch
Patch0012:	0012-Makefile.util.def-grub-macbless-Change-mansection-to.patch
Patch0013:	0013-add-part_apple-to-EFI-rescue-image-to-fix-missing-pr.patch
Patch0014:	0014-freebsd-hostdisk.c-is-only-ever-compiled-on-FreeBSD.patch
Patch0015:	0015-Prefer-more-portable-test-1-constructs.patch
Patch0016:	0016-NEWS-Add-few-missing-entries.patch
Patch0017:	0017-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
Patch0018:	0018-util-grub-mount.c-Extend-GCC-warning-workaround-to-g.patch
Patch0019:	0019-reintroduce-BUILD_LDFLAGS-for-the-cross-compile-case.patch
Patch0020:	0020-grub-core-term-terminfo.c-Recognize-keys-F1-F12.patch
Patch0021:	0021-Fix-ChangeLog-date.patch
Patch0022:	0022-Use-_W64-to-detect-MinGW-W64-32-instead-of-_FILE_OFF.patch
Patch0023:	0023-add-BUILD_EXEEXT-support-to-fix-make-clean-on-Window.patch
Patch0024:	0024-fix-include-loop-on-MinGW-due-to-libintl.h-pulling-s.patch
Patch0025:	0025-grub-core-commands-macbless.c-Rename-FILE-and-DIR-to.patch
Patch0026:	0026-Makefile.util.def-Link-grub-ofpathname-with-zfs-libs.patch
Patch0027:	0027-Makefile.am-default_payload.elf-Add-modules.patch
Patch0028:	0028-fix-removal-of-cpu-machine-links-on-mingw-msys.patch
Patch0029:	0029-grub-core-normal-main.c-read_config_file-Buffer-conf.patch
Patch0030:	0030-util-grub-install.c-Fix-a-typo.patch
Patch0031:	0031-use-MODULE_FILES-for-genemuinit-instead-of-MOD_FILES.patch
Patch0032:	0032-Ignore-EPERM-when-modifying-kern.geom.debugflags.patch
Patch0033:	0033-change-stop-condition-to-avoid-infinite-loops.patch
Patch0034:	0034-increase-network-try-interval-gradually.patch
Patch0035:	0035-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch
Patch0036:	0036-Show-detected-path-to-DejaVuSans-in-configure-summar.patch
Patch0037:	0037-add-GRUB_WINDOWS_EXTRA_DIST-to-allow-shipping-runtim.patch
Patch0038:	0038-util-grub-install.c-write_to_disk-Add-an-info-messag.patch
Patch0039:	0039-util-grub-install.c-List-available-targets.patch
Patch0040:	0040-Fix-several-translatable-strings.patch
Patch0041:	0041-do-not-set-default-prefix-in-grub-mkimage.patch
Patch0042:	0042-fix-Mingw-W64-32-cross-compile-failure-due-to-printf.patch
Patch0043:	0043-grub-core-term-serial.c-grub_serial_register-Fix-inv.patch
Patch0044:	0044-grub-install-support-for-partitioned-partx-loop-devi.patch
Patch0045:	0045-grub-core-term-at_keyboard.c-Tolerate-missing-keyboa.patch
Patch0046:	0046-grub-core-disk-ahci.c-Do-not-enable-I-O-decoding-and.patch
Patch0047:	0047-grub-core-disk-ahci.c-Allocate-and-clean-space-for-a.patch
Patch0048:	0048-grub-core-disk-ahci.c-Add-safety-cleanups.patch
Patch0049:	0049-grub-core-disk-ahci.c-Properly-handle-transactions-w.patch
Patch0050:	0050-grub-core-disk-ahci.c-Increase-timeout.-Some-SSDs-ta.patch
Patch0051:	0051-util-grub-mkfont.c-Build-fix-for-argp.h-with-older-g.patch
Patch0052:	0052-util-grub-mkrescue.c-Build-fix-for-argp.h-with-older.patch
Patch0053:	0053-add-grub_env_set_net_property-function.patch
Patch0054:	0054-add-bootpath-parser-for-open-firmware.patch
Patch0055:	0055-grub-core-disk-ahci.c-Ignore-NPORTS-field-and-rely-o.patch
Patch0056:	0056-grub-core-kern-i386-coreboot-mmap.c-Filter-out-0xa00.patch
Patch0057:	0057-grub-core-loader-i386-multiboot_mbi.c-grub_multiboot.patch
Patch0058:	0058-grub-core-mmap-i386-uppermem.c-lower_hook-COREBOOT-I.patch
Patch0059:	0059-grub-core-kern-i386-pc-mmap.c-Fallback-to-EISA-memor.patch
Patch0060:	0060-include-grub-i386-openbsd_bootarg.h-Add-addr-and-fre.patch
Patch0061:	0061-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0062:	0062-Add-fw_path-variable-revised.patch
Patch0063:	0063-Add-support-for-linuxefi.patch
Patch0064:	0064-Use-linuxefi-and-initrdefi-where-appropriate.patch
Patch0065:	0065-Don-t-allow-insmod-when-secure-boot-is-enabled.patch
Patch0066:	0066-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0067:	0067-Fix-crash-on-http.patch
Patch0068:	0068-IBM-client-architecture-CAS-reboot-support.patch
Patch0069:	0069-Add-vlan-tag-support.patch
Patch0070:	0070-Add-X-option-to-printf-functions.patch
Patch0071:	0071-DHCP-client-ID-and-UUID-options-added.patch
Patch0072:	0072-Search-for-specific-config-file-for-netboot.patch
Patch0073:	0073-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0074:	0074-Move-bash-completion-script-922997.patch
Patch0075:	0075-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0076:	0076-Don-t-write-messages-to-the-screen.patch
Patch0077:	0077-Don-t-print-GNU-GRUB-header.patch
Patch0078:	0078-Don-t-add-to-highlighted-row.patch
Patch0079:	0079-Don-t-add-to-highlighted-row.patch
Patch0080:	0080-Message-string-cleanups.patch
Patch0081:	0081-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0082:	0082-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0083:	0083-Indent-menu-entries.patch
Patch0084:	0084-Fix-margins.patch
Patch0085:	0085-Add-support-for-UEFI-operating-systems-returned-by-o.patch
Patch0086:	0086-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0087:	0087-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch
Patch0088:	0088-Use-linux16-when-appropriate-880840.patch
Patch0089:	0089-Enable-pager-by-default.-985860.patch
Patch0090:	0090-F10-doesn-t-work-on-serial-so-don-t-tell-the-user-to.patch
Patch0091:	0091-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0092:	0092-Don-t-draw-a-border-around-the-menu.patch
Patch0093:	0093-Use-the-standard-margin-for-the-timeout-string.patch
Patch0094:	0094-Fix-grub_script_execute_sourcecode-usage-on-ppc.patch
Patch0095:	0095-Add-.eh_frame-to-list-of-relocations-stripped.patch
Patch0096:	0096-Make-10_linux-work-with-our-changes-for-linux16-and-.patch
Patch0097:	0097-Don-t-print-during-fdt-loading-method.patch
Patch0098:	0098-Honor-a-symlink-when-generating-configuration-by-gru.patch
Patch0099:	0099-Don-t-require-a-password-to-boot-entries-generated-b.patch
Patch0100:	0100-Don-t-emit-Booting-.-message.patch
Patch0101:	0101-Make-CTRL-and-ALT-keys-work-as-expected-on-EFI-syste.patch
Patch0102:	0102-May-as-well-try-it.patch
Patch0103:	0103-use-fw_path-prefix-when-fallback-searching-for-grub-.patch
Patch0104:	0104-Try-mac-guid-etc-before-grub.cfg-on-tftp-config-file.patch
Patch0105:	0105-trim-arp-packets-with-abnormal-size.patch
Patch0106:	0106-Fix-convert-function-to-support-NVMe-devices.patch
Patch0107:	0107-Fix-bad-test-on-GRUB_DISABLE_SUBMENU.patch
Patch0108:	0108-Switch-to-use-APM-Mustang-device-tree-for-hardware-t.patch
Patch0109:	0109-Use-the-default-device-tree-from-the-grub-default-fi.patch
Patch0110:	0110-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
Patch0111:	0111-Reduce-timer-event-frequency-by-10.patch
Patch0112:	0112-always-return-error-to-UEFI.patch

# our patches
Patch1000:	grub2-locales.patch
Patch1001:	grub2-00_header.patch
Patch1002:	grub2-custom-color.patch
Patch1004:	grub2-read-cfg.patch
Patch1005:	grub2-symlink-is-garbage.patch
#Patch1007:	grub2-10_linux.patch
Patch1011:	grub-2.02~beta2-fix-dejavu-font.patch
Patch1019:	grub-2.00-dont-print-stuff-while-grub-is-loading.patch
Patch1020:	grub-2.02~beta2-add-recovery_option.patch
Patch1021:      grub-2.02~beta2-custom-vendor-config.patch

# openSuSE patches
Patch1101:	grub2-fix-error-terminal-gfxterm-isn-t-found.patch
Patch1105:	grub2-iterate-and-hook-for-extended-partition.patch
Patch1109:	grub2-fix-menu-in-xen-host-server.patch
Patch1111:	grub2-secureboot-chainloader.patch
Patch1112:	grub2-pass-correct-root-for-nfsroot.patch
Patch1113:	grub2-secureboot-use-linuxefi-on-uefi-in-os-prober.patch
Patch1115:	30_os-prober_UEFI_support.patch	
Patch1116:	grub2-2.02~beta2-class-via-os-prober.patch
Patch1117:	grub-2.00-autoreconf-sucks.patch

BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fontpackages-devel
BuildRequires:	unifont
BuildRequires:	help2man
BuildRequires:	rsync
BuildRequires:	texinfo
BuildRequires:	texlive-latex
BuildRequires:	texlive-epsf
BuildRequires:	texlive-kpathsea.bin
BuildRequires:	texlive
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
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif
BuildRequires:	unifont-fonts
Requires:	xorriso
Requires(post):	os-prober
Requires:	%{name}-tools = %{EVRD}
Suggests:	%{name}-theme

Provides:	bootloader

%description
GNU GRUB is a Multiboot boot loader. It was derived from GRUB, the
GRand Unified Bootloader, which was originally designed and implemented
by Erich Stefan Boleyn.

Briefly, a boot loader is the first software program that runs when a
computer starts. It is responsible for loading and transferring control
to the operating system kernel software (such as the Hurd or Linux).
The kernel, in turn, initializes the rest of the operating system (e.g. GNU).

%ifarch %{efi}
%package	efi
Summary:	GRUB for EFI systems
Group:		System/Kernel and hardware
Requires:	%{name}-tools = %{EVRD}
Suggests:	%{name}-theme

%description	efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture. 

It support rich variety of kernel formats, file systems, computer 
architectures and hardware devices.  This subpackage provides support 
for EFI systems.
%endif

%package	tools
Summary:	Support tools for GRUB
Group:		System/Kernel and hardware
Requires:	gettext os-prober which file
Conflicts:	%{name} < 2.00-24
Conflicts:	%{name}-efi < 2.00-24

%description	tools
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich variety of kernel
formats, file systems, computer architectures and hardware devices.

This subpackage provides tools for support of all platforms.

%package	starfield-theme
Summary:	An example theme for GRUB
Group:		System/Kernel and hardware
Requires:	%{name}-tools = %{EVRD}
Conflicts:	%{name} < 2.00-24

%description	starfield-theme
Example 'starfield' theme for GRUB.

%prep
%setup -qn grub-2.02~beta2 -a12 -a14 -a15
#  needs to be fixed..
%apply_patches

#{lua: for i, p in ipairs(patches) do     print("patch -p1 -i ".. rpm.expand(p .. " --fuzz=%{_default_patch_fuzz} %{_default_patch_flags} -b --suffix ")..string.format(".%04d~",i) .. "\n") end}

cp %{SOURCE10} .

perl -pi -e 's/(\@image\{font_char_metrics,,,,)\.(png\})/$1$2/;' \
	docs/grub-dev.texi

perl -pi -e "s|(^FONT_SOURCE=)|\$1%{_fontbasedir}/X11/misc/unifont.pcf.gz|;" configure configure.ac

sed -ri -e 's/-g"/"/g' -e "s/-Werror//g" configure.ac

perl -pi -e 's/-Werror//;' grub-core/Makefile.am
mkdir grub-extras
mv gpxe lua ntldr-img grub-extras
export GRUB_CONTRIB="$PWD/grub-extras"
cp %{SOURCE16} .
sh linguas.sh
autoupdate
rm m4/iconv.m4
aclocal --force -Im4 -I/usr/share/aclocal --install
./autogen.sh

tar -xf %{SOURCE8}
pushd po-update; sh ./update.sh; popd
xz -v --text ChangeLog

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
	CFLAGS="-Os" \
%if %{with uclibc}
	TARGET_CC="%{uclibc_cc}" \
	TARGET_CFLAGS="%{uclibc_cflags}" \
%endif
%endif
	TARGET_LDFLAGS="-static" \
	--with-platform=efi \
	--program-transform-name=s,grub,%{name}, \
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
	CFLAGS="-Os" \
%if %{with uclibc}
	TARGET_CC="%{uclibc_cc}" \
	TARGET_CFLAGS="%{uclibc_cflags}" \
%endif
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

%make html

#-----------------------------------------------------------------------
%install
%ifarch %{efi}
%makeinstall_std -C efi

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
%makeinstall_std -C pc/docs install-html PACKAGE_TARNAME=%{name}

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
^./boot/grub2/themes/
EOF
cat > %{buildroot}%{_filetriggers_dir}/%{name}.script << EOF
#!/bin/sh
[ -e /boot/grub2/grub.cfg ] && %{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg
EOF
chmod 755 %{buildroot}%{_filetriggers_dir}/%{name}.script

install -d %{buildroot}/boot/%{name}/themes

#mv -f %{buildroot}/%{libdir32}/grub %{buildroot}/%{libdir32}/%{name}
#mv -f %{buildroot}/%{_datadir}/grub %{buildroot}/%{_datadir}/%{name}

#bugfix: error message before loading of grub2 menu on boot
mkdir -p %{buildroot}/%{_datadir}/locale/en/LC_MESSAGES
cp %{buildroot}/%{_datadir}/locale/en@quot/LC_MESSAGES/grub.mo %{buildroot}/%{_datadir}/locale/en/LC_MESSAGES

%find_lang grub

#drop all zero-length file
#find %{buildroot} -size 0 -delete

%post
exec > /var/log/%{name}_post.log 2>&1
# Create device.map or reuse one from GRUB Legacy
[ -f /boot/grub/device.map ] && cp -u /boot/grub/device.map /boot/%{name}/device.map
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
# (tpg) remove wrong line in boot options
    if [ -e /etc/default/grub ]; then
	if grep -q "init=/lib/systemd/systemd" /etc/default/grub; then
	    sed -i -e 's#init=/lib/systemd/systemd##g' /etc/default/grub
	fi
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

#-----------------------------------------------------------------------
%files
%doc NEWS README THANKS TODO ChangeLog.xz
#%{libdir32}/%{name}
%{libdir32}/grub/*-%{platform}
%{_sysconfdir}/%{name}.cfg
%dir /boot/%{name}
%dir /boot/%{name}/locale
%dir /boot/%{name}/themes
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/%{name}/grub.cfg
# RPM filetriggers
%{_filetriggers_dir}/%{name}.*

%ifarch %{efi}
%files efi
%attr(0755,root,root) %dir /boot/efi/EFI/rosa/grub2-efi
%attr(0755,root,root) /boot/efi/EFI/rosa/grub2-efi/grub.efi
%attr(0755,root,root) %ghost %config(noreplace) /boot/efi/EFI/rosa/grub2-efi/grub.cfg
%{libdir32}/grub/%{_arch}-efi/
%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg

# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
#%config(noreplace) /boot/efi/EFI/rosa/%{name}-efi/grub.cfg
# RPM filetriggers
#%{_filetriggers_dir}/%{name}.*
%endif

%files tools -f grub.lang
%dir %{libdir32}/grub/
%dir %{_datadir}/grub/
%{_datadir}/grub/*
#%exclude %{_datadir}/grub/themes/*
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-sparc64-setup
%{_sbindir}/update-grub2
%{_bindir}/%{name}-file
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%{_bindir}/%{name}-mount
%{_bindir}/%{name}-ntldr-img
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-syslinux2cfg
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%endif
%{_bindir}/%{name}-script-check
%{_datadir}/bash-completion/completions/grub
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/grub
%dir /boot/%{name}
%dir /boot/%{name}/themes/
#%dir /boot/%{name}/themes/system
#%exclude /boot/%{name}/themes/system/*
#%exclude %{_datadir}/grub/themes/
%{_infodir}/grub*.info*
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man8/%{name}-*.8*
