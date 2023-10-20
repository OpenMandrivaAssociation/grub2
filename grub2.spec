%define libdir32 %{_exec_prefix}/lib
# (tpg) disable LTO as grub2 is not designed to benefit from it
%define _disable_lto 1

%ifarch %{ix86} %{x86_64}
%define platform pc
%endif

%ifarch armv7hnl
%define platform uboot
%endif

%ifarch aarch64 riscv64
%define platform efi
%endif

%define snapshot %{nil}
%define beta rc1

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
## WARNING! before updating snapshots grep local for
## 'boot/grub' in the source , including Makefiles*
## and compare to grub2-2.02-unity-mkrescue-use-grub2-dir.patch
## do _NOT_ update without doing that .. we just go lucky until now.
Version:	2.12
Release:	%{?beta:0.%{beta}.}1
Group:		System/Kernel and hardware
License:	GPLv3+
Url:		http://www.gnu.org/software/grub/
%if 0%{?beta:1}
Source0:	https://alpha.gnu.org/pub/pub/gnu/grub/grub-%{version}~%{beta}.tar.xz
%else
%if "%{snapshot}" == ""
Source0:	http://ftp.gnu.org/pub/gnu/grub/grub-%{version}%{?beta:-%{beta}}.tar.xz
%else
# git clone git://git.sv.gnu.org/grub.git
# git archive --format=tar --prefix grub-2.02-$(date +%Y%m%d)/ HEAD | xz -vf > grub-2.02-$(date +%Y%m%d).tar.xz
Source0:	grub-%{version}-%{snapshot}.tar.xz
%endif
%endif
Source1:	90_persistent
Source2:	grub.default
# www.4shared.com/archive/lFCl6wxL/grub_guidetar.html
Source4:	grub_guide.tar.gz
Source5:	DroidSansMonoLicense.txt
Source6:	DroidSansMono.ttf
Source9:	update-grub2
Source11:	grub2.rpmlintrc
# (tpg) source
# rm -rf grub-extras && git clone https://git.savannah.gnu.org/git/grub-extras.git && cd grub-extras
# git archive --prefix=grub-extras/ --format=tar HEAD | xz > ../grub-extras-$(date +%Y%m%d).tar.xz
Source12:	grub-extras-20231020.tar.xz
# documentation and simple test script for testing grub2 themes
Source13:	grub2-theme-test.sh
Source14:	30-uefi_firmware
Patch0:		grub2-locales.patch
Patch1:		grub2-00_header.patch
Patch2:		grub2-custom-color.patch
Patch3:		grub2-read-cfg.patch
Patch4:		grub2-symlink-is-garbage.patch
Patch5:		grub-2.04-workaround-llvm-bug-48528.patch
Patch6:		grub-2.06-enable-os-prober.patch
# (crazy) replaces:
# grub-2.00.Linux.remove.patch
# grub-2.00-add-recovery_option.patch
# grub2-2.02-add-support-for-kernel-install.patch
# fix-btrfs-GRUB_CMDLINE_LINUX_RECOVERY.patch ( https://issues.openmandriva.org/show_bug.cgi?id=2423 )
# Ok @bero .. ( also use this patch for OMV things touchting /grub.d/ and so on )
# In addition console boot support got added ( https://issues.openmandriva.org/show_bug.cgi?id=2402 )
Patch7:		omv-configuration.patch
Patch8:		grub-2.00-fix-dejavu-font.patch
Patch9:		grub2-2.00-class-via-os-prober.patch
Patch10:	grub-2.00-autoreconf-sucks.patch
Patch11:	0468-Don-t-write-messages-to-the-screen.patch
Patch12:	grub-2.02-beta2-custom-vendor-config.patch
#Patch13:	0001-Revert-Make-grub-install-check-for-errors-from-efibo.patch
Patch15:	grub-2.02-20180620-disable-docs.patch
# Without this, build fails on aarch64 w/ unresolved symbol abort
# while running grub-mkimage
Patch16:	grub-2.02-define-abort.patch
Patch17:	grub-2.04-grub-extras-lua-fix.patch

# (crazy) these are 2 BAD patches , FIXME after Lx4
# Patch7 prepares remove for that ( partially )
# Patches from Mageia
Patch100:	grub2-2.00-mga-dont_write_sparse_file_error_to_screen.patch
Patch101:	grub2-2.00-mga-dont_write_diskfilter_error_to_screen.patch

# Patches from SuSe

# Patches from Unity
Patch300:	grub2-2.02-unity-mkrescue-use-grub2-dir.patch

# Patches from upstream
# [Selected from running git format-patch grub-2.12-rc1 in master branch]
Patch1000: 0001-tests-util-grub-shell-Add-verbose-to-grub-mkrescue-w.patch
Patch1001: 0002-tests-util-grub-shell-Allow-setting-default-timeout-.patch
Patch1002: 0003-tests-util-grub-shell-Allow-setting-the-value-of-deb.patch
Patch1003: 0004-tests-util-grub-shell-luks-tester-Allow-GRUB_SHELL_L.patch
Patch1004: 0005-util-grub.d-25_bli.in-Fix-shebang-on-unmerged-usr.patch
Patch1005: 0006-docs-Add-missing-assumption.patch
Patch1006: 0007-configure-Fix-SDL2-typo-by-referencing-value.patch
Patch1007: 0008-util-grub-mount-Fix-memory-leak-in-fuse_getattr.patch
Patch1008: 0009-docs-Group-usage-of-user-space-utilities-into-single.patch
Patch1009: 0010-docs-Document-hexdump-command.patch
Patch1010: 0011-docs-A-note-to-cat-that-hexdump-should-be-used-for-b.patch
Patch1011: 0012-term-ns8250-spcr-Continue-processing-SPCR-table-even.patch
Patch1012: 0013-docs-Improve-initrd-documentation.patch
Patch1013: 0014-commands-videoinfo-Prevent-crash-when-run-while-vide.patch
Patch1014: 0015-fs-archelp-If-path-given-to-grub_archelp_dir-is-not-.patch
Patch1015: 0016-commands-ls-Send-correct-dirname-to-print-functions.patch
Patch1016: 0017-commands-ls-Print-if-unable-to-get-file-size.patch
Patch1017: 0018-tests-util-grub-shell-Convert-spaces-to-TABs.patch
Patch1018: 0019-tests-util-grub-shell-luks-tester-Do-not-remove-gene.patch
Patch1019: 0020-tests-util-grub-shell-Allow-explicitly-using-other-s.patch
Patch1020: 0021-tests-Add-serial_test.patch
Patch1021: 0022-kern-misc-Make-grub_vsnprintf-C99-POSIX-conformant.patch
Patch1022: 0023-disk-cryptodisk-Fix-missing-change-when-updating-to-.patch
Patch1023: 0024-tests-util-grub-shell-luks-tester-Allow-setting-time.patch
Patch1024: 0025-docs-Use-ref-instead-of-xref.patch
Patch1025: 0026-docs-Add-menu-to-prevent-older-makeinfo-versions-fro.patch
Patch1026: 0027-video-efi_gop-Require-shadow-if-PixelBltOnly.patch
Patch1027: 0028-ZFS-support-inode-type-embed-into-its-ID.patch
Patch1028: 0029-ZFS-Fix-invalid-memcmp.patch
Patch1029: 0030-ZFS-Don-t-iterate-over-null-objsets.patch
Patch1030: 0031-ZFS-Check-bonustype-in-addition-to-dnode-type.patch
Patch1031: 0032-loader-i386-linux-Prefer-entry-in-long-mode-when-boo.patch
Patch1032: 0033-loader-efi-linux-Implement-x86-mixed-mode-using-lega.patch
Patch1033: 0034-configure-Enable-fno-omit-frame-pointer-for-backtrac.patch
Patch1034: 0035-loongarch-Eliminate-cmodel-compilation-warnings.patch
Patch1035: 0036-templates-linux_xen-Fix-XSM-entries-generation.patch
Patch1036: 0037-lib-i386-relocator64-Fix-64-bit-FreeBSD-boot-on-BIOS.patch
Patch1037: 0038-util-grub-install-common-Minor-improvements-to-print.patch
Patch1038: 0039-util-grub-install-common-Print-usable-grub-mkimage-c.patch
Patch1039: 0040-kern-acpi-Skip-NULL-entries-in-RSDT-and-XSDT.patch
Patch1040: 0041-fs-ntfs-Fix-an-OOB-write-when-parsing-the-ATTRIBUTE_.patch
Patch1041: 0042-fs-ntfs-Fix-an-OOB-read-when-reading-data-from-the-r.patch
Patch1042: 0043-fs-ntfs-Fix-an-OOB-read-when-parsing-directory-entri.patch
Patch1043: 0044-fs-ntfs-Fix-an-OOB-read-when-parsing-bitmaps-for-ind.patch
Patch1044: 0045-fs-ntfs-Fix-an-OOB-read-when-parsing-a-volume-label.patch
Patch1045: 0046-fs-ntfs-Make-code-more-readable.patch
Patch1046: 0047-commands-efi-lsefisystab-Print-the-UEFI-specificatio.patch
Patch1047: 0048-term-serial-Ensure-proper-NULL-termination-after-gru.patch
Patch1048: 0049-disk-cryptodisk-Optimize-luks_script_get.patch
Patch1049: 0050-disk-cryptodisk-Add-support-for-LUKS2-in-proc-luks_s.patch
Patch1050: 0051-kern-efi-init-Disable-stack-smashing-protection-on-g.patch
Patch1051: 0052-tests-util-grub-shell-Enable-RNG-device-to-better-te.patch
Patch1052: 0053-kern-ieee1275-init-Restrict-high-memory-in-presence-.patch
Patch1053: 0054-fs-btrfs-Zero-file-data-not-backed-by-extents.patch
Patch1054: 0055-kern-i386-pc-init-Flush-cache-only-on-VIA-C3-and-ear.patch
Patch1055: 0056-disk-i386-pc-biosdisk-Read-up-to-63-sectors-in-LBA-m.patch
Patch1056: 0057-Revert-zfsinfo-Correct-a-check-for-error-allocating-.patch

# Additional OpenMandriva patches that need to be applied after upstream patches
Patch2000:	grub-2.06-add-mitigations-off-mode.patch

BuildRequires:	efi-srpm-macros
BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fontpackages-devel
BuildRequires:	unifont
BuildRequires:	fonts-ttf-dejavu
BuildRequires:	unifont-fonts
BuildRequires:	help2man
BuildRequires:	rsync
BuildRequires:	texinfo
BuildRequires:	texlive-tex.bin
BuildRequires:	glibc-static-devel
BuildRequires:	gettext-devel
BuildRequires:	lzo-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(fuse3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(ncursesw)
%ifarch %{arm} %{armx}
BuildRequires:	gcc
%endif
Provides:	bootloader
# (crazy) without gettext() function of grub2 is fakeed with printf ..
Requires:	gettext-base
Suggests:	os-prober
Suggests:	distro-theme-common
Suggests:	distro-theme-OpenMandriva-grub2
%ifarch %{ix86} %{x86_64}
Suggests:	microcode-intel
%endif
Conflicts:	grub2-tools < 2.02-1.beta2.6
%rename		grub2-tools
Suggests:	%{name}-doc >= %{EVRD}
Suggests:	%{name}-extra >= %{EVRD}
%ifarch %{efi}
# (tpg) this is needed for grub2-install
Requires:	efibootmgr
Requires:	efi-filesystem
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
Requires:	%{name} >= %{EVRD}
# (crazy) without gettext() function of grub2 is fakeed with printf ..
Requires:	gettext-base
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
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 2.02-8
Requires:	console-setup
Suggests:	xorriso
Suggests:	mtools

%description extra
Extra tools and files for GRUB.

%package starfield-theme
Summary:	An example theme for GRUB
Group:		System/Kernel and hardware
Requires:	%{name} >= %{EVRD}

%description starfield-theme
Example 'starfield' theme for GRUB.

%package doc
Summary:	Documentation for GRUB
Group:		System/Kernel and hardware
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 2.02-8

%description doc
Documentation for GRUB.

#-----------------------------------------------------------------------

%ifarch %{arm} %{armx}
%global optflags %{optflags} -fuse-ld=bfd
%global build_ldflags %{build_ldflags} -fuse-ld=bfd
%endif

%prep
%autosetup -p1 -n grub-%{version}%{?beta:~%{beta}}%{?snapshot:%{snapshot}} -a12

sed -i -e "s|^FONT_SOURCE=.*|FONT_SOURCE=%{SOURCE6}|g" configure configure.ac
sed -ri -e 's/-g"/"/g' -e "s/-Werror//g" configure.ac
sed -i -e 's/-Werror//g' grub-core/Makefile.am

# (tpg) remove not needed extra modules
rm -rf grub-extras/915resolution
rm -rf grub-extras/disabled
rm -rf grub-extras/ntldr-img
rm -rf grub-extras/lua

export GRUB_CONTRIB=./grub-extras
sed -i -e 's,-I m4,-I m4 --dont-fix,g' autogen.sh

# (tpg) pull latest translations
./linguas.sh

# Workaround for https://savannah.gnu.org/bugs/?57298.
# A number of strings were unintentionally excluded from the translation catalogue in the
# 2.04 release. Fortunately the omitted strings are just commented out in the .po files, so
# we can easily restore them. This workaround should be removed if/when upstream fix the bug.
cd po
for po_file in *.po ; do
    sed -i -e 's/^#~ //' -e 's/^#~|/#|/' $po_file
    msgfmt -o ${po_file%.po}.gmo $po_file
done
cd ..

#-----------------------------------------------------------------------
%build
%define _disable_ld_no_undefined 1
export GRUB_CONTRIB="$PWD/grub-extras"
export CONFIGURE_TOP="$PWD"

#(proyvind): debugedit will fail on some binaries if linked using gold
# https://savannah.gnu.org/bugs/?34539
# https://sourceware.org/bugzilla/show_bug.cgi?id=14187
./autogen.sh

%if "%{platform}" != ""
mkdir -p %{platform}
cd %{platform}
# Clang causes openmandriva theme to disappear. Only black theme on non UEFI/EFI platform. Switch back to gcc (angry)
%configure CC=gcc BUILD_CC=gcc TARGET_CC=gcc \
	CFLAGS="-Os -fuse-ld=bfd" \
	LDFLAGS="" \
	TARGET_LDFLAGS="-static" \
	--with-platform=%{platform} \
	--enable-nls \
%ifarch %{x86_64}
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
	--enable-grub-emu-sdl \
	--without-included-regex

%make_build ascii.h widthspec.h
%make_build all
cd -
%endif

%ifarch %{efi}
mkdir -p efi
cd efi
%ifarch %{arm} %{armx}
%configure CC=gcc BUILD_CC=gcc TARGET_CC=gcc \
%else
%configure BUILD_CC=%{__cc} TARGET_CC=%{__cc} \
%endif
	CFLAGS="-Os -fuse-ld=bfd" \
	LDFLAGS="" \
	TARGET_LDFLAGS="-static" \
	--with-platform=efi \
	--enable-nls \
	--program-transform-name=s,grub,%{name}-efi, \
	--libdir=%{libdir32} \
	--libexecdir=%{libdir32} \
	--with-grubdir=grub2 \
	--disable-werror \
	--enable-grub-mkfont \
	--enable-device-mapper \
	--enable-grub-emu-sdl \
	--without-included-regex

%make_build ascii.h widthspec.h
%make_build -C grub-core

%define grub_modules_default all_video boot btrfs cat gettext chain configfile cryptodisk echo efifwsetup efinet ext2 f2fs fat font gcry_rijndael gcry_rsa gcry_serpent gcry_sha256 gcry_twofish gcry_whirlpool gfxmenu gfxterm gfxterm_background gfxterm_menu gzio halt hfsplus iso9660 jpeg loadenv loopback linux lsefi luks lvm mdraid09 mdraid1x minicmd normal part_apple part_gpt part_msdos password_pbkdf2 probe png reboot regexp search search_fs_file search_fs_uuid search_label serial sleep squash4 syslinuxcfg test tftp video xfs zstd

%ifarch aarch64
%define grubefiarch arm64-efi
%define grub_modules %{grub_modules_default} efi_gop
%else
%define grubefiarch %{_arch}-efi
%define grub_modules multiboot multiboot2 %{grub_modules_default}
%endif

#This line loads all the modules but makes the efi image unstable.
#./grub-mkimage -O %{grubefiarch} -p /EFI/openmandriva/%{name}-efi -o grub.efi -d grub-core $(ls grub-core/*.mod | sed 's/.*\///g' | sed 's/\.mod//g' | xargs
#) In practice the grub.efi image is only required for the iso. when grub is installed it selects the modules it needs to boot the current install from the installed
#  OS.

#These lines produce a grub.efi suitable for an iso. Note the path in the -p option it points to the grub.cfg file on the iso.
../%{platform}/grub-mkimage -v -O %{grubefiarch} -C xz -p /EFI/BOOT -o grub.efi -d grub-core %{grub_modules}

# sign our EFI image
#%%pesign -s -i%%{buildroot}/%{efi_esp_dir}/grub.efi -o %{buildroot}/%{efi_esp_dir}/OMgrub.efi
cd -
%endif


#-----------------------------------------------------------------------
%install
######legacy
%if "%{platform}" != ""
%make_install -C %{platform}

# (crazy) fixme? why so?
# Script that makes part of grub.cfg persist across updates
install -m755 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/grub.d/90_persistent
install -m755 %{SOURCE14} -D %{buildroot}%{_sysconfdir}/grub.d/30_uefi_firmware

# Ghost config file
install -d %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
%endif

######EFI
%ifarch %{efi}
%make_install -C efi/grub-core

install -m755 efi/grub.efi -D %{buildroot}/%{efi_esp_dir}/grub.efi
#%%pesign -s -i %%{buildroot}/%{efi_esp_dir}/grub.efi -o %%{buildroot}/%{efi_esp_dir}/grub.efi
%endif

%if "%{platform}" == "efi"
cd %{buildroot}%{_bindir}
for i in grub2-efi-*; do
    GENERICNAME="$(printf "%s\n" $i |sed -e 's,-efi,,')"
    mv $i $GENERICNAME
done
cd -
%endif

# (crazy) all this is strange , figure bc we do the same from other package(s)
# Defaults
install -m755 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/default/grub
# (tpg) use default distro name
sed -e 's#TMP_DISTRO#%{distribution}#' -i %{buildroot}%{_sysconfdir}/default/grub

#Add more useful update-grub2 script
install -m755 %{SOURCE9} -D %{buildroot}%{_bindir}

install -d %{buildroot}/boot/%{name}/themes/

#bugfix: error message before loading of grub2 menu on boot
mkdir -p %{buildroot}%{_localedir}/en/LC_MESSAGES
cp -f %{buildroot}%{_localedir}/en@quot/LC_MESSAGES/grub.mo %{buildroot}%{_localedir}/en/LC_MESSAGES/grub.mo

# (tpg) remove *.modules and leave *.mod
# Allow stuff to fail because some modules may not have been built
# (e.g. no EFI)
find %{buildroot}%{libdir32}/grub/*-%{platform} -name "*.module" -delete || :
find %{buildroot}%{libdir32}/grub/%{_arch}-efi/ -name "*.module" -delete || :

rm -f %{buildroot}%{_bindir}/%{name}-sparc64-setup
rm -f %{buildroot}%{_bindir}/%{name}-ofpathname

%find_lang grub

%triggerin -- %{name} < %{EVRD}
# (tpg) run only on update
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
# (crazy) FIXME: this need patch , btrfs and f2fs
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
    %{_bindir}/update-grub2
fi


%transfiletriggerin -p <lua> -- /boot /boot/grub2/themes /etc/os-release /etc/grub.d /usr/sbin/os-prober
os.execute("%{_bindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg")

%transfiletriggerpostun -p <lua> -- /lib/modules /boot/grub2/themes
os.execute("%{_bindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg")

------------------------------------------------------------------------

%files  -f grub.lang
%{libdir32}/grub/*-%{platform}
%ifnarch %{aarch64}
#Files here are needed for install. Moved from efi package
%{libdir32}/grub/%{_arch}-efi/
%endif
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
%files efi
# Files in this package are only required for the creation of iso's
# The install process creates all the files required to boot with grub via EFI
%attr(0755,root,root) %{efi_esp_dir}/grub.efi
%{_bindir}/%{name}-render-label
%{_sbindir}/%{name}-macbless
%endif

%files starfield-theme
%{_datadir}/grub/themes/starfield

%files doc
%doc NEWS README THANKS TODO
#{_docdir}/%%{name}
#{_infodir}/%%{name}.info*
#{_infodir}/grub-dev.info*
