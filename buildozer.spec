[app]
title = ApexTitan
package.name = apextitan
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,ttf,wav,mp3,ogg
version = 0.1
requirements = python3==3.10.12,hostpython3==3.10.12,kivy==2.3.0,pyjnius==1.5.0,pygame
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
