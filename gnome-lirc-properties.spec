%define		polkit_minver 0.95-0.git20090913.2
%define		lirc_ver 0.8.6-1

Summary:	Infrared Remote Controls setup tool
Name:		gnome-lirc-properties
Version:	0.5.1
Release:	0.2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-lirc-properties/0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	a732d41e55bc0490bc0a68142f7cb18f
URL:		http://live.gnome.org/gnome-lirc-properties
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	lirc >= %{lirc_ver}
BuildRequires:	lirc-remotes >= %{lirc_ver}
BuildRequires:	python-devel >= 2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	scrollkeeper
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	lirc >= %{lirc_ver}
Requires:	lirc-remotes >= %{lirc_ver}
Requires:	polkit >= %{polkit_minver}
Requires:	python >= 1:2.5
Requires:	python-dbus
Requires:	python-pygtk-gtk
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnome-lirc-properties helps users set up infrared remote controls for
use with the LIRC framework.

%prep
%setup -q

%build
autoreconf
# --disable-policy-kit because 0.106 nuked polkit-backend-1 which this code depends on
#BuildRequires:	pkgconfig(polkit-backend-1)
%configure \
	--disable-policy-kit \
	--disable-conf-check \
	--with-remotes-database=%{_docdir}/lirc-remotes-0.9.0/remotes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/gnome-lirc-properties.desktop

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README AUTHORS
/etc/dbus-1/system.d/org.gnome.LircProperties.Mechanism.conf
%attr(755,root,root) %{_bindir}/gnome-lirc-properties
%{_datadir}/%{name}
%{_datadir}/polkit-1/actions/org.gnome.lirc-properties.mechanism.policy
%{_datadir}/dbus-1/system-services/org.gnome.LircProperties.Mechanism.service
%{_datadir}/hal/fdi/policy/10osvendor/20-x11-remotes.fdi
%{_desktopdir}/gnome-lirc-properties.desktop
%{_iconsdir}/hicolor/*/apps/gnome-lirc-properties.*
%{_mandir}/man1/gnome-lirc-properties.1*
%dir %{py_sitescriptdir}/gnome_lirc_properties
%{py_sitescriptdir}/gnome_lirc_properties/*.py[co]
%dir %{py_sitescriptdir}/gnome_lirc_properties/ui
%{py_sitescriptdir}/gnome_lirc_properties/ui/*.py[co]
