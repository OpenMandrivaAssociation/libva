# libva is used by mesa. Mesa is used by wine and steam.
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 2
%define oldlibname %mklibname va 2
%define libname %mklibname va
%define devname %mklibname va -d
%define oldlib32name libva2
%define lib32name libva%{major}
%define dev32name libva-devel
%global optflags %{optflags} -O3

%bcond_without glx

Summary:	Video Acceleration (VA) API for Linux
Name:		libva
Version:	2.19.0
Release:	1
Group:		System/Libraries
License:	MIT
Url:		http://01.org/linuxmedia
Source0:	https://github.com/intel/libva/archive/%{version}/%{name}-%{version}.tar.gz
%ifarch %{armx}
# (tpg) add support fot Hantro VPU
#Patch1:		https://patch-diff.githubusercontent.com/raw/intel/libva/pull/340.patch
%endif
%if %{with glx}
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
%endif
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	meson
%if %{with compat32}
BuildRequires:	devel(libdrm)
BuildRequires:	devel(libpciaccess)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libGL)
%endif

%description
Libva is a library providing the VA API video acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{mklibname va-drm} = %{EVRD}
%if %{with glx}
Requires:	%{mklibname va-glx} = %{EVRD}
%endif
Requires:	%{mklibname va-wayland} = %{EVRD}
Requires:	%{mklibname va-x11} = %{EVRD}
%ifnarch %{armx} %{riscv}
Requires:	libva-intel-driver
%endif
%rename %{oldlibname}

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.

%libpackage va-drm %{major}
%if %{with glx}
%libpackage va-glx %{major}
%endif
%libpackage va-wayland %{major}
%libpackage va-x11 %{major}

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library for %{name} (32-bit)
Group:		System/Libraries
Requires:	libva-drm = %{EVRD}
%if %{with glx}
Requires:	libva-glx = %{EVRD}
%endif
Requires:	libva-wayland = %{EVRD}
Requires:	%{mklib32name va-x11} = %{EVRD}
%rename %{oldlib32name}

%description -n %{lib32name}
Libva is a library providing the VA API video acceleration API.

%lib32package va-drm %{major}
%if %{with glx}
%lib32package va-glx %{major}
%endif
%lib32package va-wayland %{major}
%lib32package va-x11 %{major}

%package -n %{dev32name}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%endif

%prep
%autosetup -p1

%if %{with compat32}
%meson32 \
%if %{with glx}
	-Dwith_glx=yes \
%endif
	-Dwith_x11=yes \
	-Dwith_wayland=yes \
	-Dwith_legacy=emdg,nvctrl,fglrx
%endif

%meson \
%if %{with glx}
	-Dwith_glx=yes \
%endif
	-Dwith_x11=yes \
	-Dwith_wayland=yes \
	-Dwith_legacy=emdg,nvctrl,fglrx

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{devname}
%doc COPYING
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/%{name}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/%{name}*.so
%{_prefix}/lib/pkgconfig/%{name}*.pc
%endif
