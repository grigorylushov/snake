[app]

title = Snake Game
package.name = snake
package.domain = gn.kp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.3.0
orientation = portrait
osx.kivy_version = 2.2.0
fullscreen = 0

android.api = 30
android.minapi = 21
android.ndk = 23b
android.ndk_api = 21
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r23b
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

[buildozer]

log_level = 2
warn_on_root = 1
