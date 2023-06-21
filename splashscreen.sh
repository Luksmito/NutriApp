sed -i 's/remove_presplash()/pass/' .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/kivy/arm64-v8a__ndk_target_28/kivy/kivy/base.py

python3 -m compileall .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/kivy/arm64-v8a__ndk_target_28/kivy/kivy/base.py -f -b

cp -f .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/kivy/arm64-v8a__ndk_target_28/kivy/kivy/base.pyc .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/dists/nutriapp/_python_bundle__arm64-v8a/_python_bundle/site-packages/kivy

cp -f .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/kivy/arm64-v8a__ndk_target_28/kivy/kivy/base.pyc .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/dists/nutriapp/_python_bundle__armeabi-v7a/_python_bundle/site-packages/kivy

sed -i "s/mActivity.removeLoadingScreen()/pass/" .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/android-sdl2/arm64-v8a__ndk_target_28/android/android/_android.pyx

cp -f .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/android-sdl2/arm64-v8a__ndk_target_28/android/android/_android.pyx .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/android-sdl2/armeabi-v7a__ndk_target_28/android/android/_android.pyx

cp -f .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/android-sdl2/arm64-v8a__ndk_target_28/android/android/_android.pyx .buildozer/android/platform/python-for-android/pythonforandroid/recipes/android/src/android/_android.pyx

sed -i 's/5000)/50000)/' .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/bootstrap_builds/sdl2/src/main/java/org/kivy/android/PythonActivity.java

sed -i 's/5000)/50000)/' .buildozer/android/platform/build-arm64-v8a_armeabi-v7a/dists/nutriapp/src/main/java/org/kivy/android/PythonActivity.java

sed -i 's/5000)/50000)/' .buildozer/android/platform/python-for-android/pythonforandroid/bootstraps/sdl2/build/src/main/java/org/kivy/android/PythonActivity.java