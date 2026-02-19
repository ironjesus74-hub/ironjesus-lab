#!/data/data/com.termux/files/usr/bin/bash
echo "Running device health..."
getprop ro.build.version.release
pm list packages | grep google
