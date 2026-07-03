# grub-btrfs (Fedora COPR build)

Fedora RPM packaging of [grub-btrfs](https://github.com/Antynea/grub-btrfs)
by Antynea adds Btrfs snapshots as bootable entries in the GRUB menu,
so you can boot directly into a snapshot to inspect or recover a system
without touching the running root filesystem.

This repository holds only the `.spec` file used to build the package on
[Fedora Copr](https://copr.fedorainfracloud.org/coprs/pego-copr/grub-btrfs/).
The actual source code is pulled from the upstream project at build time.

## Install

```bash
sudo dnf copr enable pego-copr/grub-btrfs
sudo dnf install grub-btrfs
```

After installing, generate the GRUB menu once and enable the daemon that
keeps it updated automatically whenever a snapshot is created or deleted:

```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo systemctl enable --now grub-btrfsd.service
```

## Why this exists

Upstream doesn't ship an RPM spec file, and grub-btrfs's `Makefile`
refuses to run its `install` target unless invoked as root which
breaks unprivileged RPM build environments (mock/copr-rpmbuild always
build as an unprivileged user). This spec avoids `make install`
entirely and installs each file directly via `install -Dm`, matching
the layout expected on Fedora (`grub2-mkconfig`, `/boot/grub2`).

## Source

This build tracks the upstream `master` branch of
[Antynea/grub-btrfs](https://github.com/Antynea/grub-btrfs), so package
content updates on every rebuild without needing a spec change only
the `Version` field is manually bumped for cosmetic accuracy.

## License

grub-btrfs itself is licensed under GPL-3.0 by its original author,
[Antynea](https://github.com/Antynea). This repository only contains
Fedora packaging metadata (the `.spec` file).
