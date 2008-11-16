Summary:	GRand Unified Bootloader
Name:		grub2
Version:	1.96
Release:	%mkrel 1
Epoch:		0
License:	GPLv3
Group:		System/Kernel and hardware
URL:		http://www.gnu.org/software/grub/grub-2.en.html
Source0:	ftp://alpha.gnu.org/gnu/grub/grub-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
BuildRequires:	bison
BuildRequires:	liblzo-devel
BuildRequires:	libncurses-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
GNU GRUB is a very powerful boot loader, which can load a wide
variety of free operating systems, as well as proprietary operating
systems with chain-loading.

%prep
%setup -q -n grub-%{version}

%build
%configure2_5x
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_sysconfdir}/grub.d/README

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README THANKS TODO 
%dir %{_sysconfdir}/grub.d
%config(noreplace) %{_sysconfdir}/grub.d/00_header
%config(noreplace) %{_sysconfdir}/grub.d/10_hurd
%config(noreplace) %{_sysconfdir}/grub.d/10_linux
%{_bindir}/grub-mkimage
%{_bindir}/grub-mkrescue
#%{_sbindir}/grub-emu
%{_sbindir}/grub-install
%{_sbindir}/grub-mkdevicemap
%{_sbindir}/grub-probe
%{_sbindir}/grub-setup
%{_sbindir}/update-grub
%{_libdir}/grub
