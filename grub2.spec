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

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
## WARNING! before updating snapshots grep local for
## 'boot/grub' in the source , including Makefiles*
## and compare to grub2-2.02-unity-mkrescue-use-grub2-dir.patch
## do _NOT_ update without doing that .. we just go lucky until now.
Version:	2.06
Release:	3
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
# Show clang kernels after gcc kernels
Patch18:	grub2-clang-kernels-last.patch

# (crazy) these are 2 BAD patches , FIXME after Lx4
# Patch7 prepares remove for that ( partially )
# Patches from Mageia
Patch100:	grub2-2.00-mga-dont_write_sparse_file_error_to_screen.patch
Patch101:	grub2-2.00-mga-dont_write_diskfilter_error_to_screen.patch

# Patches from SuSe

# Patches from Unity
Patch300:	grub2-2.02-unity-mkrescue-use-grub2-dir.patch

# Patches from upstream
# [Selected from running git format-patch grub-2.06 in master branch]
Patch1001:	0002-zfs-Use-grub_uint64_t-instead-of-1ULL-in-BF64_-CODE-.patch
Patch1002:	0003-fs-ext2-Ignore-checksum-seed-incompat-feature.patch
Patch1003:	0004-tests-ahci-Change-ide-drive-deprecated-QEMU-device-n.patch
Patch1004:	0005-ieee1275-Drop-HEAP_MAX_ADDR-and-HEAP_MIN_SIZE-consta.patch
Patch1005:	0006-osdep-Introduce-include-grub-osdep-major.h-and-use-i.patch
Patch1006:	0007-osdep-linux-hostdisk-Use-stat-instead-of-udevadm-for.patch
Patch1007:	0008-commands-setpci-Honor-write-mask-argument.patch
Patch1008:	0009-libgcrypt-Avoid-Wsign-compare-in-rijndael-do_setkey.patch
Patch1009:	0010-libgcrypt-Avoid-Wempty-body-in-rijndael-do_setkey.patch
Patch1010:	0011-fs-xfs-Fix-unreadable-filesystem-with-v4-superblock.patch
Patch1011:	0012-configure-Remove-obsoleted-malign-jumps-loops-functi.patch
Patch1012:	0013-configure-Check-for-falign-jumps-1-beside-falign-loo.patch
Patch1013:	0014-tests-Let-xorriso-fixely-assume-UTF-8-as-local-chara.patch
Patch1015:	0016-autogen.sh-Detect-python.patch
Patch1016:	0017-kern-fs-Allow-number-of-blocks-in-block-list-to-be-o.patch
Patch1017:	0018-commands-read-Add-silent-mode-to-read-command-to-sup.patch
Patch1018:	0019-tests-Keep-grub-fs-tester-ziso9660-from-failing-for-.patch
Patch1019:	0020-emu-Fix-executable-stack-marking.patch
Patch1020:	0021-templates-Add-GRUB_CMDLINE_LINUX_RECOVERY.patch
Patch1021:	0022-fs-udf-Fix-regression-which-is-preventing-symlink-ac.patch
Patch1022:	0023-docs-grub-Improve-search-documentation-by-adding-sho.patch
Patch1023:	0024-powerpc-Drop-Open-Hack-Ware.patch
Patch1024:	0025-powerpc-Drop-Open-Hack-Ware-remove-GRUB_IEEE1275_FLA.patch
Patch1025:	0026-powerpc-Drop-Open-Hack-Ware-remove-GRUB_IEEE1275_FLA.patch
Patch1026:	0027-powerpc-Drop-Open-Hack-Ware-remove-GRUB_IEEE1275_FLA.patch
Patch1027:	0028-powerpc-Drop-Open-Hack-Ware-remove-GRUB_IEEE1275_FLA.patch
Patch1028:	0029-fs-ext2-Fix-handling-of-missing-sparse-extent-leafs.patch
Patch1029:	0030-disk-diskfilter-Use-nodes-in-logical-volume-s-segmen.patch
Patch1030:	0031-build-Fix-build-error-with-binutils-2.36.patch
Patch1031:	0032-docs-grub-dev-Fix-typos.patch
Patch1032:	0033-tests-Fix-partmap_test-for-arm-efi-disk-numbering-ha.patch
Patch1033:	0034-tests-When-checking-squashfs-fstime-use-superblock-l.patch
Patch1034:	0035-tests-Add-set-e-to-missing-tests.patch
Patch1035:	0036-tests-Do-not-occlude-subshell-error-codes-when-used-.patch
Patch1036:	0037-tests-Do-not-occlude-grub-shell-return-code.patch
Patch1037:	0038-tests-Make-setup-errors-in-grub-fs-tester-hard-error.patch
Patch1038:	0039-tests-A-failure-of-mktemp-should-cause-the-test-scri.patch
Patch1039:	0040-tests-Exit-with-skipped-exit-code-when-test-not-perf.patch
Patch1040:	0041-tests-Use-BUILD_SHEBANG-autoconf-var-instead-of-lite.patch
Patch1041:	0042-tests-Rename-variable-filtime-filetime-as-its-meant-.patch
Patch1042:	0043-tests-mkreiserfs-only-supports-4096-block-size.patch
Patch1043:	0044-tests-Disable-ReiserFS-tests-for-old-format-because-.patch
Patch1044:	0045-tests-mkfs.btrfs-now-supports-only-4-KiB-sector-size.patch
Patch1045:	0046-tests-Only-test-MINIX3-volumes-of-1-KiB-block-size.patch
Patch1046:	0047-tests-Change-FAT-volume-label-to-be-with-in-the-vali.patch
Patch1047:	0048-tests-Skip-HFS-test-only-when-mac_roman-module-is-no.patch
Patch1048:	0049-tests-Output-list-of-devices-when-partmap-fails.patch
Patch1049:	0050-tests-Do-not-delete-filesystem-images-on-error.patch
Patch1050:	0051-docs-Add-fuller-accounting-of-make-check-prerequisit.patch
Patch1051:	0052-osdep-linux-Fix-md-array-device-enumeration.patch
Patch1052:	0053-tests-Boot-PowerPC-using-PMU-instead-of-CUDA-for-pow.patch
Patch1053:	0054-tests-Test-aborts-due-to-missing-requirements-should.patch
Patch1054:	0055-tests-In-partmap_test-use-parted-variable-when-check.patch
Patch1055:	0056-kern-misc-Add-debug-log-condition-to-log-output.patch
Patch1056:	0057-kern-dl-Print-module-name-on-license-check-failure.patch
Patch1057:	0058-util-grub-install-common-Fix-memory-leak-in-copy_all.patch
Patch1058:	0059-util-grub-mkrescue-Fix-memory-leak-in-write_part.patch
Patch1059:	0060-util-grub-fstest-Fix-resource-leaks-in-cmd_cmp.patch
Patch1060:	0061-util-grub-mkfont-Fix-memory-leak-in-write_font_pf2.patch
Patch1061:	0062-fs-zfs-zfs-Fix-possible-insecure-use-of-chunk-size-i.patch
Patch1062:	0063-io-gzio-Fix-possible-use-of-uninitialized-variable-i.patch
Patch1063:	0064-templates-Filter-out-POSIX-locale-for-translation.patch
Patch1064:	0065-commands-probe-Fix-resource-leaks.patch
Patch1065:	0066-disk-ldm-Fix-resource-leak.patch
Patch1066:	0067-fs-btrfs-Make-extent-item-iteration-to-handle-gaps.patch
Patch1067:	0068-docs-Add-sentence-on-where-Debian-packages-can-be-se.patch
Patch1068:	0069-docs-Update-development-docs-to-include-information-.patch
Patch1069:	0070-docs-Fix-broken-links-in-development-docs.patch
Patch1070:	0071-docs-Add-documentation-on-packages-for-building-docu.patch
Patch1071:	0072-minilzo-Update-to-minilzo-2.10.patch
Patch1072:	0073-efinet-Correct-closing-of-SNP-protocol.patch
Patch1073:	0074-efi-Create-the-grub_efi_close_protocol-library-funct.patch
Patch1074:	0075-grub-mkconfig-Restore-umask-for-the-grub.cfg.patch
Patch1075:	0076-configure-Fix-misspelled-variable-BUILD_LDFAGS-BUILD.patch
Patch1076:	0077-luks2-Add-debug-message-to-align-with-luks-and-geli-.patch
Patch1077:	0078-cryptodisk-Refactor-to-discard-have_it-global.patch
Patch1078:	0079-cryptodisk-Return-failure-in-cryptomount-when-no-cry.patch
Patch1079:	0080-cryptodisk-Improve-error-messaging-in-cryptomount-in.patch
Patch1080:	0081-cryptodisk-Improve-cryptomount-u-error-message.patch
Patch1081:	0082-cryptodisk-Add-infrastructure-to-pass-data-from-cryp.patch
Patch1082:	0083-cryptodisk-Refactor-password-input-out-of-crypto-dev.patch
Patch1083:	0084-cryptodisk-Move-global-variables-into-grub_cryptomou.patch
Patch1084:	0085-cryptodisk-Improve-handling-of-partition-name-in-cry.patch
Patch1085:	0086-tests-Refactor-building-xorriso-command-for-iso9660-.patch
Patch1086:	0087-fs-btrfs-Use-full-btrfs-bootloader-area.patch
Patch1087:	0088-mm-Document-GRUB-internal-memory-management-structur.patch
Patch1088:	0089-mm-Clarify-grub_real_malloc.patch
Patch1089:	0090-mm-grub_real_malloc-Make-small-allocs-comment-match-.patch
Patch1090:	0091-mm-Document-grub_free.patch
Patch1091:	0092-mm-Document-grub_mm_init_region.patch
Patch1092:	0093-cryptodisk-Fix-Coverity-use-after-free-bug.patch
Patch1093:	0094-kern-misc-Allow-selective-disabling-of-debug-facilit.patch
Patch1094:	0095-util-resolve-Do-not-read-past-the-end-of-the-array-i.patch
Patch1095:	0096-util-resolve-Bail-with-error-if-moddep.lst-file-line.patch
Patch1096:	0097-gentpl.py-Fix-issue-where-sometimes-marker-files-hav.patch
Patch1097:	0098-Makefile-Only-look-for-MARKER-at-the-start-of-a-line.patch
Patch1098:	0099-net-http-Allow-use-of-non-standard-TCP-IP-ports.patch
Patch1099:	0100-conf-Makefile.common-Order-alphabetically-variables.patch
Patch1100:	0101-efi-Correct-struct-grub_efi_boot_services.patch
Patch1101:	0102-RISC-V-Adjust-march-flags-for-binutils-2.38.patch
Patch1102:	0103-fs-affs-Fix-resource-leaks.patch
Patch1103:	0104-util-grub-module-verifierXX-Add-function-to-calculat.patch
Patch1104:	0105-util-grub-module-verifierXX-Validate-number-of-elf-s.patch
Patch1105:	0106-util-grub-module-verifierXX-Validate-elf-section-hea.patch
Patch1106:	0107-tests-Do-not-remove-image-file-on-error-in-pata_test.patch
Patch1107:	0108-tests-Skip-pata_test-on-i386-efi.patch
Patch1108:	0109-tests-Remove-BASE-NUM-bashism-in-grub-fs-tester.patch
Patch1109:	0110-Revert-iee1275-datetime-Fix-off-by-1-error.patch
Patch1110:	0111-commands-search-Fix-bug-stopping-iteration-when-no-f.patch
Patch1111:	0112-tests-Add-check-native-and-check-nonnative-make-targ.patch
Patch1112:	0113-configure-Replace-Wl-r-d-with-Wl-r-and-add-fno-commo.patch
Patch1113:	0114-configure-Properly-handle-MM_DEBUG.patch
Patch1114:	0115-mm-Export-grub_mm_dump-and-grub_mm_dump_free.patch
Patch1115:	0116-mm-Temporarily-disable-grub_mm_debug-while-calling-g.patch
Patch1116:	0117-templates-Add-support-for-pci-arbiter-and-rumpdisk-o.patch
Patch1117:	0118-templates-Properly-handle-multiple-initrd-paths-in-3.patch
Patch1118:	0119-ChangeLog-Retire-ChangeLog-2015.patch
Patch1119:	0120-tests-Fix-whitespace-formatting.patch
Patch1120:	0121-commands-efi-lsefisystab-Short-text-EFI_IMAGE_SECURI.patch
Patch1121:	0122-net-ethernet-Fix-VLAN-networking-on-little-endian-sy.patch
Patch1122:	0123-bus-Remove-trailing-whitespaces.patch
Patch1123:	0124-commands-Remove-trailing-whitespaces.patch
Patch1124:	0125-disk-Remove-trailing-whitespaces.patch
Patch1125:	0126-font-Remove-trailing-whitespaces.patch
Patch1126:	0127-fs-Remove-trailing-whitespaces.patch
Patch1127:	0128-gfxmenu-Remove-trailing-whitespaces.patch
Patch1128:	0129-gfxmenu-Remove-trailing-whitespaces.patch
Patch1129:	0130-io-Remove-trailing-whitespaces.patch
Patch1130:	0131-kern-Remove-trailing-whitespaces.patch
Patch1131:	0132-lib-Remove-trailing-whitespaces.patch
Patch1132:	0133-loader-Remove-trailing-whitespaces.patch
Patch1133:	0134-net-Remove-trailing-whitespaces.patch
Patch1134:	0135-normal-Remove-trailing-whitespaces.patch
Patch1135:	0136-osdep-Remove-trailing-whitespaces.patch
Patch1136:	0137-partmap-Remove-trailing-whitespaces.patch
Patch1137:	0138-script-Remove-trailing-whitespaces.patch
Patch1138:	0139-term-Remove-trailing-whitespaces.patch
Patch1139:	0140-tests-Remove-trailing-whitespaces.patch
Patch1140:	0141-video-Remove-trailing-whitespaces.patch
Patch1141:	0142-util-Remove-trailing-whitespaces.patch
Patch1142:	0143-include-Remove-trailing-whitespaces.patch
Patch1143:	0144-grub-mount-Add-support-for-libfuse3.patch
Patch1144:	0145-net-Check-against-nb-tail-in-grub_netbuff_pull.patch
Patch1145:	0146-po-Un-transliterate-the-zu-format-code.patch
Patch1146:	0147-osdep-windows-platform-Disable-gcc9-Waddress-of-pack.patch
Patch1147:	0148-loader-i386-bsd-Initialize-ptr-variable-in-grub_bsd_.patch
Patch1148:	0149-commands-i386-pc-sendkey-Fix-writing-1-byte-into-a-r.patch
Patch1149:	0150-conf-i386-cygwin-img-ld-Do-not-discard-.data-and-.ed.patch
Patch1150:	0151-configure-Drop-grub_coredir-unneeded-references.patch
Patch1151:	0152-INSTALL-Add-more-cross-compiling-Debian-packages.patch
Patch1152:	0153-INSTALL-Drop-mention-of-libusb.patch
Patch1153:	0154-config.h.in-Use-visual-indentation.patch
Patch1154:	0155-config-Where-present-ensure-config-util.h-precedes-c.patch
Patch1159:	0160-configure-Fix-various-new-autotools-warnings.patch
Patch1160:	0161-lib-posix_wrap-errno.h-Add-__set_errno-macro.patch
Patch1161:	0162-grub-mkimage-Only-check-aarch64-relocations-when-bui.patch
Patch1162:	0163-kern-rescue_parser-Ensure-that-parser-allocated-memo.patch
Patch1163:	0164-term-efi-console-Do-not-set-colorstate-until-the-fir.patch
Patch1164:	0165-term-efi-console-Do-not-set-cursor-until-the-first-t.patch
Patch1167:	0168-commands-search-Refactor-no-floppy-option-to-have-so.patch
Patch1168:	0169-commands-search-Add-new-efidisk-only-option-for-EFI-.patch
Patch1169:	0170-gdb-Add-malloc-and-free-symbols-to-kernel.exec-to-im.patch
Patch1170:	0171-configure-Allow-HOST_CC-to-override-CC.patch
Patch1171:	0172-configure-Sort-AM_CONDITIONALs-alphabetically.patch
Patch1172:	0173-configure-Remove-dead-code.patch
Patch1173:	0174-configure-Remove-unused-CFLAGS-definitions.patch
Patch1174:	0175-configure-Whitespace-changes-to-improve-readability.patch
Patch1175:	0176-INSTALL-Add-information-on-using-build-when-cross-co.patch
Patch1176:	0177-net-net-Unset-grub_net_poll_cards_idle-when-net-modu.patch
Patch1177:	0178-net-net-Avoid-unnecessary-calls-to-grub_net_tcp_retr.patch
Patch1178:	0179-net-tcp-Only-call-grub_get_time_ms-when-there-are-so.patch
Patch1179:	0180-net-arp-Fix-uninitialized-scalar-variable.patch
Patch1180:	0181-net-bootp-Fix-uninitialized-scalar-variable.patch
Patch1181:	0182-net-net-Fix-uninitialized-scalar-variable.patch
Patch1182:	0183-loader-i386-bsd-Fix-uninitialized-scalar-variable.patch
Patch1183:	0184-loader-i386-pc-linux-Fix-uninitialized-scalar-variab.patch
Patch1184:	0185-loader-i386-xnu-Fix-uninitialized-scalar-variable.patch
Patch1185:	0186-loader-i386-xnu-Fix-uninitialized-scalar-variable.patch
Patch1186:	0187-kern-efi-init-Log-a-console-error-during-a-stack-che.patch
Patch1187:	0188-net-net-Add-vlan-information-to-net_ls_addr-output.patch
Patch1188:	0189-net-net-Add-net_set_vlan-command.patch
Patch1189:	0190-kern-efi-efi-Print-VLAN-info-in-EFI-device-path.patch
Patch1190:	0191-net-drivers-efi-efinet-Configure-VLAN-from-UEFI-devi.patch
Patch1191:	0192-util-mkimage-Fix-dangling-pointer-may-be-used-error.patch
Patch1192:	0193-build-Fix-Werror-array-bounds-array-subscript-0-is-o.patch
Patch1193:	0194-lib-reed_solomon-Fix-array-subscript-0-is-outside-ar.patch
Patch1194:	0195-video-readers-jpeg-Fix-possible-invalid-loop-boundar.patch
Patch1196:	0197-tests-Disable-blkid-cache-usage.patch
Patch1197:	0198-tests-Give-grub-fs-tester-temp-directory-a-better-na.patch
Patch1198:	0199-docs-Add-note-that-drivemap-is-only-available-on-i38.patch
Patch1199:	0200-docs-Clarify-meaning-of-list-and-cond-for-if-and-whi.patch
Patch1200:	0201-docs-Use-correct-list-format.patch
Patch1201:	0202-tests-Ensure-that-mountpoints-are-unmounted-before-e.patch
Patch1202:	0203-tests-Ensure-that-loopback-devices-and-zfs-devices-a.patch
Patch1203:	0204-net-Fix-NULL-pointer-dereference-when-parsing-ICMP6_.patch
Patch1204:	0205-grub-install-Allow-to-install-to-non-EFI-ESP-when-fo.patch
Patch1205:	0206-grub-mkimage-Creating-aarch64-images-from-x86-host-i.patch
Patch1206:	0207-osdep-hurd-Support-device-entries-with-dev-disk-qual.patch
Patch1208:	0209-net-net-Fix-incorrect-condition-for-calling-grub_net.patch
Patch1209:	0210-docs-Fix-spelling-typo-and-remove-unnecessary-spaces.patch
Patch1210:	0211-docs-Make-note-that-sendkey-is-only-available-on-i38.patch
Patch1211:	0212-docs-Make-note-of-i386-pc-specific-usage-of-halt-com.patch
Patch1212:	0213-docs-Markup-loader-commands-with-command-tag.patch
Patch1213:	0214-docs-Create-command-section-for-loader-commands.patch
Patch1214:	0215-docs-Add-under-documented-loader-commands-to-beginni.patch
Patch1215:	0216-docs-Add-section-for-general-undocumented-commands.patch
Patch1216:	0217-tests-Show-host-determined-fs-UUID-when-hfs-UUID-tes.patch
Patch1217:	0218-tests-Add-sbin-and-usr-sbin-to-path-in-partmap-test.patch
Patch1218:	0219-commands-macbless-Remove-whitespace-between-N_-macro.patch
Patch1219:	0220-util-probe-Remove-unused-header-includes.patch
Patch1220:	0221-disk-luks-Unify-grub_cryptodisk_dev-function-names.patch
Patch1221:	0222-disk-geli-Unify-grub_cryptodisk_dev-function-names.patch
Patch1222:	0223-disk-cryptodisk-Add-options-to-cryptomount-to-suppor.patch
Patch1223:	0224-disk-cryptodisk-Use-enum-constants-as-indexes-into-c.patch
Patch1224:	0225-docs-Add-documentation-on-keyfile-option-to-cryptomo.patch
Patch1225:	0226-osdep-hurd-getroot-Use-part-qualifier.patch
Patch1226:	0227-disk-efi-efidisk-Pass-buffers-with-higher-alignment.patch
Patch1227:	0228-grub-core-loader-i386-bsdXX-Avoid-downcasting-char-t.patch
Patch1228:	0229-util-grub-module-verifierXX-Add-e_shoff-check-in-get.patch
Patch1229:	0230-fs-zfs-zfs-make_mdn-avoid-pointer-downcasting.patch
Patch1230:	0231-fs-zfs-zfs-zfs_mount-avoid-pointer-downcasting.patch
Patch1231:	0232-loader-efi-chainloader-Simplify-the-loader-state.patch
Patch1232:	0233-commands-boot-Add-API-to-pass-context-to-loader.patch
Patch1233:	0234-loader-efi-chainloader-Use-grub_loader_set_ex.patch
Patch1234:	0235-kern-efi-sb-Reject-non-kernel-files-in-the-shim_lock.patch
Patch1235:	0236-kern-file-Do-not-leak-device_name-on-error-in-grub_f.patch
Patch1236:	0237-video-readers-png-Abort-sooner-if-a-read-operation-f.patch
Patch1237:	0238-video-readers-png-Refuse-to-handle-multiple-image-he.patch
Patch1238:	0239-video-readers-png-Drop-greyscale-support-to-fix-heap.patch
Patch1239:	0240-video-readers-png-Avoid-heap-OOB-R-W-inserting-huff-.patch
Patch1240:	0241-video-readers-png-Sanity-check-some-huffman-codes.patch
Patch1241:	0242-video-readers-jpeg-Abort-sooner-if-a-read-operation-.patch
Patch1242:	0243-video-readers-jpeg-Do-not-reallocate-a-given-huff-ta.patch
Patch1243:	0244-video-readers-jpeg-Refuse-to-handle-multiple-start-o.patch
Patch1244:	0245-video-readers-jpeg-Block-int-underflow-wild-pointer-.patch
Patch1245:	0246-normal-charset-Fix-array-out-of-bounds-formatting-un.patch
Patch1246:	0247-net-ip-Do-IP-fragment-maths-safely.patch
Patch1247:	0248-net-netbuff-Block-overly-large-netbuff-allocs.patch
Patch1248:	0249-net-dns-Fix-double-free-addresses-on-corrupt-DNS-res.patch
Patch1249:	0250-net-dns-Don-t-read-past-the-end-of-the-string-we-re-.patch
Patch1250:	0251-net-tftp-Prevent-a-UAF-and-double-free-from-a-failed.patch
Patch1251:	0252-net-tftp-Avoid-a-trivial-UAF.patch
Patch1252:	0253-net-http-Do-not-tear-down-socket-if-it-s-already-bee.patch
Patch1253:	0254-net-http-Fix-OOB-write-for-split-http-headers.patch
Patch1254:	0255-net-http-Error-out-on-headers-with-LF-without-CR.patch
Patch1255:	0256-fs-f2fs-Do-not-read-past-the-end-of-nat-journal-entr.patch
Patch1256:	0257-fs-f2fs-Do-not-read-past-the-end-of-nat-bitmap.patch
Patch1257:	0258-fs-f2fs-Do-not-copy-file-names-that-are-too-long.patch
Patch1258:	0259-fs-btrfs-Fix-several-fuzz-issues-with-invalid-dir-it.patch
Patch1259:	0260-fs-btrfs-Fix-more-ASAN-and-SEGV-issues-found-with-fu.patch
Patch1260:	0261-fs-btrfs-Fix-more-fuzz-issues-related-to-chunks.patch
Patch1261:	0291-fs-fat-Don-t-error-when-mtime-is-0.patch

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
%if "%{snapshot}" == ""
%setup -qn grub-%{version} -a12
%else
%setup -qn grub-%{version}-%{snapshot} -a12
%endif
%autopatch -p1

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
