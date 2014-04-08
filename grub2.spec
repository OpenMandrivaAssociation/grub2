%define libdir32 %{_exec_prefix}/lib
%define platform pc
%define efi 1
#%define		unifont		%(echo %{_datadir}/fonts/TTF/unifont/unifont-*.ttf)

%global efi %{ix86} x86_64
%global optflags %{optflags} -Os

%bcond_with	talpo
%bcond_with	uclibc

Summary:	GNU GRUB is a Multiboot boot loader
Name:		grub2
Version:	2.00
Release:	39
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
Source12:	grub-lua-rev28.tar.xz
# documentation and simple test script for testing grub2 themes
Source13:	mandriva-grub2-theme-test.sh
Source14:	ntldr-img-rev21.tar.xz
Source15:	gpxe-rev15.tar.xz
Source16:	linguas.sh

# fedora patches
Patch0000:	grub-2.00-bzrignore.patch
Patch0001:	0001-Add-monochrome-text-support-mda_text-aka-hercules-in.patch
Patch0002:	0002-missing-file-from-last-commit.patch
Patch0003:	0003-grub-core-loader-i386-linux.c-find_efi_mmap_size-Don.patch
Patch0004:	0004-include-grub-list.h-FOR_LIST_ELEMENTS_SAFE-New-macro.patch
Patch0005:	0005-gentpl.py-Make-mans-depend-on-grub-mkconfig_lib.patch
Patch0006:	0006-grub-core-net-tftp.c-ack-Fix-endianness-problem.patch
Patch0007:	0007-grub-core-fs-ext2.c-Experimental-support-for-64-bit.patch
Patch0008:	0008-grub-core-term-efi-serial.c-Support-1.5-stop-bits.patch
Patch0009:	0009-grub-core-lib-legacy_parse.c-Support-clear-and-testl.patch
Patch0010:	0010-grub-core-Makefile.am-Fix-path-to-boot-i386-pc-start.patch
Patch0011:	0011-Fix-coreboot-compilation.patch
Patch0012:	0012-grub-core-normal-autofs.c-autoload_fs_module-Save-an.patch
Patch0013:	0013-grub-core-lib-xzembed-xz_dec_stream.c-hash_validate-.patch
Patch0014:	0014-grub-core-loader-i386-bsd.c-grub_bsd_elf32_size_hook.patch
Patch0015:	0015-New-command-lsefi.patch
Patch0016:	0016-util-grub-mkconfig_lib.in-grub_quote-Remove-extra-la.patch
Patch0017:	0017-EHCI-and-OHCI-PCI-bus-master.patch
Patch0018:	0018-Update-manual-NetBSD-wise.patch
Patch0019:	0019-Regenerate-po-POTFILES.in-with-the-following-commman.patch
Patch0020:	0020-Strengthen-the-configure-test-for-working-nostdinc-i.patch
Patch0021:	0021-.bzrignore-Add-grub-bios-setup-grub-ofpathname-and.patch
Patch0022:	0022-docs-man-grub-mkdevicemap.h2m-Remove-since-grub-mkde.patch
Patch0023:	0023-grub-core-mmap-mips-loongson-Remove-empty-directory.patch
Patch0024:	0024-Makefile.am-EXTRA_DIST-Add.patch
Patch0025:	0025-Makefile.am-EXTRA_DIST-Add-linguas.sh.-It-s-only-str.patch
Patch0026:	0026-grub-core-fs-xfs.c-grub_xfs_read_block-Make-keys-a-c.patch
Patch0027:	0027-grub-core-partmap-dvh.c-grub_dvh_is_valid-Add-missin.patch
Patch0028:	0028-grub-core-script-yylex.l-Ignore-unused-function-and-.patch
Patch0029:	0029-grub-core-disk-ieee1275-ofdisk.c-scan-Check-function.patch
Patch0030:	0030-util-import_gcry.py-Sort-cipher_files-to-make-build-.patch
Patch0031:	0031-NEWS-Fix-typo.patch
Patch0032:	0032-configure.ac-Add-SuSe-path.patch
Patch0033:	0033-grub-core-Makefile.core.def-efifwsetup-New-module.patch
Patch0034:	0034-grub-core-loader-efi-appleloader.c-devpath_8-New-var.patch
Patch0035:	0035-grub-core-disk-diskfilter.c-free_array-GRUB_UTIL-Fix.patch
Patch0036:	0036-Don-t-require-grub-mkconfig_lib-to-generate-manpages.patch
Patch0037:	0037-include-grub-efi-api.h-grub_efi_runtime_services-Mak.patch
Patch0038:	0038-grub-core-term-terminfo.c-Only-fix-up-powerpc-key-re.patch
Patch0039:	0039-util-grub-mkconfig_lib.in-grub_quote-Remove-outdated.patch
Patch0040:	0040-grub-core-loader-i386-linux.c-grub_cmd_linux-Fix-inc.patch
Patch0041:	0041-grub-core-kern-ieee1275-cmain.c-grub_ieee1275_find_o.patch
Patch0042:	0042-util-grub-mkconfig_lib.in-grub_tab-New-variable.patch
Patch0043:	0043-util-grub-setup.c-write_rootdev-Remove-unused-core_i.patch
Patch0044:	0044-grub-core-partmap-msdos.c-pc_partition_map_embed-Rev.patch
Patch0045:	0045-Fix-grub-emu-build-on-FreeBSD.patch
Patch0046:	0046-util-grub-install.in-Make-the-error-message-if-sourc.patch
Patch0047:	0047-grub-core-fs-affs.c-grub_affs_mount-Support-AFFS-boo.patch
Patch0048:	0048-util-grub-mkconfig_lib.in-is_path_readable_by_grub-R.patch
Patch0049:	0049-Makefile.util.def-grub-mknetdir-Move-to-prefix-bin.patch
Patch0050:	0050-grub-core-loader-i386-linux.c-allocate_pages-Fix-spe.patch
Patch0051:	0051-grub-core-commands-configfile.c-GRUB_MOD_INIT-Correc.patch
Patch0052:	0052-grub-core-Makefile.am-moddep.lst-Use-AWK-instead-of-.patch
Patch0053:	0053-Add-missing-ChangeLog.patch
Patch0054:	0054-Fix-ordering-and-tab-indentation-of-NetBSD-boot-menu.patch
Patch0055:	0055-grub-core-net-bootp.c-parse_dhcp_vendor-Fix-double-i.patch
Patch0056:	0056-include-grub-types.h-Fix-functionality-unaffecting-t.patch
Patch0057:	0057-Support-big-endian-UFS1.patch
Patch0058:	0058-Fix-big-endian-mtime.patch
Patch0059:	0059-grub-core-fs-ufs.c-grub_ufs_dir-Stop-if-direntlen-is.patch
Patch0060:	0060-util-getroot.c-convert_system_partition_to_system_di.patch
Patch0061:	0061-util-grub-mkfont.c-argp_parser-Fix-a-typo-which-prev.patch
Patch0062:	0062-grub-core-term-gfxterm.c-grub_virtual_screen_setup-G.patch
Patch0063:	0063-grub-core-gfxmenu-view.c-init_terminal-Avoid-making-.patch
Patch0064:	0064-grub-core-kern-ieee1275-init.c-grub_machine_get_boot.patch
Patch0065:	0065-util-grub-install.in-Remove-stale-TODO.patch
Patch0066:	0066-util-grub-install.in-Follow-the-symbolic-link-parame.patch
Patch0067:	0067-grub-core-disk-cryptodisk.c-grub_cmd_cryptomount-Str.patch
Patch0068:	0068-docs-grub.texi-Network-Update-instructions-on-genera.patch
Patch0069:	0069-util-grub.d-20_linux_xen.in-Addmissing-assignment-to.patch
Patch0070:	0070-Backport-gnulib-fixes-for-C11.-Fixes-Savannah-bug-37.patch
Patch0071:	0071-Apply-program-name-transformations-at-build-time-rat.patch
Patch0072:	0072-neater-gnulib-backport.patch
Patch0073:	0073-util-grub-mkconfig.in-Accept-GRUB_TERMINAL_OUTPUT-vg.patch
Patch0074:	0074-grub-core-bus-usb-ehci.c-grub_ehci_pci_iter-Remove-i.patch
Patch0075:	0075-Remove-several-trivially-unnecessary-uses-of-nested-.patch
Patch0076:	0076-docs-grub.texi-configfile-Explain-environment-variab.patch
Patch0077:	0077-Fix-failing-printf-test.patch
Patch0078:	0078-grub-core-tests-lib-test.c-grub_test_run-Return-non-.patch
Patch0079:	0079-docs-grub.texi-Invoking-grub-mount-New-section.patch
Patch0080:	0080-docs-grub.texi-Invoking-grub-mkrelpath-New-section.patch
Patch0081:	0081-grub-core-fs-iso9660.c-grub_iso9660_susp_iterate-Avo.patch
Patch0082:	0082-configure.ac-Extend-Wno-trampolines-to-host.patch
Patch0083:	0083-util-grub.d-10_kfreebsd.in-Fix-improper-references-t.patch
Patch0084:	0084-util-grub.d-10_kfreebsd.in-Correct-the-patch-to-zpoo.patch
Patch0085:	0085-grub-core-disk-diskfilter.c-grub_diskfilter_write-Ca.patch
Patch0086:	0086-grub-core-fs-nilfs2.c-grub_nilfs2_palloc_groups_per_.patch
Patch0087:	0087-grub-core-fs-ntfs.c-Eliminate-useless-divisions-in-f.patch
Patch0088:	0088-grub-core-fs-ext2.c-grub_ext2_read_block-Use-shifts-.patch
Patch0089:	0089-grub-core-fs-minix.c-grub_minix_read_file-Simplify-a.patch
Patch0090:	0090-docs-grub.texi-grub_cpu-New-subsection.patch
Patch0091:	0091-grub-core-io-bufio.c-grub_bufio_open-Use-grub_zalloc.patch
Patch0092:	0092-grub-core-kern-disk.c-grub_disk_write-Fix-sector-num.patch
Patch0093:	0093-Support-Apple-FAT-binaries-on-non-Apple-platforms.patch
Patch0094:	0094-grub-core-fs-ntfs.c-Ue-more-appropriate-types.patch
Patch0095:	0095-Import-gcrypt-public-key-cryptography-and-implement-.patch
Patch0096:	0096-Clean-up-dangling-references-to-grub-setup.patch
Patch0097:	0097-autogen.sh-Do-not-try-to-delete-nonexistant-files.patch
Patch0098:	0098-Remove-autogenerated-files-from-VCS.patch
Patch0099:	0099-grub-core-lib-libgcrypt_wrap-mem.c-_gcry_log_bug-Mak.patch
Patch0100:	0100-grub-core-lib-libgcrypt_wrap-mem.c-gcry_x-alloc-Make.patch
Patch0101:	0101-grub-core-commands-verify.c-Mark-messages-for-transl.patch
Patch0102:	0102-Remove-nested-functions-from-PCI-iterators.patch
Patch0103:	0103-util-grub-mkimage.c-generate_image-Fix-size-of-publi.patch
Patch0104:	0104-New-command-list_trusted.patch
Patch0105:	0105-Fix-compilation-with-older-compilers.patch
Patch0106:	0106-grub-core-kern-emu-hostdisk.c-read_device_map-Explic.patch
Patch0107:	0107-Remove-nested-functions-from-memory-map-iterators.patch
Patch0108:	0108-Remove-nested-functions-from-script-reading-and-pars.patch
Patch0109:	0109-grub-core-script-lexer.c-grub_script_lexer_init-Rena.patch
Patch0110:	0110-Improve-bidi-handling-in-entry-editor.patch
Patch0111:	0111-New-terminal-outputs-using-serial-morse-and-spkmodem.patch
Patch0112:	0112-Add-new-command-pcidump.patch
Patch0113:	0113-Rewrite-spkmodem-to-use-PIT-for-timing.-Double-the-s.patch
Patch0114:	0114-Add-license-header-to-spkmodem-recv.c.patch
Patch0115:	0115-Fix-typos-for-developer-and-development.patch
Patch0116:	0116-Remove-nested-functions-from-device-iterators.patch
Patch0117:	0117-Remove-nested-functions-from-ELF-iterators.patch
Patch0118:	0118-util-grub-script-check.c-main-Uniform-the-error-mess.patch
Patch0119:	0119-docs-grub.texi-Simple-configuration-Clarify-GRUB_HID.patch
Patch0120:	0120-Split-long-USB-transfers-into-short-ones.patch
Patch0121:	0121-include-grub-elf.h-Update-ARM-definitions-based-on-b.patch
Patch0122:	0122-conf-Makefile.common-Fix-autogen-rules-to-pass-defin.patch
Patch0123:	0123-grub-core-loader-i386-linux.c-grub_cmd_initrd-Don-t-.patch
Patch0124:	0124-util-grub-mkimage.c-main-Postpone-freeing-arguments..patch
Patch0125:	0125-docs-grub.texi-Multi-boot-manual-config-Fix-typo-for.patch
Patch0126:	0126-Remove-nested-functions-from-filesystem-directory-it.patch
Patch0127:	0127-grub-core-partmap-msdos.c-embed_signatures-Add-the-s.patch
Patch0128:	0128-Improve-spkmomdem-reliability-by-adding-a-separator-.patch
Patch0129:	0129-grub-core-commands-lsmmap.c-Fix-unused-variable-on-e.patch
Patch0130:	0130-grub-core-disk-arc-arcdisk.c-grub_arcdisk_iterate-Fi.patch
Patch0131:	0131-Fix-powerpc-and-sparc64-build-failures-caused-by-un-.patch
Patch0132:	0132-grub-core-commands-ls.c-grub_ls_print_devices-Add-mi.patch
Patch0133:	0133-Make-color-variables-global-instead-of-it-being-per-.patch
Patch0134:	0134-Improve-spkmomdem-reliability-by-adding-a-separator-.patch
Patch0135:	0135-grub-core-normal-term.c-print_ucs4_terminal-Don-t-ou.patch
Patch0136:	0136-Improve-spkmodem-reliability-by-adding-a-separator-b.patch
Patch0137:	0137-Remove-nested-functions-from-USB-iterators.patch
Patch0138:	0138-grub-core-font-font.c-blit_comb-do_blit-Make-static-.patch
Patch0139:	0139-include-grub-kernel.h-FOR_MODULES-Adjust-to-preserve.patch
Patch0140:	0140-grub-core-lib-libgcrypt_wrap-cipher_wrap.h-Include-s.patch
Patch0141:	0141-util-grub-reboot.in-usage-Document-the-need-for.patch
Patch0142:	0142-Improve-FreeDOS-direct-loading-support-compatibility.patch
Patch0143:	0143-grub-core-normal-menu_text.c-grub_menu_init_page-Fix.patch
Patch0144:	0144-util-grub-install.in-change-misleading-comment-about.patch
Patch0145:	0145-grub-core-fs-xfs.c-grub_xfs_read_block-Fix-computati.patch
Patch0146:	0146-grub-core-bus-usb-serial-common.c-grub_usbserial_att.patch
Patch0147:	0147-grub-core-bus-usb-usb.c-grub_usb_device_attach-Add-m.patch
Patch0148:	0148-grub-core-commands-lsacpi.c-Show-more-info.-Hide-som.patch
Patch0149:	0149-Missing-part-of-last-commit.patch
Patch0150:	0150-Implement-USBDebug-full-USB-stack-variant.patch
Patch0151:	0151-grub-core-fs-fshelp.c-find_file-Set-oldnode-to-zero-.patch
Patch0152:	0152-grub-core-disk-cryptodisk.c-grub_cryptodisk_scan_dev.patch
Patch0153:	0153-grub-core-commands-lsacpi.c-Fix-types-on-64-bit-plat.patch
Patch0154:	0154-Support-Openfirmware-disks-with-non-512B-sectors.patch
Patch0155:	0155-Implement-new-command-cmosdump.patch
Patch0156:	0156-grub-core-normal-misc.c-grub_normal_print_device_inf.patch
Patch0157:	0157-Makefile.util.def-Add-partmap-msdos.c-to-common-libr.patch
Patch0158:	0158-grub-core-normal-menu_entry.c-insert_string-fix-off-.patch
Patch0159:	0159-grub-core-normal-menu_entry.c-update_screen-remove.patch
Patch0160:	0160-grub-core-disk-efi-efidisk.c-grub_efidisk_get_device.patch
Patch0161:	0161-grub-core-partmap-msdos.c-grub_partition_msdos_itera.patch
Patch0162:	0162-Remove-nested-functions-from-disk-and-file-read-hook.patch
Patch0163:	0163-grub-core-loader-machoXX.c-Remove-nested-functions.patch
Patch0164:	0164-util-grub-fstest.c-Remove-nested-functions.patch
Patch0165:	0165-grub-core-commands-parttool.c-grub_cmd_parttool-Move.patch
Patch0166:	0166-grub-core-fs-iso9660.c-Remove-nested-functions.patch
Patch0167:	0167-grub-core-fs-minix.c-Remove-nested-functions.patch
Patch0168:	0168-grub-core-fs-jfs.c-Remove-nested-functions.patch
Patch0169:	0169-grub-core-lib-arg.c-grub_arg_show_help-Move-showargs.patch
Patch0170:	0170-grub-core-kern-i386-coreboot-mmap.c-grub_linuxbios_t.patch
Patch0171:	0171-Enable-linux16-on-non-BIOS-systems-for-i.a.-memtest.patch
Patch0172:	0172-grub-core-kern-main.c-grub_set_prefix_and_root-Strip.patch
Patch0173:	0173-grub-core-disk-efi-efidisk.c-Transform-iterate_child.patch
Patch0174:	0174-grub-core-loader-i386-pc-linux.c-grub_cmd_linux-Fix-.patch
Patch0175:	0175-Remove-nested-functions-from-videoinfo-iterators.patch
Patch0176:	0176-grub-core-gentrigtables.c-Make-tables-const.patch
Patch0177:	0177-grub-core-kern-emu-hostdisk.c-read_device_map-Remove.patch
Patch0178:	0178-util-grub-editenv.c-list_variables-Move-print_var-ou.patch
Patch0179:	0179-grub-core-fs-hfsplus.c-grub_hfsplus_btree_iterate_no.patch
Patch0180:	0180-grub-core-fs-hfs.c-Remove-nested-functions.patch
Patch0181:	0181-grub-core-commands-loadenv.c-grub_cmd_list_env-Move-.patch
Patch0182:	0182-grub-core-normal-charset.c-grub_bidi_logical_to_visu.patch
Patch0183:	0183-grub-core-script-execute.c-gettext_append-Remove-nes.patch
Patch0184:	0184-grub-core-lib-ia64-longjmp.S-Fix-the-name-of-longjmp.patch
Patch0185:	0185-Make-elfload-not-use-hooks.-Opt-for-flags-and-iterat.patch
Patch0186:	0186-grub-core-kern-term.c-grub_term_normal_color.patch
Patch0187:	0187-Move-to-more-hookless-approach-in-IEEE1275-devices-h.patch
Patch0188:	0188-include-grub-mips-loongson-cmos.h-Fix-high-CMOS-addr.patch
Patch0189:	0189-include-grub-cmos.h-Handle-high-CMOS-addresses-on-sp.patch
Patch0190:	0190-grub-core-disk-ieee1275-nand.c-Fix-compilation-on.patch
Patch0191:	0191-grub-core-kern-env.c-include-grub-env.h-Change-itera.patch
Patch0192:	0192-grub-core-commands-regexp.c-set_matches-Move-setvar-.patch
Patch0193:	0193-grub-core-script-execute.c-grub_script_arglist_to_ar.patch
Patch0194:	0194-Remove-all-trampoline-support.-Add-Wtrampolines-when.patch
Patch0195:	0195-grub-core-term-terminfo.c-grub_terminfo_cls-Issue-an.patch
Patch0196:	0196-Lift-up-core-size-limits-on-some-platforms.-Fix-pote.patch
Patch0197:	0197-grub-core-normal-crypto.c-read_crypto_list-Fix-incor.patch
Patch0198:	0198-grub-core-commands-acpi.c-grub_acpi_create_ebda-Don-.patch
Patch0199:	0199-grub-core-fs-iso9660.c-add_part-Remove-always_inline.patch
Patch0200:	0200-grub-core-fs-fshelp.c-grub_fshelp_log2blksize-Remove.patch
Patch0201:	0201-Avoid-costly-64-bit-division-in-grub_get_time_ms-on-.patch
Patch0202:	0202-grub-core-fs-hfs.c-grub_hfs_read_file-Avoid-divmod64.patch
Patch0203:	0203-Adjust-types-in-gdb-module-to-have-intended-unsigned.patch
Patch0204:	0204-grub-core-video-i386-pc-vbe.c.patch
Patch0205:	0205-include-grub-datetime.h-grub_datetime2unixtime-Fix-u.patch
Patch0206:	0206-grub-core-loader-i386-pc-plan9.c-fill_disk-Fix-types.patch
Patch0207:	0207-grub-core-commands-verify.c-grub_verify_signature-Us.patch
Patch0208:	0208-grub-core-lib-arg.c-grub_arg_list_alloc-Use-shifts-r.patch
Patch0209:	0209-grub-core-loader-i386-bsdXX.c-grub_openbsd_find_ramd.patch
Patch0210:	0210-Resend-a-packet-if-we-got-the-wrong-buffer-in-status.patch
Patch0211:	0211-Better-estimate-the-maximum-USB-transfer-size.patch
Patch0212:	0212-remove-get_endpoint_descriptor-and-change-all-functi.patch
Patch0213:	0213-Implement-boot-time-analysis-framework.patch
Patch0214:	0214-Fix-USB-devices-not-being-detected-when-requested.patch
Patch0215:	0215-Initialize-USB-ports-in-parallel-to-speed-up-boot.patch
Patch0216:	0216-include-grub-boottime.h-Add-missing-file.patch
Patch0217:	0217-Fix-a-conflict-between-ports-structures-with-2-contr.patch
Patch0218:	0218-New-commands-cbmemc-lscoreboot-coreboot_boottime-to-.patch
Patch0219:	0219-grub-core-commands-boottime.c-Fix-copyright-header.patch
Patch0220:	0220-Slight-improve-in-USB-related-boot-time-checkpoints.patch
Patch0221:	0221-grub-core-commands-verify.c-hashes-Add-several-hashe.patch
Patch0222:	0222-po-POTFILES.in-Regenerate.patch
Patch0223:	0223-grub-core-commands-i386-coreboot-cbls.c-Fix-typos-an.patch
Patch0224:	0224-Add-ability-to-generate-newc-additions-on-runtime.patch
Patch0225:	0225-grub-core-fs-zfs-zfs.c-Fix-incorrect-handling-of-spe.patch
Patch0226:	0226-grub-core-term-at_keyboard.c-Increase-robustness-on-.patch
Patch0227:	0227-Add-new-proc-filesystem-framework-and-put-luks_scrip.patch
Patch0228:	0228-grub-core-Makefile.core.def-vbe-Disable-on-coreboot-.patch
Patch0229:	0229-util-grub-mkconfig_lib.in-prepare_grub_to_access_dev.patch
Patch0230:	0230-grub-core-Makefile.core.def-vga-Disable-on-coreboot-.patch
Patch0231:	0231-util-grub.d-20_linux_xen.in-Automatically-add-no-rea.patch
Patch0232:	0232-Replace-the-region-at-0-from-coreboot-tables-to-avai.patch
Patch0233:	0233-grub-core-normal-menu.c-Wait-if-there-were-errors-sh.patch
Patch0234:	0234-grub-core-disk-ahci.c-Give-more-time-for-AHCI-reques.patch
Patch0235:	0235-grub-core-gfxmenu-font.c-grub_font_get_string_width-.patch
Patch0236:	0236-grub-core-commands-acpihalt.c-skip_ext_op-Add-suppor.patch
Patch0237:	0237-grub-core-kern-efi-mm.c-grub_efi_finish_boot_service.patch
Patch0238:	0238-grub-core-commands-verify.c-Fix-hash-algorithms-valu.patch
Patch0239:	0239-INSTALL-Mention-xorriso-requirement.patch
Patch0240:	0240-grub-core-partmap-apple.c-apple_partition_map_iterat.patch
Patch0241:	0241-grub-core-gfxmenu-gui_circular_progress.c-Fix-off-by.patch
Patch0242:	0242-grub-core-gfxmenu-view.c-Fix-off-by-one-error.patch
Patch0243:	0243-grub-core-gfxmenu-gui_circular_progress.c-Take-both-.patch
Patch0244:	0244-grub-core-gfxmenu-gui_progress_bar.c-Handle-padding-.patch
Patch0245:	0245-include-grub-elf.h-Add-missing-ARM-relocation-codes-.patch
Patch0246:	0246-util-grub-mount.c-fuse_init-Return-error-if-fuse_mai.patch
Patch0247:	0247-Fix-screen-corruption-in-menu-entry-editor-and-simpl.patch
Patch0248:	0248-grub-core-term-i386-pc-console.c-grub_console_getwh-.patch
Patch0249:	0249-grub-core-commands-verify.c-Save-verified-file-to-av.patch
Patch0250:	0250-grub-core-lib-posix_wrap-locale.h-GRUB_UTIL-Include-.patch
Patch0251:	0251-util-grub-setup.c-setup-Handle-some-corner-cases.patch
Patch0252:	0252-grub-core-bus-usb-usbtrans.c-grub_usb_bulk_readwrite.patch
Patch0253:	0253-Use-TSC-as-a-possible-time-source-on-i386-ieee1275.patch
Patch0254:	0254-grub-core-disk-efi-efidisk.c-Handle-partitions-on-no.patch
Patch0255:	0255-Unify-file-copying-setup-across-different-install-sc.patch
Patch0256:	0256-util-grub-mkimage.c-Introduce-new-define-EFI32_HEADE.patch
Patch0257:	0257-docs-grub.texi-Document-menuentry-id-option.patch
Patch0258:	0258-docs-grub.texi-Document-more-user-commands.patch
Patch0259:	0259-Move-GRUB_CHAR_BIT-to-types.h.patch
Patch0260:	0260-include-grub-bsdlabel.h-Use-enums.patch
Patch0261:	0261-grub-core-commands-verify.c-Use-GRUB_CHAR_BIT.patch
Patch0262:	0262-Add-new-defines-GRUB_RSDP_SIGNATURE_SIZE-and-GRUB_RS.patch
Patch0263:	0263-Replace-8-with-GRUB_CHAR_BIT-in-several-places-when-.patch
Patch0264:	0264-grub-core-commands-acpi.c-Use-sizeof-rather-than-har.patch
Patch0265:	0265-util-grub-mkfont.c-Prefer-enum-to-define.patch
Patch0266:	0266-Use-GRUB_PROPERLY_ALIGNED_ARRAY-in-grub-core-disk-cr.patch
Patch0267:	0267-util-grub.d-30_os-prober.in-Support-btrrfs-linux-pro.patch
Patch0268:	0268-util-grub-install_header-Use-PACKAGE-.mo-in-message-.patch
Patch0269:	0269-conf-Makefile.extra-dist-EXTRA_DIST-Add.patch
Patch0270:	0270-grub-core-normal-term.c-Few-more-fixes-for-menu-entr.patch
Patch0271:	0271-grub-core-normal-term.c-Few-more-fixes-for-menu-entr.patch
Patch0272:	0272-docs-grub-dev.texi-Move-itemize-after-subsection-to-.patch
Patch0273:	0273-grub-core-term-i386-pc-console.c-Fix-cursor-moving-a.patch
Patch0274:	0274-grub-core-Makefile.core.def-Add-kern-elfXX.c-to-elf-.patch
Patch0275:	0275-Fix-ia64-efi-image-generation-on-big-endian-machines.patch
Patch0276:	0276-autogen.sh-Use-h-not-f-to-test-for-existence-of-symb.patch
Patch0277:	0277-Fix-missing-PVs-if-they-don-t-contain-interesting-LV.patch
Patch0278:	0278-util-grub.d-30_os-prober.in-Add-onstr-to-entries-for.patch
Patch0279:	0279-Use-ACPI-shutdown-intests-as-traditional-port-was-re.patch
Patch0280:	0280-Import-new-gnulib.patch
Patch0281:	0281-docs-grub.texi-Fix-description-of-GRUB_CMDLINE_XEN-a.patch
Patch0282:	0282-Merge-powerpc-grub-mkrescue-flavour-with-common.-Use.patch
Patch0283:	0283-Support-i386-ieee1275-grub-mkrescue-and-make-check-o.patch
Patch0284:	0284-tests-partmap_test.in-Fix-missing-qemudisk-setting.patch
Patch0285:	0285-tests-grub_cmd_date.in-New-test-for-datetime.patch
Patch0286:	0286-docs-grub.texi-Update-coreboot-status-info.patch
Patch0287:	0287-Turn-off-QEMU-ACPI-way-since-new-releases-don-t-have.patch
Patch0288:	0288-tests-util-grub-shell.in-Fix-it-on-powerpc.patch
Patch0289:	0289-Disable-partmap-check-on-i386-ieee1275-due-to-openfi.patch
Patch0290:	0290-grub-core-net-drivers-ieee1275-ofnet.c-Don-t-attempt.patch
Patch0291:	0291-grub-core-net-http.c-Fix-bad-free.patch
Patch0292:	0292-Fix-handling-of-split-transfers.patch
Patch0293:	0293-grub-core-bus-usb-ehci.c-grub_ehci_fini_hw-Ignore-er.patch
Patch0294:	0294-util-grub-mkimage.c-Document-memdisk-implying-prefix.patch
Patch0295:	0295-Handle-Japanese-special-keys.patch
Patch0296:	0296-Replace-stpcpy-with-grub_stpcpy-in-tools.patch
Patch0297:	0297-Better-support-Apple-Intel-Macs-on-CD.patch
Patch0298:	0298-util-grub-mkrescue.in-Fix-wrong-architecture-for-ppc.patch
Patch0299:	0299-docs-man-grub-glue-efi.h2m-Add-missing-file.patch
Patch0300:	0300-Fix-memory-leaks-in-ofnet.patch
Patch0301:	0301-grub-core-kern-ieee1275-cmain.c-grub_ieee1275_find_o.patch
Patch0302:	0302-grub-core-disk-ieee1275-ofdisk.c-Iterate-over-bootpa.patch
Patch0303:	0303-Allow-IEEE1275-ports-on-path-even-if-it-wasn-t-detec.patch
Patch0304:	0304-Support-mkrescue-on-sparc64.patch
Patch0305:	0305-Support-grub-shell-on-sparc64.patch
Patch0306:	0306-tests-partmap_test.in-Skip-on-sparc64.patch
Patch0307:	0307-tests-grub_cmd_date.in-Add-missing-exit-1.patch
Patch0308:	0308-Move-GRUB-out-of-system-area-when-using-xorriso-1.2..patch
Patch0309:	0309-grub-core-loader-i386-linux.c-Remove-useless-leftove.patch
Patch0310:	0310-docs-grub-dev.texi-Rearrange-menu-to-match-the-secti.patch
Patch0311:	0311-Add-option-to-compress-files-on-install-image-creati.patch
Patch0312:	0312-grub-core-lib-posix_wrap-sys-types.h-Make-WORDS_BIGE.patch
Patch0313:	0313-grub-core-disk-ieee1275-ofdisk.c-Fix-CD-ROM-and-boot.patch
Patch0314:	0314-grub-core-kern-ieee1275-openfw.c-grub_ieee1275_deval.patch
Patch0315:	0315-tests-grub_script_expansion.in-Use-fixed-string-grep.patch
Patch0316:	0316-tests-grub_cmd_date.in-Skip-on-sparc64.patch
Patch0317:	0317-Fix-DMRAID-partition-handling.patch
Patch0318:	0318-grub-core-disk-efi-efidisk.c-Limit-disk-read-or-writ.patch
Patch0319:	0319-autogen.sh-Use-f-in-addition-for-h-when-checking-fil.patch
Patch0320:	0320-grub-core-disk-efi-efidisk.c-Really-limit-transfer-c.patch
Patch0321:	0321-build-aux-snippet-Add-missing-gnulib-files.patch
Patch0322:	0322-grub-core-disk-efi-efidisk.c-Detect-floppies-by-ACPI.patch
Patch0323:	0323-util-grub-mkrescue.in-Add-GPT-for-EFI-boot.patch
Patch0324:	0324-Add-support-for-pseries-and-other-bootinfo-machines-.patch
Patch0325:	0325-util-grub.d-30_os-prober.in-Add-onstr-to-linux-entri.patch
Patch0326:	0326-grub-core-kern-elfXX.c-grub_elfXX_load-Handle.patch
Patch0327:	0327-grub-core-commands-videotest.c-grub_cmd_videotest-Fi.patch
Patch0328:	0328-grub-core-kern-ieee1275-cmain.c-grub_ieee1275_find_o.patch
Patch0329:	0329-grub-core-kern-ieee1275-init.c-grub_claim_heap-Impro.patch
Patch0330:	0330-grub-core-lib-efi-relocator.c-grub_relocator_firmwar.patch
Patch0331:	0331-grub-core-Makefile.core.def-legacycfg-Enable-on-EFI.patch
Patch0332:	0332-grub-core-kern-mm.c-grub_mm_init_region-Fix-conditio.patch
Patch0333:	0333-Support-coreboot-framebuffer.patch
Patch0334:	0334-grub-core-disk-arc-arcdisk.c-grub_arcdisk_iterate_it.patch
Patch0335:	0335-Move-mips-arc-link-address.-Previous-link-address-wa.patch
Patch0336:	0336-grub-core-kern-dl.c-grub_dl_resolve_symbols-Handle-m.patch
Patch0337:	0337-util-grub-mkrescue.in-Add-mips-arc-support.patch
Patch0338:	0338-Add-missing-video-ids-to-coreboot-and-ieee1275-video.patch
Patch0339:	0339-grub-core-disk-ata.c-grub_ata_real_open-Use-grub_err.patch
Patch0340:	0340-grub-core-loader-i386-linux.c-grub_linux_boot-Defaul.patch
Patch0341:	0341-grub-core-normal-menu_text.c-print_entry-Put-an-aste.patch
Patch0342:	0342-util-grub-install.in-Fix-target-fo-qemu_mips.patch
Patch0343:	0343-grub-core-term-arc-console.c-Assume-that-console-is-.patch
Patch0344:	0344-util-grub-mkrescue.in-Alias-sashARCS-as-sash.patch
Patch0345:	0345-Make-check-work-on-mips-arc.patch
Patch0346:	0346-grub-core-term-ieee1275-console.c-grub_console_dimen.patch
Patch0347:	0347-util-grub-mkrescue.in-Move-all-files-that-don-t-have.patch
Patch0348:	0348-util-grub-mkrescue.in-Fix-loongson-filename.patch
Patch0349:	0349-tests-partmap_test.in-Add-missing-double-semicolon.patch
Patch0350:	0350-grub-core-boot-powerpc-bootinfo.txt.in-Missing-updat.patch
Patch0351:	0351-Add-serial-on-ARC-platform.patch
Patch0352:	0352-Enable-mipsel-arc.patch
Patch0353:	0353-configure.ac-Fix-loongson-conditional.patch
Patch0354:	0354-util-grub-mkrescue.in-Rename-i386-ieee1275-core-imag.patch
Patch0355:	0355-Add-test-to-check-that-different-boot-mediums-work.patch
Patch0356:	0356-tests-pseries_test.in-New-test.patch
Patch0357:	0357-util-getroot.c-exec_pipe-Put-proper-if-s-so-that-its.patch
Patch0358:	0358-grub-core-Makefile.core.def-Fix-grub-emu-and-grub-em.patch
Patch0359:	0359-Replace-libcurses-with-our-own-vt100-handling-for-th.patch
Patch0360:	0360-Make-make-check-work-on-emu.patch
Patch0361:	0361-Fix-pseries-test.patch
Patch0362:	0362-Improve-AHCI-detection-and-command-issuing.patch
Patch0363:	0363-Implement-grub_machine_get_bootlocation-for-ARC.patch
Patch0364:	0364-Core-compression-test.patch
Patch0365:	0365-grub-core-loader-multiboot_mbi2.c-grub_multiboot_loa.patch
Patch0366:	0366-grub-core-disk-ahci.c-grub_ahci_pciinit-Fix-handling.patch
Patch0367:	0367-util-ieee1275-ofpath.c-of_path_of_scsi-Fix-path-outp.patch
Patch0368:	0368-grub-core-term-ns8250.c-Systematically-probe-ports-b.patch
Patch0369:	0369-missing-file.patch
Patch0370:	0370-include-grub-macho.h-Set-GRUB_MACHO_FAT_EFI_MAGIC-as.patch
Patch0371:	0371-grub-core-term-morse.c-Macroify-dih-and-dah.patch
Patch0372:	0372-Move-directory-override-directorry-to-grub-install_h.patch
Patch0373:	0373-Remove-POTFILES.in-and-regenerate-it-in-autogen.sh.patch
Patch0374:	0374-INSTALL-Document-linguas.sh.patch
Patch0375:	0375-grub-core-commands-probe.c-Add-missing-grub_device_c.patch
Patch0376:	0376-grub-core-kern-file.c-Use-const-char-rather-than-cas.patch
Patch0377:	0377-include-grub-efi-api.h-GRUB_EFI_DEVICE_PATH_LENGTH-U.patch
Patch0378:	0378-grub-core-disk-ahci.c-Fix-compilation-for-amd64-form.patch
Patch0379:	0379-grub-core-io-lzopio.c-Use-GRUB_PROPERLY_ALIGNED_ARRA.patch
Patch0380:	0380-New-command-nativedisk.patch
Patch0381:	0381-grub-core-commands-nativedisk.c-Ignore-unknown-files.patch
Patch0382:	0382-docs-grub.texi-Add-a-comment-about-usefullness-of-na.patch
Patch0383:	0383-grub-core-lib-arg.c-grub_arg_show_help-Fix-a-NULL-po.patch
Patch0384:	0384-grub-core-kern-mips-arc-init.c-Fix-prefix-detection.patch
Patch0385:	0385-include-grub-list.h-FOR_LIST_ELEMENTS_SAFE-Fix-a-NUL.patch
Patch0386:	0386-grub-core-script-execute.c-grub_script_arglist_to_ar.patch
Patch0387:	0387-grub-core-bus-usb-uhci.c-Fix-DMA-handling-and-enable.patch
Patch0388:	0388-grub-core-commands-nativedisk.c-Customize-the-list-o.patch
Patch0389:	0389-Enforce-disabling-of-firmware-disk-drivers-when-nati.patch
Patch0390:	0390-Add-few-new-tests.patch
Patch0391:	0391-Unify-more-code-in-grub-install_header.patch
Patch0392:	0392-grub-core-gfxmenu-gui_list.c-Refresh-first_shown_ent.patch
Patch0393:	0393-Make-PCI-init-in-i386-qemu-port-more-robust.patch
Patch0394:	0394-grub-core-gfxmenu-circular_progress.c-Set-start_angl.patch
Patch0395:	0395-configure.ac-Use-mcmodel-large-on-x86_64-emu-as-well.patch
Patch0396:	0396-grub-core-partmap-amiga.c-Fix-size-of-checksummed-bl.patch
Patch0397:	0397-grub-core-kern-mips-loongson-init.c-Support-halt-for.patch
Patch0398:	0398-include-grub-arc-arc.h-Account-for-missing-other-per.patch
Patch0399:	0399-Add-few-more-tests.patch
Patch0400:	0400-grub-core-commands-videotest.c-Reduce-flickering-and.patch
Patch0401:	0401-First-automated-video-test-running-videotest-and-com.patch
Patch0402:	0402-grub-core-loader-i386-linux.c-grub_linux_setup_video.patch
Patch0403:	0403-grub-core-tests-videotest_checksum.c-videotest_check.patch
Patch0404:	0404-Add-missing-exports-on-mips.patch
Patch0405:	0405-Several-fixes-to-ieee1275-and-big-endian-video.patch
Patch0406:	0406-grub-core-normal-term.c-print_ucs4_real-Fix-startwid.patch
Patch0407:	0407-grub-core-gfxmenu-view.c-grub_gfxmenu_view_new-Clear.patch
Patch0408:	0408-include-grub-gui.h-grub_gfxmenu_timeout_unregister-F.patch
Patch0409:	0409-grub-core-video-fb-fbblit.c-grub_video_fbblit_blend_.patch
Patch0410:	0410-grub-core-gfxmenu-gfxmenu.c-grub_gfxmenu_try-Allow-s.patch
Patch0411:	0411-New-series-of-tests-for-gfxterm-and-gfxmenu.patch
Patch0412:	0412-grub-core-tests-video_checksum.c-Don-t-set-GENERATE_.patch
Patch0413:	0413-Rename-grub-core-tests-checksums.c-into-grub-core-te.patch
Patch0414:	0414-grub-core-font-font.c-grub_font_construct_glyph-Fix-.patch
Patch0415:	0415-Fix-test-a-and-o-precedence.patch
Patch0416:	0416-grub-core-gettext-gettext.c-Try-lang.gmo-as-well.patch
Patch0417:	0417-grub-core-normal-menu.c-run_menu-Fix-timeout-referen.patch
Patch0418:	0418-Fix-several-memory-leaks.patch
Patch0419:	0419-grub-core-normal-main.c-Fix-freed-memory-dereference.patch
Patch0420:	0420-grub-core-normal-menu_text.c-menu_clear_timeout-Clea.patch
Patch0421:	0421-grub-core-tests-lib-functional_test.c-Don-t-stop-on-.patch
Patch0422:	0422-Speed-up-gfxterm-by-saving-intermediate-results-in-i.patch
Patch0423:	0423-More-video-checks.patch
Patch0424:	0424-Speed-up-gfxterm-by-slightly-agglomerating-mallocs.patch
Patch0425:	0425-Agglomerate-more-mallocs-to-speed-up-gfxterm.patch
Patch0426:	0426-Factor-out-human-size-printing.patch
Patch0427:	0427-grub-core-commands-testspeed.c-New-command-testspeed.patch
Patch0428:	0428-Reimplement-grub-reboot-to-not-depend-on-saved_entry.patch
Patch0429:	0429-grub-core-font-font.c-Use-grub_dprintf-for-debug-sta.patch
Patch0430:	0430-tests-priority_queue_unit_test.cc-New-test.patch
Patch0431:	0431-grub-core-video-readers-jpeg.c-Use-grub_dprintf-for-.patch
Patch0432:	0432-grub-core-loader-linux.c-Use-grub_dprintf-for-debug-.patch
Patch0433:	0433-Mark-few-forgotten-strings-for-translation.patch
Patch0434:	0434-Simplify-few-strings.patch
Patch0435:	0435-autogen.sh-Exclude-unused-libgcrypt-files-from-trans.patch
Patch0436:	0436-tests-gettext_strings_test.in-A-test-to-check-for-st.patch
Patch0437:	0437-New-variables-net_default_-to-determine-MAC-IP-of-de.patch
Patch0438:	0438-grub-core-tests-setjmp_test.c-New-test.patch
Patch0439:	0439-Menu-color-test.patch
Patch0440:	0440-grub-core-commands-videoinfo.c-Use-paletted-rather-t.patch
Patch0441:	0441-Compressed-HFS-support.patch
#Patch0442:	0442-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0443:	0443-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0444:	0444-Add-fw_path-variable-revised.patch
Patch0445:	0445-Don-t-set-boot-device-on-ppc-ieee1275.patch
Patch0446:	0446-Add-support-for-linuxefi.patch
Patch0447:	0447-Add-support-for-crappy-cd-craparino.patch
Patch0448:	0448-Use-linuxefi-and-initrdefi-where-appropriate.patch
Patch0449:	0449-Don-t-allow-insmod-when-secure-boot-is-enabled.patch
Patch0450:	0450-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0451:	0451-Fix-crash-on-http.patch
Patch0452:	0452-Issue-separate-DNS-queries-for-ipv4-and-ipv6.patch
Patch0453:	0453-IBM-client-architecture-CAS-reboot-support.patch
Patch0454:	0454-Add-vlan-tag-support.patch
Patch0455:	0455-Add-X-option-to-printf-functions.patch
Patch0456:	0456-DHCP-client-ID-and-UUID-options-added.patch
Patch0457:	0457-Search-for-specific-config-file-for-netboot.patch
Patch0458:	0458-Add-bootpath-device-to-the-list.patch
Patch0459:	0459-add-GRUB_DISABLE_SUBMENU-option.patch
Patch0460:	0460-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0461:	0461-Move-bash-completion-script-922997.patch
Patch0462:	0462-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0463:	0463-grub-core-term-efi-console.c-Fix-compile-error.patch
Patch0464:	0464-configure.ac-Don-t-use-extended-registers-on-x86_64.patch
Patch0465:	0465-configure.ac-Don-t-disable-extended-registers-on-emu.patch
Patch0466:	0466-conf-Makefile.common-Poison-float-and-double-on-non-.patch
Patch0467:	0467-Progressively-skip-menu-elements-on-small-terminals-.patch
#Patch0468:	0468-Don-t-write-messages-to-the-screen.patch
#Patch0469:	0469-Don-t-print-GNU-GRUB-header.patch
Patch0470:	0470-Don-t-draw-a-border-around-the-menu.patch
Patch0471:	0471-Don-t-add-to-highlighted-row.patch
Patch0472:	0472-Don-t-add-to-highlighted-row.patch
Patch0473:	0473-Use-the-standard-margin-for-the-timeout-string.patch
Patch0474:	0474-Message-string-cleanups.patch
Patch0475:	0475-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0476:	0476-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0477:	0477-Indent-menu-entries.patch
Patch0478:	0478-Fix-margins.patch
Patch0479:	0479-Add-support-for-UEFI-operating-systems-returned-by-o.patch
Patch0480:	0480-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0481:	0481-Revert-Add-bootpath-device-to-the-list-967862.patch
Patch0482:	0482-Fix-net_bootp-cmd-crash-when-there-isn-t-network-car.patch
Patch0483:	0483-Initialize-grub_file_filters_-all-enabled.patch
Patch0484:	0484-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch

# clean up after P0208
Patch999:	grub-2.00-remove-dropped-m4-macros-from-aclocal-as-well.patch

# our patches
Patch1000:	grub2-locales.patch
Patch1001:	grub2-00_header.patch
Patch1002:	grub2-custom-color.patch
Patch1004:	grub2-read-cfg.patch
Patch1005:	grub2-symlink-is-garbage.patch
#Patch1007:	grub2-10_linux.patch
Patch1008:	grub2-theme-not_selected_item_box.patch
Patch1011:	grub-2.00-fix-dejavu-font.patch
Patch1018:	grub-2.00-lua-undef-double-poision-override.patch
Patch1019:	grub-2.00-dont-print-stuff-while-grub-is-loading.patch
Patch1020:	grub-2.00-add-recovery_option.patch
Patch1021:      grub-2.00-custom-vendor-config.patch

# openSuSE patches
Patch1100:	grub2-fix-locale-en.mo.gz-not-found-error-message.patch
Patch1101:	grub2-fix-error-terminal-gfxterm-isn-t-found.patch
Patch1104:	grub2-install-opt-skip-fs-probe.patch
Patch1105:	grub2-iterate-and-hook-for-extended-partition.patch
Patch1109:	grub2-fix-menu-in-xen-host-server.patch
Patch1110:	grub2-efidisk-ahci-workaround.patch
Patch1111:	grub2-secureboot-chainloader.patch
Patch1112:	grub2-pass-correct-root-for-nfsroot.patch
Patch1113:	grub2-secureboot-use-linuxefi-on-uefi-in-os-prober.patch
Patch1115:	30_os-prober_UEFI_support.patch	
Patch1116:	grub2-2.00-class-via-os-prober.patch
Patch1117:	grub-2.00-autoreconf-sucks.patch

BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
#BuildRequires:	fonts-ttf-unifont
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
%setup -qn grub-%{version} -a12 -a14 -a15
#  needs to be fixed..
#apply_patches

%{lua: for i, p in ipairs(patches) do     print("patch -p1 -i ".. rpm.expand(p .. " --fuzz=%{_default_patch_fuzz} %{_default_patch_flags} -b --suffix ")..string.format(".%04d~",i) .. "\n") end}

cp %{SOURCE10} .

perl -pi -e 's/(\@image\{font_char_metrics,,,,)\.(png\})/$1$2/;' \
	docs/grub-dev.texi

perl -pi -e "s|(^FONT_SOURCE=)|\$1%{SOURCE6}|;" configure configure.ac

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
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-sparc64-setup
%{_sbindir}/update-grub2
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
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%endif
%{_bindir}/%{name}-script-check
%{_datadir}/bash-completion/completions/grub
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%dir /boot/%{name}
%dir /boot/%{name}/themes/
#%dir /boot/%{name}/themes/system
#%exclude /boot/%{name}/themes/system/*
#%exclude %{_datadir}/grub/themes/
%{_infodir}/grub*.info*
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man8/%{name}-*.8*
