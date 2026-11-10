[app]
title = Zeta AI
package.name = zeta_ai
package.domain = org.mubashir
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,requests,urllib3,certifi

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Target stable SDK and NDK configurations matching the runner profiles
android.api = 33
android.minapi = 24
android.ndk = 25b
android.skip_apk_rescale = True

android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

[buildozer]
log_level = 2
warn_on_root = 1
