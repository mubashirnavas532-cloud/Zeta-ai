[app]
title = Zeta AI
package.name = zeta_ai
package.domain = org.mubashir
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,urllib3

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Permissions required for Zeta's advanced features
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

[buildozer]
log_level = 2
warn_on_root = 1
