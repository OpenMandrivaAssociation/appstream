%define oname AppStream

%define major 4
%define girmajor 1.0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{girmajor}
%define devname %mklibname %{name} -d

%define qt_major 2
%define oldlibnameqt %mklibname AppStreamQt 2
%define libnameqt %mklibname AppStreamQt
%define devnameqt %mklibname AppStreamQt -d

Summary:	Utilities to generate, maintain and access the AppStream Xapian database
Name:		appstream
Version:	0.16.4
Release:	1
# lib LGPLv2.1+, tools GPLv2+
License:	GPLv2+ and LGPLv2.1+
Group:		System/Configuration/Packaging
Url:		https://www.freedesktop.org/wiki/Distributions/AppStream/Software
Source0:	https://www.freedesktop.org/software/appstream/releases/%{oname}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	qmake5
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	xmlto
BuildRequires:	gperf
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(xmlb) >= 0.3.6
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	vala-tools
BuildRequires:	gtk-doc
BuildRequires:	libstemmer-devel
BuildRequires:	lmdb-devel
Requires:	%{libname} = %{EVRD}
# Should be added later, requires generation script
# Requires:	appstream-data

%description
AppStream-Core makes it easy to access application information from the
AppStream database over a nice GObject-based interface.

%files -f appstream.lang
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/appstream.conf
%{_bindir}/appstreamcli
%{_mandir}/man1/appstreamcli.1.*
%dir %{_datadir}/app-info/
%dir %{_datadir}/app-info/icons
%dir %{_datadir}/app-info/xmls
%{_datadir}/metainfo/org.freedesktop.appstream.cli.metainfo.xml
%ghost %{_var}/cache/app-info/cache.watch
%dir %{_var}/cache/app-info
%dir %{_var}/cache/app-info/icons
%dir %{_var}/cache/app-info/gv
%dir %{_var}/cache/app-info/xapian
%dir %{_var}/cache/app-info/xmls
%{_datadir}/gettext/its/metainfo.*

%posttrans
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:
 
%transfiletriggerin -- %{_datadir}/app-info/xmls
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:
 
%transfiletriggerpostun -- %{_datadir}/app-info/xmls
%{_bindir}/appstreamcli refresh --force >& /dev/null ||:

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Obsoletes:	%{mklibname appstream 2} < 0.9.0

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
Obsoletes:	%{mklibname appstream-git 0.8} < 0.9.0

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
%doc %{_docdir}/%{name}
%{_includedir}/appstream/
%{_libdir}/libappstream.so
%{_libdir}/pkgconfig/appstream.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/AppStream-%{girmajor}.gir
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/appstream
%{_datadir}/installed-tests/appstream/metainfo-validate.test

#----------------------------------------------------------------------------

%package -n %{libnameqt}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
%rename   %{oldlibnameqt}
Obsoletes:	%{mklibname appstreamqt 1} < 0.10.4
Obsoletes:	%{mklibname AppStreamQt 3} < 1.0.0-0.20230924.1

%description -n %{libnameqt}
Shared library for %{name}.

%files -n %{libnameqt}
%{_libdir}/libAppStreamQt.so.%{qt_major}*
%{_libdir}/libAppStreamQt.so.%{version}*

#----------------------------------------------------------------------------

%package -n %{devnameqt}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libnameqt} = %{EVRD}
Provides:	%{name}-qt5-devel = %{EVRD}
Obsoletes:	%{mklibname appstreamqt -d} < 0.10.4

%description -n %{devnameqt}
Development files for %{name}.

%files -n %{devnameqt}
%{_includedir}/AppStreamQt/
%{_libdir}/cmake/AppStreamQt/
%{_libdir}/libAppStreamQt.so

%package vala
Summary:	Vala bindings for %{name}
Group:		Development/Other
Requires:	%{name}%{?_isa} = %{EVRD}
Requires:	vala

%description vala
Vala files for %{name}.

%files vala
%{_datadir}/vala/vapi/appstream.deps
%{_datadir}/vala/vapi/appstream.vapi

#----------------------------------------------------------------------------

%prep
%autosetup -n %{oname}-%{version}

%build
%meson \
    -Dqt=true \
    -Dvapi=true

%meson_build

%install
%meson_install
mkdir -p %{buildroot}%{_datadir}/app-info/{icons,xmls}
mkdir -p %{buildroot}%{_var}/cache/app-info/{icons,gv,xapian,xmls}
touch %{buildroot}%{_var}/cache/app-info/cache.watch

%find_lang appstream
