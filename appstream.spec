%define oname AppStream

%define major 2
%define girmajor 0.8
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{girmajor}
%define devname %mklibname %{name} -d

%define qt_major 1
%define libnameqt %mklibname %{name}qt %{qt_major}
%define devnameqt %mklibname %{name}qt -d

Summary:	Utilities to generate, maintain and access the AppStream Xapian database
Name:		appstream
Version:	0.8.0
Release:	1
# lib LGPLv2.1+, tools GPLv2+
License:	GPLv2+ and LGPLv2.1+
Group:		System/Configuration/Packaging
Url:		http://www.freedesktop.org/wiki/Distributions/AppStream/Software
Source0:	http://www.freedesktop.org/software/appstream/releases/%{oname}-%{version}.tar.xz
BuildRequires:	cmake
BuildRequires:	intltool
BuildRequires:	xmlto
BuildRequires:	xapian-core-devel
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(yaml-0.1)
# Should be added later, requires generation script
# Requires:	appstream-data

%description
AppStream-Core makes it easy to access application information from the
AppStream database over a nice GObject-based interface.

%files -f appstream.lang
%doc AUTHORS LICENSE.GPLv2 LICENSE.LGPLv2.1
%config(noreplace) %{_sysconfdir}/appstream.conf
%{_bindir}/appstream-index
%{_bindir}/appstream-validate
%{_mandir}/man1/appstream-index.1*
%{_mandir}/man1/appstream-validate.1*
%dir %{_datadir}/app-info/
%dir %{_datadir}/app-info/icons
%dir %{_datadir}/app-info/xmls
%{_datadir}/app-info/categories.xml
%ghost %{_var}/cache/app-info/cache.watch
%dir %{_var}/cache/app-info
%dir %{_var}/cache/app-info/icons
%dir %{_var}/cache/app-info/xapian
%dir %{_var}/cache/app-info/xmls

%posttrans
%{_bindir}/appstream-index refresh --force >& /dev/null ||:

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared library for %{name}.

%files -n %{libname}
%{_libdir}/libappstream.so.%{major}*
%{_libdir}/libappstream.so.%{version}

#----------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection files for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{girname}
GObject Introspection files for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/AppStream-%{girmajor}.typelib

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%{_includedir}/AppStream/
%{_libdir}/libappstream.so
%{_libdir}/pkgconfig/appstream.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/AppStream-0.8.gir
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/appstream

#----------------------------------------------------------------------------

%package -n %{libnameqt}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libnameqt}
Shared library for %{name}.

%files -n %{libnameqt}
%{_libdir}/libAppstreamQt.so.%{qt_major}*

#----------------------------------------------------------------------------

%package -n %{devnameqt}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libnameqt} = %{EVRD}
Provides:	%{name}-qt5-devel = %{EVRD}

%description -n %{devnameqt}
Development files for %{name}.

%files -n %{devnameqt}
%{_includedir}/AppstreamQt/
%{_libdir}/cmake/AppstreamQt/
%{_libdir}/libAppstreamQt.so

#----------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}

%build
%cmake \
	-DQT:BOOL=ON \
	-DAPPSTREAM_QT_VERSION:STRING="5" \
	-DTESTS:BOOL=ON \
	-DVAPI:BOOL=OFF

%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_datadir}/app-info/{icons,xmls}
mkdir -p %{buildroot}%{_var}/cache/app-info/{icons,xapian,xmls}
touch %{buildroot}%{_var}/cache/app-info/cache.watch

%find_lang appstream

