Name:           grub2
Version:        1.95
Release:        %mkrel 3
Epoch:          0
Summary:        GRand Unified Bootloader
License:        GPL
Group:          System/Kernel and hardware
URL:            http://www.gnu.org/software/grub/grub-2.en.html
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-1.95.tar.gz
Source1:        ftp://alpha.gnu.org/gnu/grub/grub-1.95.tar.gz.sig
BuildRequires:  bison
BuildRequires:  liblzo-devel
BuildRequires:  libncurses-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description 
GNU GRUB is a very powerful boot loader, which can load a wide
variety of free operating systems, as well as proprietary operating
systems with chain-loading.

%prep
%setup -q -n grub-%{version}

%build
%{configure2_5x}
%{__make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS TODO 
%{_bindir}/grub-mkimage
%{_sbindir}/grub-emu
%{_sbindir}/grub-install
%{_sbindir}/grub-mkdevicemap
%{_sbindir}/grub-probe
%{_sbindir}/grub-setup
%{_libdir}/grub


