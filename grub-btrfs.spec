%define debug_package %{nil}

Name:           grub-btrfs
Version:        4.14
Release:        1%{?dist}
Summary:        Include btrfs snapshots at boot menu for GRUB

License:        GPL-3.0-only
URL:            https://github.com/Antynea/grub-btrfs
Source0:        https://github.com/Antynea/grub-btrfs/archive/refs/heads/master.tar.gz

BuildArch:      noarch
BuildRequires:  bash
BuildRequires:  bzip2

Requires:       btrfs-progs
Requires:       grub2-tools
Requires:       util-linux
Requires:       grep
Requires:       inotify-tools

%description
grub-btrfs is a simple script that automatically includes btrfs snapshots
in the GRUB boot menu, allowing you to select snapshots for booting in
case of system failures.

%prep
%setup -q -n %{name}-master

%build
mkdir TEMP_DIR
cp manpages/grub-btrfs.8.man TEMP_DIR/grub-btrfs.8
bzip2 TEMP_DIR/grub-btrfs.8
cp manpages/grub-btrfsd.8.man TEMP_DIR/grub-btrfsd.8
bzip2 TEMP_DIR/grub-btrfsd.8

%install
install -Dm755 -t "%{buildroot}%{_sysconfdir}/grub.d/" 41_snapshots-btrfs
install -Dm644 -t "%{buildroot}%{_sysconfdir}/default/grub-btrfs/" config
install -Dm755 -t "%{buildroot}%{_bindir}/" grub-btrfsd
install -Dm644 -t "%{buildroot}%{_prefix}/lib/systemd/system/" grub-btrfsd.service
install -Dm644 -t "%{buildroot}%{_mandir}/man8" "TEMP_DIR/grub-btrfs.8.bz2"
install -Dm644 -t "%{buildroot}%{_mandir}/man8" "TEMP_DIR/grub-btrfsd.8.bz2"

# Fedora usa grub2-mkconfig e /boot/grub2, non grub-mkconfig/ /boot/grub
sed -i \
    -e 's|^#GRUB_BTRFS_MKCONFIG=.*|GRUB_BTRFS_MKCONFIG=/usr/sbin/grub2-mkconfig|' \
    -e 's|^#GRUB_BTRFS_GRUB_DIRNAME=.*|GRUB_BTRFS_GRUB_DIRNAME="/boot/grub2"|' \
    -e 's|^#GRUB_BTRFS_SCRIPT_CHECK=.*|GRUB_BTRFS_SCRIPT_CHECK=grub2-script-check|' \
    "%{buildroot}%{_sysconfdir}/default/grub-btrfs/config"

%post
if [ "$(stat -c %d:%i /)" = "$(stat -c %d:%i /proc/1/root/.)" ]; then
    /usr/sbin/grub2-mkconfig -o /boot/grub2/grub.cfg || :
fi

%files
%license LICENSE
%doc README.md
%{_sysconfdir}/grub.d/41_snapshots-btrfs
%{_sysconfdir}/default/grub-btrfs/config
%{_bindir}/grub-btrfsd
%{_mandir}/man8/grub-btrf*.8.*
%{_prefix}/lib/systemd/system/grub-btrfsd.service

%changelog
* Fri Jul 03 2026 gabriy2 <120041541+gabriy2@users.noreply.github.com> - 4.13-1
- Build per Fedora, adattato da OpenMandrivaAssociation/grub-btrfs
