%define major 2
%define libname %mklibname va %{major}
%define devname %mklibname va -d
# disable utils after upgrade, that build libva
# and enable utils
%bcond_with utils

Summary:	Video Acceleration (VA) API for Linux
Name:		libva
Epoch:		2
Version:	2.0.0
Release:	1
Group:		System/Libraries
License:	MIT
Url:		https://01.org/linuxmedia/vaapi
Source0:	https://github.com/01org/libva/archive/libva-%{version}.tar.gz
# utils
Source1:	https://github.com/01org/libva-utils/archive/%{version}.tar.gz
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)

%description
Libva is a library providing the VA API video acceleration API.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libva is a library providing the VA API video acceleration API.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with utils}
%package	utils
Summary:	Tools for %{name} (including vainfo)
Group:		System/Libraries
BuildRequires:	%{name}-devel = %{EVRD}

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.
%endif

%prep
%setup -qn %{name}-%{name}-%{version} -a 1
NOCONFIGURE=1 ./autogen.sh
cd libva-utils*
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--enable-glx

%make

%if %{with utils}
pushd %{name}-utils-%{version}
%configure
%make
popd
%endif

%install
%makeinstall_std
%if %{with utils}
%makeinstall_std -C %{name}-utils-%{version}
%endif

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}-wayland.so.%{major}*
%{_libdir}/%{name}-drm.so.%{major}*
%{_libdir}/%{name}-glx.so.%{major}*
%{_libdir}/%{name}-x11.so.%{major}*

%files -n %{devname}
%doc COPYING
%{_includedir}/va
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%if %{with utils}
%files utils
%{_bindir}/avcenc
%{_bindir}/jpegenc
%{_bindir}/mpeg2vaenc
%{_bindir}/h264encode
%{_bindir}/loadjpeg
%{_bindir}/mpeg2vldemo
%{_bindir}/putsurface*
%{_bindir}/vainfo
%endif
