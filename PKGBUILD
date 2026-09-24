# Maintainer: Mig Saito <migsaito@example.com>
pkgname=arch-universal-toolbox
pkgver=0.1.0
pkgrel=1
pkgdesc='Graphical toolbox for Arch Linux package and mirror management'
arch=('any')
url='https://github.com/migsaito/arch-universal-toolbox'
license=('MIT')
depends=('python' 'python-pyqt5' 'pacman')
source=("$pkgname-$pkgver.tar.gz::https://github.com/migsaito/arch-universal-toolbox/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
  cd "$pkgname-$pkgver"
  python -m compileall -q src
}

package() {
  cd "$pkgname-$pkgver"

  install -dm755 "$pkgdir/usr/lib/$pkgname"
  cp -r src "$pkgdir/usr/lib/$pkgname/"
  install -dm755 "$pkgdir/usr/share/$pkgname/locales"
  install -m644 src/locales/*.json "$pkgdir/usr/share/$pkgname/locales/"
  install -Dm755 run.py "$pkgdir/usr/bin/$pkgname"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 packaging/$pkgname.desktop \
    "$pkgdir/usr/share/applications/$pkgname.desktop"
  install -Dm644 packaging/$pkgname.svg \
    "$pkgdir/usr/share/icons/hicolor/scalable/apps/$pkgname.svg"

  sed -i "s|/usr/bin/env python3|/usr/bin/python|" \
    "$pkgdir/usr/bin/$pkgname"
  sed -i "s|from src.main import main|from sys import path; path.insert(0, '/usr/lib/$pkgname'); from src.main import main|" \
    "$pkgdir/usr/bin/$pkgname"
  sed -i "s|Path(__file__).parent / \"locales\"|Path('/usr/share/$pkgname/locales')|" \
    "$pkgdir/usr/lib/$pkgname/i18n.py"
}
