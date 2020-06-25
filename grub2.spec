%define libdir32 %{_exec_prefix}/lib

%ifarch %{ix86} %{x86_64}
%define platform pc
%endif

%ifarch armv7hnl
%define platform uboot
%endif

%ifarch aarch64 riscv64
%define platform efi
%endif

%define debug_package %{nil}
%define snapshot %{nil}

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
## WARNING! before updating snapshots grep local for
## 'boot/grub' in the source , including Makefiles*
## and compare to grub2-2.02-unity-mkrescue-use-grub2-dir.patch
## do _NOT_ update without doing that .. we just go lucky until now.
Version:	2.04
Release:	6
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
# www.4shared.com/archive/lFCl6wxL/grub_guidetar.html
Source4:	grub_guide.tar.gz
Source5:	DroidSansMonoLicense.txt
Source6:	DroidSansMono.ttf
Source9:	update-grub2
Source11:	grub2.rpmlintrc
# (tpg) source
# rm -rf grub-extras && git clone https://git.savannah.gnu.org/git/grub-extras.git && cd grub-extras
# git archive --prefix=grub-extras/ --format=tar HEAD | xz > ../grub-extras-$(date +%Y%m%d).tar.xz
Source12:	grub-extras-20191024.tar.xz
# documentation and simple test script for testing grub2 themes
Source13:	grub2-theme-test.sh
Source14:	30-uefi_firmware
Source20:	bootstrap
Source21:	bootstrap.conf


# Fedora patches, some are disabled as we do not need them

Patch0001:	0001-Add-support-for-Linux-EFI-stub-loading.patch
Patch0002:	0002-Rework-linux-command.patch
Patch0003:	0003-Rework-linux16-command.patch
Patch0004:	0004-Add-secureboot-support-on-efi-chainloader.patch
Patch0005:	0005-Make-any-of-the-loaders-that-link-in-efi-mode-honor-.patch
Patch0006:	0006-Handle-multi-arch-64-on-32-boot-in-linuxefi-loader.patch
#Patch0007:	0007-re-write-.gitignore.patch
Patch0008:	0008-IBM-client-architecture-CAS-reboot-support.patch
Patch0009:	0009-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0010:	0010-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0011:	0011-Honor-a-symlink-when-generating-configuration-by-gru.patch
Patch0012:	0012-Move-bash-completion-script-922997.patch
Patch0013:	0013-Update-to-minilzo-2.08.patch
Patch0014:	0014-Allow-fallback-to-include-entries-by-title-not-just-.patch
Patch0015:	0015-Add-GRUB_DISABLE_UUID.patch
Patch0016:	0016-Make-exit-take-a-return-code.patch
Patch0017:	0017-Mark-po-exclude.pot-as-binary-so-git-won-t-try-to-di.patch
Patch0018:	0018-Make-efi-machines-load-an-env-block-from-a-variable.patch
Patch0019:	0019-DHCP-client-ID-and-UUID-options-added.patch
Patch0020:	0020-Fix-bad-test-on-GRUB_DISABLE_SUBMENU.patch
Patch0021:	0021-Add-support-for-UEFI-operating-systems-returned-by-o.patch
Patch0022:	0022-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0023:	0023-Add-fw_path-variable-revised.patch
Patch0024:	0024-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0025:	0025-Add-X-option-to-printf-functions.patch
Patch0026:	0026-Search-for-specific-config-file-for-netboot.patch
Patch0027:	0027-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0028:	0028-Add-devicetree-loading.patch
Patch0029:	0029-Don-t-write-messages-to-the-screen.patch
Patch0030:	0030-Don-t-print-GNU-GRUB-header.patch
Patch0031:	0031-Don-t-add-to-highlighted-row.patch
Patch0032:	0032-Message-string-cleanups.patch
Patch0033:	0033-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0034:	0034-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0035:	0035-Indent-menu-entries.patch
Patch0036:	0036-Fix-margins.patch
Patch0037:	0037-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch
Patch0038:	0038-Enable-pager-by-default.-985860.patch
Patch0039:	0039-F10-doesn-t-work-on-serial-so-don-t-tell-the-user-to.patch
Patch0040:	0040-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0041:	0041-Don-t-draw-a-border-around-the-menu.patch
Patch0042:	0042-Use-the-standard-margin-for-the-timeout-string.patch
Patch0043:	0043-Add-.eh_frame-to-list-of-relocations-stripped.patch
Patch0044:	0044-Don-t-munge-raw-spaces-when-we-re-doing-our-cmdline-.patch
Patch0045:	0045-Don-t-require-a-password-to-boot-entries-generated-b.patch
Patch0046:	0046-Don-t-emit-Booting-.-message.patch
Patch0047:	0047-Replace-a-lot-of-man-pages-with-slightly-nicer-ones.patch
Patch0048:	0048-use-fw_path-prefix-when-fallback-searching-for-grub-.patch
Patch0049:	0049-Try-mac-guid-etc-before-grub.cfg-on-tftp-config-file.patch
Patch0050:	0050-Fix-convert-function-to-support-NVMe-devices.patch
Patch0051:	0051-Add-grub_util_readlink.patch
Patch0052:	0052-Make-editenv-chase-symlinks-including-those-across-d.patch
Patch0053:	0053-Generate-OS-and-CLASS-in-10_linux-from-etc-os-releas.patch
Patch0054:	0054-Minimize-the-sort-ordering-for-.debug-and-rescue-ker.patch
Patch0055:	0055-Try-prefix-if-fw_path-doesn-t-work.patch
Patch0056:	0056-Update-info-with-grub.cfg-netboot-selection-order-11.patch
Patch0057:	0057-Use-Distribution-Package-Sort-for-grub2-mkconfig-112.patch
Patch0058:	0058-Handle-rssd-storage-devices.patch
Patch0059:	0059-Make-grub2-mkconfig-construct-titles-that-look-like-.patch
Patch0060:	0060-Add-friendly-grub2-password-config-tool-985962.patch
Patch0061:	0061-tcp-add-window-scaling-support.patch
Patch0062:	0062-Fix-security-issue-when-reading-username-and-passwor.patch
Patch0063:	0063-Add-a-url-parser.patch
Patch0064:	0064-efinet-and-bootp-add-support-for-dhcpv6.patch
Patch0065:	0065-Add-grub-get-kernel-settings-and-use-it-in-10_linux.patch
Patch0066:	0066-Normalize-slashes-in-tftp-paths.patch
Patch0067:	0067-bz1374141-fix-incorrect-mask-for-ppc64.patch
Patch0068:	0068-Make-grub_fatal-also-backtrace.patch
Patch0069:	0069-Fix-up-some-man-pages-rpmdiff-noticed.patch
Patch0070:	0070-arm64-make-sure-fdt-has-address-cells-and-size-cells.patch
Patch0071:	0071-Make-our-info-pages-say-grub2-where-appropriate.patch
Patch0072:	0072-print-more-debug-info-in-our-module-loader.patch
Patch0073:	0073-macos-just-build-chainloader-entries-don-t-try-any-x.patch
Patch0074:	0074-grub2-btrfs-Add-ability-to-boot-from-subvolumes.patch
Patch0075:	0075-export-btrfs_subvol-and-btrfs_subvolid.patch
Patch0076:	0076-grub2-btrfs-03-follow_default.patch
Patch0077:	0077-grub2-btrfs-04-grub2-install.patch
Patch0078:	0078-grub2-btrfs-05-grub2-mkconfig.patch
Patch0079:	0079-grub2-btrfs-06-subvol-mount.patch
Patch0080:	0080-Fallback-to-old-subvol-name-scheme-to-support-old-sn.patch
Patch0081:	0081-Grub-not-working-correctly-with-btrfs-snapshots-bsc-.patch
Patch0082:	0082-Add-grub_efi_allocate_pool-and-grub_efi_free_pool-wr.patch
Patch0083:	0083-Use-grub_efi_.-memory-helpers-where-reasonable.patch
Patch0084:	0084-Add-PRIxGRUB_EFI_STATUS-and-use-it.patch
Patch0085:	0085-Don-t-use-dynamic-sized-arrays-since-we-don-t-build-.patch
Patch0086:	0086-don-t-ignore-const.patch
Patch0087:	0087-don-t-use-int-for-efi-status.patch
Patch0088:	0088-make-GRUB_MOD_INIT-declare-its-function-prototypes.patch
Patch0089:	0089-editenv-handle-relative-symlinks.patch
Patch0090:	0090-Make-libgrub.pp-depend-on-config-util.h.patch
Patch0091:	0091-Don-t-guess-boot-efi-as-HFS-on-ppc-machines-in-grub-.patch
Patch0092:	0092-20_linux_xen-load-xen-or-multiboot-2-modules-as-need.patch
Patch0093:	0093-Make-pmtimer-tsc-calibration-not-take-51-seconds-to-.patch
Patch0094:	0094-align-struct-efi_variable-better.patch
###Patch0095:	0095-Add-BLS-support-to-grub-mkconfig.patch
Patch0096:	0096-Don-t-attempt-to-backtrace-on-grub_abort-for-grub-em.patch
Patch0097:	0097-Add-linux-and-initrd-commands-for-grub-emu.patch
Patch0098:	0098-Add-grub2-switch-to-blscfg.patch
Patch0099:	0099-Add-grub_debug_enabled.patch
Patch0100:	0100-make-better-backtraces.patch
Patch0101:	0101-normal-don-t-draw-our-startup-message-if-debug-is-se.patch
Patch0102:	0102-Work-around-some-minor-include-path-weirdnesses.patch
Patch0103:	0103-Make-it-possible-to-enabled-build-id-sha1.patch
Patch0104:	0104-Add-grub_qdprintf-grub_dprintf-without-the-file-line.patch
Patch0105:	0105-Make-a-gdb-dprintf-that-tells-us-load-addresses.patch
Patch0106:	0106-Fixup-for-newer-compiler.patch
Patch0107:	0107-Don-t-attempt-to-export-the-start-and-_start-symbols.patch
Patch0108:	0108-Fixup-for-newer-compiler.patch
Patch0109:	0109-Add-support-for-non-Ethernet-network-cards.patch
Patch0110:	0110-misc-fix-invalid-character-recongition-in-strto-l.patch
Patch0111:	0111-net-read-bracketed-ipv6-addrs-and-port-numbers.patch
Patch0112:	0112-bootp-New-net_bootp6-command.patch
Patch0113:	0113-efinet-UEFI-IPv6-PXE-support.patch
Patch0114:	0114-grub.texi-Add-net_bootp6-doument.patch
Patch0115:	0115-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
Patch0116:	0116-efinet-Setting-network-from-UEFI-device-path.patch
Patch0117:	0117-efinet-Setting-DNS-server-from-UEFI-protocol.patch
Patch0118:	0118-Fix-one-more-coverity-complaint.patch
Patch0119:	0119-Support-UEFI-networking-protocols.patch
Patch0120:	0120-AUDIT-0-http-boot-tracker-bug.patch
Patch0121:	0121-grub-core-video-efi_gop.c-Add-support-for-BLT_ONLY-a.patch
Patch0122:	0122-efi-uga-use-64-bit-for-fb_base.patch
Patch0123:	0123-EFI-console-Do-not-set-text-mode-until-we-actually-n.patch
Patch0124:	0124-EFI-console-Add-grub_console_read_key_stroke-helper-.patch
Patch0125:	0125-EFI-console-Implement-getkeystatus-support.patch
Patch0126:	0126-Make-grub_getkeystatus-helper-funtion-available-ever.patch
Patch0127:	0127-Accept-ESC-F8-and-holding-SHIFT-as-user-interrupt-ke.patch
Patch0128:	0128-grub-editenv-Add-incr-command-to-increment-integer-v.patch
Patch0129:	0129-Add-auto-hide-menu-support.patch
Patch0130:	0130-Output-a-menu-entry-for-firmware-setup-on-UEFI-FastB.patch
Patch0131:	0131-Add-grub-set-bootflag-utility.patch
Patch0132:	0132-docs-Add-grub-boot-indeterminate.service-example.patch
Patch0133:	0133-gentpl-add-disable-support.patch
Patch0134:	0134-gentpl-add-pc-firmware-type.patch
Patch0135:	0135-efinet-also-use-the-firmware-acceleration-for-http.patch
Patch0136:	0136-efi-http-Make-root_url-reflect-the-protocol-hostname.patch
Patch0137:	0137-Make-it-so-we-can-tell-configure-which-cflags-utils-.patch
Patch0138:	0138-module-verifier-make-it-possible-to-run-checkers-on-.patch
Patch0139:	0139-Rework-how-the-fdt-command-builds.patch
Patch0140:	0140-Disable-non-wordsize-allocations-on-arm.patch
Patch0141:	0141-strip-R-.note.gnu.property-at-more-places.patch
Patch0142:	0142-Prepend-prefix-when-HTTP-path-is-relative.patch
Patch0143:	0143-Make-linux_arm_kernel_header.hdr_offset-be-at-the-ri.patch
Patch0144:	0144-Make-grub_error-more-verbose.patch
Patch0145:	0145-Make-reset-an-alias-for-the-reboot-command.patch
Patch0146:	0146-EFI-more-debug-output-on-GOP-and-UGA-probing.patch
Patch0147:	0147-Add-a-version-command.patch
Patch0148:	0148-Add-more-dprintf-and-nerf-dprintf-in-script.c.patch
Patch0149:	0149-arm-arm64-loader-Better-memory-allocation-and-error-.patch
Patch0150:	0150-Try-to-pick-better-locations-for-kernel-and-initrd.patch
Patch0151:	0151-Attempt-to-fix-up-all-the-places-Wsign-compare-error.patch
Patch0152:	0152-Don-t-use-Wno-sign-compare-Wno-conversion-Wno-error-.patch
Patch0153:	0153-x86-efi-Use-bounce-buffers-for-reading-to-addresses-.patch
Patch0154:	0154-x86-efi-Re-arrange-grub_cmd_linux-a-little-bit.patch
Patch0155:	0155-x86-efi-Make-our-own-allocator-for-kernel-stuff.patch
Patch0156:	0156-x86-efi-Allow-initrd-params-cmdline-allocations-abov.patch
Patch0157:	0157-Fix-getroot.c-s-trampolines.patch
Patch0158:	0158-Do-not-allow-stack-trampolines-anywhere.patch
Patch0159:	0159-Reimplement-boot_counter.patch
Patch0160:	0160-Make-grub_strtol-end-pointers-have-safer-const-quali.patch
Patch0161:	0161-Fix-menu-entry-selection-based-on-ID-and-title.patch
Patch0162:	0162-Make-the-menu-entry-users-option-argument-to-be-opti.patch
Patch0163:	0163-Add-efi-export-env-and-efi-load-env-commands.patch
Patch0164:	0164-Make-it-possible-to-subtract-conditions-from-debug.patch
Patch0165:	0165-Export-all-variables-from-the-initial-context-when-c.patch
Patch0166:	0166-Fix-the-looking-up-grub.cfg-XXX-while-tftp-booting.patch
Patch0167:	0167-Try-to-set-fPIE-and-friends-on-libgnu.a.patch
Patch0168:	0168-Don-t-make-grub_strtoull-print-an-error-if-no-conver.patch
Patch0169:	0169-Fix-the-type-of-grub_efi_status_t.patch
Patch0170:	0170-grub.d-Split-out-boot-success-reset-from-menu-auto-h.patch
Patch0171:	0171-Fix-systemctl-kexec-exit-status-check.patch
Patch0172:	0172-Print-grub-emu-linux-loader-messages-as-debug.patch
Patch0173:	0173-Don-t-assume-that-boot-commands-will-only-return-on-.patch
Patch0174:	0174-Fix-undefined-references-for-fdt-when-building-with-.patch
Patch0175:	0175-Do-better-in-bootstrap.conf.patch
Patch0176:	0176-Use-git-to-apply-gnulib-patches.patch
Patch0177:	0177-autogen.sh-use-find-wholename-for-long-path-matches.patch
Patch0178:	0178-bootstrap.conf-don-t-clobber-AM_CFLAGS-here.patch
Patch0179:	0179-Fix-build-error-with-the-fdt-module-on-risc-v.patch
Patch0180:	0180-RISC-V-Fix-computation-of-pc-relative-relocation-off.patch
###Patch0181:	0181-blscfg-Add-support-for-the-devicetree-field.patch
###Patch0182:	0182-Set-a-devicetree-var-in-a-BLS-config-if-GRUB_DEFAULT.patch
###Patch0183:	0183-Don-t-add-a-class-option-to-menu-entries-generated-f.patch
###Patch0184:	0184-10_linux.in-Also-use-GRUB_CMDLINE_LINUX_DEFAULT-to-s.patch
###Patch0185:	0185-blscfg-Don-t-hardcode-an-env-var-as-fallback-for-the.patch
Patch0186:	0186-grub-set-bootflag-Update-comment-about-running-as-ro.patch
Patch0187:	0187-grub-set-bootflag-Write-new-env-to-tmpfile-and-then-.patch
###Patch0188:	0188-blscfg-add-a-space-char-when-appending-fields-for-va.patch
Patch0189:	0189-grub.d-Fix-boot_indeterminate-getting-set-on-boot_su.patch
###Patch0190:	0190-blscfg-Add-support-for-sorting-the-plus-higher-than-.patch
###Patch0191:	0191-Fix-savedefault-with-blscfg.patch
Patch0192:	0192-Also-define-GRUB_EFI_MAX_ALLOCATION_ADDRESS-for-RISC.patch
Patch0193:	0193-chainloader-Define-machine-types-for-RISC-V.patch
Patch0194:	0194-Add-start-symbol-for-RISC-V.patch
Patch0195:	0195-RISC-V-Add-__clzdi2-symbol.patch
Patch0196:	0196-grub-install-Define-default-platform-for-RISC-V.patch
###Patch0197:	0197-blscfg-Always-use-the-root-variable-to-search-for-BL.patch
Patch0198:	0198-bootstrap.conf-Force-autogen.sh-to-use-python3.patch
Patch0199:	0199-efi-http-Export-fw-http-_path-variables-to-make-them.patch
Patch0200:	0200-efi-http-Enclose-literal-IPv6-addresses-in-square-br.patch
Patch0201:	0201-efi-net-Allow-to-specify-a-port-number-in-addresses.patch
Patch0202:	0202-efi-ip4_config-Improve-check-to-detect-literal-IPv6-.patch
Patch0203:	0203-efi-net-Print-a-debug-message-if-parsing-the-address.patch
###Patch0204:	0204-blscfg-return-NULL-instead-of-a-zero-length-array-in.patch
###Patch0205:	0205-grub-switch-to-blscfg-Update-grub2-binary-in-ESP-for.patch
###Patch0206:	0206-grub-switch-to-blscfg-Only-mark-GRUB-as-BLS-supporte.patch
###Patch0207:	0207-10_linux.in-Merge-logic-from-10_linux_bls-and-drop-t.patch
###Patch0208:	0208-grub-switch-to-blscfg-Use-install-to-copy-GRUB-binar.patch
###Patch0209:	0209-10_linux.in-Enable-BLS-configuration-if-new-kernel-p.patch
Patch0210:	0210-efi-Set-image-base-address-before-jumping-to-the-PE-.patch
###Patch0211:	0211-blscfg-Lookup-default_kernelopts-variable-as-fallbac.patch
###Patch0212:	0212-10_linux.in-fix-early-exit-due-error-when-reading-pe.patch
Patch0213:	0213-envblk-Fix-buffer-overrun-when-attempting-to-shrink-.patch
###Patch0214:	0214-10_linux.in-Store-cmdline-in-BLS-snippets-instead-of.patch
###Patch0215:	0215-10_linux.in-restore-existence-check-in-get_sorted_bl.patch
Patch0216:	0216-tpm-Don-t-propagate-TPM-measurement-errors-to-the-ve.patch
Patch0217:	0217-tpm-Enable-module-for-all-EFI-platforms.patch
###Patch0218:	0218-10_linux.in-Don-t-update-BLS-files-that-aren-t-manag.patch
Patch0219:	0219-x86-efi-Reduce-maximum-bounce-buffer-size-to-16-MiB.patch
Patch0220:	0220-http-Prepend-prefix-when-the-HTTP-path-is-relative-a.patch
Patch0221:	0221-fix-build-with-rpm-4.16.patch

# Other patches
Patch0400:	grub2-locales.patch
Patch0401:	grub2-00_header.patch
Patch0402:	grub2-custom-color.patch
Patch0403:	grub2-read-cfg.patch
Patch0404:	grub2-symlink-is-garbage.patch
Patch0406:	grub-2.02-fuse3.patch
# (crazy) replaces:
# grub-2.00.Linux.remove.patch
# grub-2.00-add-recovery_option.patch
# grub2-2.02-add-support-for-kernel-install.patch
# fix-btrfs-GRUB_CMDLINE_LINUX_RECOVERY.patch ( https://issues.openmandriva.org/show_bug.cgi?id=2423 )
# Ok @bero .. ( also use this patch for OMV things touchting /grub.d/ and so on )
# In addition console boot support got added ( https://issues.openmandriva.org/show_bug.cgi?id=2402 )
# (tpg) 2020-06-25 does it is really needed ?
#Patch0407:	omv-configuration.patch
Patch0408:	grub-2.00-fix-dejavu-font.patch
Patch0409:	grub2-2.00-class-via-os-prober.patch
Patch0410:	grub-2.00-autoreconf-sucks.patch
Patch0411:	grub-2.02-beta2-custom-vendor-config.patch
Patch0412:	fix-microcode-os-prober-initrd-line-parsing.patch
Patch0413:	grub-2.02-20180620-disable-docs.patch
# Without this, build fails on aarch64 w/ unresolved symbol abort
# while running grub-mkimage
%ifarch aarch64
Patch0414:	grub-2.02-define-abort.patch
%endif
Patch0415:	grub-2.04-grub-extras-lua-fix.patch
# Show clang kernels after gcc kernels
Patch0416:	grub2-clang-kernels-last.patch

# Upstream patches
Patch0500:	grub2-2.04-fix-grub-install-locale-copy.patch

# Patches from Unity
Patch0502:	grub2-2.02-unity-mkrescue-use-grub2-dir.patch

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
BuildRequires:	git-core
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
%endif
Requires:	efi-filesystem

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
%global ldflags %{ldflags} -fuse-ld=bfd
%endif

%prep
%if "%{snapshot}" == ""
%setup -qn grub-%{version} -a12
%else
%setup -qn grub-%{version}-%{snapshot} -a12
%endif

cp -a %{SOURCE20} bootstrap
cp -a %{SOURCE21} bootstrap.conf

%autopatch -p1

chmod +x bootstrap
./bootstrap

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

%define grub_modules_default all_video boot btrfs cat chain configfile cryptodisk echo efifwsetup efinet ext2 f2fs fat font gcry_rijndael gcry_rsa gcry_serpent gcry_sha256 gcry_twofish gcry_whirlpool gfxmenu gfxterm gfxterm_background gfxterm_menu gzio halt hfsplus iso9660 jpeg loadenv loopback linux lsefi luks lvm mdraid09 mdraid1x minicmd normal part_apple part_gpt part_msdos password_pbkdf2 probe png reboot regexp search search_fs_file search_fs_uuid search_label serial sleep squash4 syslinuxcfg test tftp video xfs zstd

%ifarch aarch64
%define grubefiarch arm64-efi
%define grub_modules %{grub_modules_default}
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
cd %{buildroot}%{_sbindir}
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
install -m755 %{SOURCE9} -D %{buildroot}%{_sbindir}

install -d %{buildroot}/boot/%{name}/themes/

#bugfix: error message before loading of grub2 menu on boot
mkdir -p %{buildroot}%{_localedir}/en/LC_MESSAGES
cp -f %{buildroot}%{_localedir}/en@quot/LC_MESSAGES/grub.mo %{buildroot}%{_localedir}/en/LC_MESSAGES/grub.mo

# (tpg) remove *.modules and leave *.mod
# Allow stuff to fail because some modules may not have been built
# (e.g. no EFI)
find %{buildroot}%{libdir32}/grub/*-%{platform} -name "*.module" -delete || :
find %{buildroot}%{libdir32}/grub/%{_arch}-efi/ -name "*.module" -delete || :

rm -f %{buildroot}%{_sbindir}/%{name}-sparc64-setup
rm -f %{buildroot}%{_sbindir}/%{name}-ofpathname

%find_lang grub

%post
exec >/dev/null 2>&1

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
fi

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
    %{_sbindir}/update-grub2
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
