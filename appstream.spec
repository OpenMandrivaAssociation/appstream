%define oname AppStream

%define major 4
%define girmajor 1.0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{girmajor}
%define devname %mklibname %{name} -d

%define qt_major 2
%define libnameqt %mklibname AppStreamQt %{qt_major}
%define devnameqt %mklibname AppStreamQt -d

Summary:	Utilities to generate, maintain and access the AppStream Xapian database
Name:		appstream
Version:	0.12.2
Release:	1
# lib LGPLv2.1+, tools GPLv2+
License:	GPLv2+ and LGPLv2.1+
Group:		System/Configuration/Packaging
Url:		http://www.freedesktop.org/wiki/Distributions/AppStream/Software
Source0:	http://www.freedesktop.org/software/appstream/releases/%{oname}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	qmake5
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	xmlto
BuildRequires:	gperf
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(packagekit-glib2)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	gtk-doc
BuildRequires:	libstemmer-devel
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
%dir %{_var}/cache/app-info/xapian
%dir %{_var}/cache/app-info/xmls
%{_datadir}/gettext/its/metainfo.*

%posttrans
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

#----------------------------------------------------------------------------

%package -n %{libnameqt}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Obsoletes:  %{mklibname appstreamqt 1} < 0.10.4

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
Obsoletes:  %{mklibname appstreamqt -d} < 0.10.4

%description -n %{devnameqt}
Development files for %{name}.

%files -n %{devnameqt}
%{_includedir}/AppStreamQt/
%{_libdir}/cmake/AppStreamQt/
%{_libdir}/libAppStreamQt.so

#----------------------------------------------------------------------------

%prep
%autosetup -n %{oname}-%{version}

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
%meson -Dqt=true
ninja -C build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR="%{buildroot}" ninja -C build install

mkdir -p %{buildroot}%{_datadir}/app-info/{icons,xmls}
mkdir -p %{buildroot}%{_var}/cache/app-info/{icons,xapian,xmls}
touch %{buildroot}%{_var}/cache/app-info/cache.watch

%find_lang appstream
