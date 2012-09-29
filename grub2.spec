%define		libdir32	%{_exec_prefix}/lib
%define		unifont		%(echo %{_datadir}/fonts/TTF/unifont/unifont-*.ttf)

%bcond_with	talpo

Name:           grub2
Version:        2.00
Release:        1
Summary:        GNU GRUB is a Multiboot boot loader

Group:          System/Kernel and hardware
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Source0:        http://ftp.gnu.org/pub/gnu/grub/grub-%{version}.tar.xz
Source1:        90_persistent
Source2:        grub.default

# basic test
Source3:	theme.txt
Source4:	background.jpg
Source5:	star_w.jpg

Source6:	grub.melt

# documentation and simple test script for testing grub2 themes
Source7:	mandriva-grub2-theme-test.sh
# www.4shared.com/archive/lFCl6wxL/grub_guidetar.html
Source8:	grub_guide.tar.gz
Source9:	grub-lua-rev24.tar.xz

Source10:	%{name}.rpmlintrc

BuildRequires:	bison
BuildRequires:  flex
BuildRequires:	fonts-ttf-unifont
BuildRequires:	freetype2-devel
BuildRequires:	glibc-static-devel
BuildRequires:	help2man
BuildRequires:	liblzma-devel
BuildRequires:	liblzo-devel
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig(devmapper)
#BuildRequires:	texinfo
BuildRequires:	texlive
%if %{with talpo}
BuildRequires:	talpo
%endif
BuildRequires:	autogen

Requires(preun):drakxtools-backend
Requires(post): drakxtools-backend

Requires:	xorriso

%description
GNU GRUB is a Multiboot boot loader. It was derived from GRUB, the
GRand Unified Bootloader, which was originally designed and implemented
by Erich Stefan Boleyn.

Briefly, a boot loader is the first software program that runs when a
computer starts. It is responsible for loading and transferring control
to the operating system kernel software (such as the Hurd or Linux).
The kernel, in turn, initializes the rest of the operating system (e.g. GNU).

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
%prep
%setup -q -n grub-%{version} -a9
perl -pi -e 's/(\@image\{font_char_metrics,,,,)\.(png\})/$1$2/;'	\
	docs/grub-dev.texi

perl -pi -e "s|(^FONT_SOURCE=)|\$1%{unifont}|;" configure configure.ac

sed -ri -e 's/-g"/"/g' -e "s/-Werror//g" configure.ac

perl -pi -e 's/-Werror//;' grub-core/Makefile.am
mkdir grub-extras
mv lua grub-extras
export GRUB_CONTRIB=./grub-extras
./autogen.sh

#-----------------------------------------------------------------------
%build
export GRUB_CONTRIB=./grub-extras

#(proyvind): debugedit will fail on some binaries if linked using gold
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
%configure						\
%if %{with talpo}
	CC=talpo					\
	CFLAGS=-fplugin-arg-melt-option=talpo-arg-file:%{SOURCE6} \
%else
	CFLAGS=""                                       \
%endif
	TARGET_LDFLAGS=-static				\
	--with-platform=pc				\
    %ifarch x86_64
	--enable-efiemu					\
    %endif
	--with-grubdir=%{name}				\
	--program-transform-name=s,grub,%{name},	\
	--libdir=%{libdir32}				\
	--libexecdir=%{libdir32}			\
	--disable-werror				\
	--enable-device-mapper
%make all

make html pdf

#-----------------------------------------------------------------------
%install
%makeinstall_std
%makeinstall_std -C docs install-pdf install-html
mv -f %{buildroot}%{_docdir}/grub %{buildroot}%{_docdir}/%{name}
install -m644 COPYING INSTALL NEWS README THANKS TODO ChangeLog	\
	%{buildroot}%{_docdir}/%{name}

# (bor) grub.info is harcoded in sources
mv %{buildroot}%{_infodir}/grub.info %{buildroot}%{_infodir}/grub2.info

# Script that makes part of grub.cfg persist across updates
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/grub.d/

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
install -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/default/grub

# Install filetriggers to update grub.cfg on kernel add or remove
install -d %{buildroot}%{_filetriggers_dir}
pushd %{buildroot}%{_filetriggers_dir} && {
	cat > %{name}.filter << EOF
^./boot/vmlinuz-
EOF
	cat > %{name}.script << EOF
#!/bin/sh
%{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg
EOF
	chmod 0755 %{name}.script
	popd
}

%__mkdir_p %{buildroot}/boot/grub2/themes/mandriva
install -m644 %{SOURCE3} %{SOURCE4} %{SOURCE5}		\
    %{buildroot}/boot/grub2/themes/mandriva

%find_lang grub

%post
exec >/dev/null 2>&1
# Create device.map or reuse one from GRUB Legacy
cp -u /boot/grub/device.map /boot/%{name}/device.map 2>/dev/null ||
	%{_sbindir}/%{name}-mkdevicemap
# Determine the partition with /boot
BOOT_PARTITION=$(df -h /boot |(read; awk '{print $1; exit}'))
# (Re-)Generate core.img, but don't let it be installed in boot sector
%{_sbindir}/%{name}-install --grub-setup=/bin/true $BOOT_PARTITION
# Generate grub.cfg and add GRUB2 chainloader to menu on initial install
if [ $1 = 1 ]; then
    %{_sbindir}/bootloader-config --action add-entry --image /boot/%{name}/core.img --label 'Chainload GRUB2'
    %{_sbindir}/%{name}-mkconfig -o /boot/%{name}/grub.cfg
fi

%preun
exec >/dev/null
if [ $1 = 0 ]; then
    # Remove GRUB2 from bootloader menu on final remove
    %{_sbindir}/bootloader-config --action remove-entry --image /boot/%{name}/core.img
    # XXX Ugly
    rm -f /boot/%{name}/*.mod
    rm -f /boot/%{name}/*.img
    rm -f /boot/%{name}/*.lst
    rm -f /boot/%{name}/*.o
    rm -f /boot/%{name}/device.map
fi

#-----------------------------------------------------------------------
%files -f grub.lang
%defattr(-,root,root,-)
#%{libdir32}/%{name}
%{libdir32}/grub
%{_sbindir}/%{name}-*
%{_bindir}/%{name}-*
%{_datadir}/grub
%{_sysconfdir}/grub.d
%{_sysconfdir}/%{name}.cfg
%{_sysconfdir}/default/grub
%{_sysconfdir}/bash_completion.d/grub
%dir /boot/%{name}
%dir /boot/%{name}/locale
/boot/%{name}/themes
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/%{name}/grub.cfg
%doc %{_docdir}/%{name}
%{_infodir}/%{name}.info*
%{_infodir}/grub-dev.info*
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man8/%{name}-*.8*
# RPM filetriggers
%{_filetriggers_dir}/%{name}.*
