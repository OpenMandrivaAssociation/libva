%define major 2
%define libname %mklibname va %{major}
%define devname %mklibname va -d
%global optflags %{optflags} -O3

%bcond_without	glx

Summary:	Video Acceleration (VA) API for Linux
Name:		libva
Version:	2.6.0
Release:	1
Group:		System/Libraries
License:	MIT
Url:		http://freedesktop.org/wiki/Software/vaapi
Source0:	https://github.com/01org/libva/releases/download/%{version}/%{name}-%{version}.tar.gz
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
BuildRequires:  meson

%description
Libva is a library providing the VA API video acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{mklibname va-drm %{major}} = %{EVRD}
%if %{with glx}
Requires:	%{mklibname va-glx %{major}} = %{EVRD}
%endif
Requires:	%{mklibname va-wayland %{major}} = %{EVRD}
Requires:	%{mklibname va-x11 %{major}} = %{EVRD}
%ifnarch %{armx} %{riscv}
Requires:	libva-intel-driver
%endif

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
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson \
%if %{with glx}
	-Dwith_glx \
	-Dwith_x11 \
	-Dwith_wayland
%endif
%meson_build

%install
%meson_install

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{devname}
%doc COPYING
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc
