Name:           grub-btrfs
Version:        4.11
Release:        1%{?dist}
Summary:        Include btrfs snapshots as GRUB boot options

License:        GPLv3
URL:            https://github.com/Antynea/grub-btrfs
Source0:        https://github.com/Antynea/grub-btrfs/archive/refs/heads/master.tar.gz

BuildArch:      noarch
Requires:       grub2-tools, btrfs-progs, inotify-tools, bash
BuildRequires:  make

%description
grub-btrfs adds a submenu to the GRUB boot menu listing available
Btrfs snapshots (created with Snapper, Timeshift, or manually),
allowing the system to boot directly into a read-only snapshot.

%prep
%setup -q -n grub-btrfs-master

%build
# Nothing to compile, shell scripts only

%install
make DESTDIR=%{buildroot} \
     PREFIX=/usr \
     LIB_DIR=%{buildroot}/usr/lib \
     SHARE_DIR=%{buildroot}/usr/share \
     BIN_DIR=%{buildroot}/usr/bin \
     MAN_DIR=%{buildroot}/usr/share/man \
     SYSTEMD=true \
     INITCPIO=false \
     INSTALL_DOCS=true \
     install

%files
/etc/grub.d/41_snapshots-btrfs
/etc/default/grub-btrfs/config
/usr/bin/grub-btrfsd
%{_unitdir}/grub-btrfsd.service
%{_unitdir}/grub-btrfs.path
%doc /usr/share/doc/%{name}/README.md
%{_mandir}/man8/grub-btrfs.8*
%{_mandir}/man8/grub-btrfsd.8*

%changelog
* Fri Jul 03 2026 Pego <tuamail@esempio.com> - 4.11-1
- Build personale da sorgente upstream Antynea
