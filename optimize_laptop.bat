@echo off
title Laptop System Health and Performance Optimizer
color 0b
echo =======================================================
echo     LAPTOP FULL SYSTEM REPAIR AND OPTIMIZATION
echo =======================================================
echo.
echo [1/5] Running Windows Image Component Repair (DISM)...
echo -------------------------------------------------------
DISM /Online /Cleanup-Image /RestoreHealth
echo.
echo [2/5] Running System File Checker (SFC Scan)...
echo -------------------------------------------------------
sfc /scannow
echo.
echo [3/5] Cleaning up Windows Component Store...
echo -------------------------------------------------------
DISM /Online /Cleanup-Image /StartComponentCleanup
echo.
echo [4/5] Optimizing and TRIMming NVMe SSD (C:)...
echo -------------------------------------------------------
powershell -Command "Optimize-Volume -DriveLetter C -ReTrim -Verbose"
echo.
echo [5/5] Flushing and Resetting Network Stack...
echo -------------------------------------------------------
ipconfig /flushdns
netsh winsock reset
echo.
echo =======================================================
echo   ALL SYSTEM REPAIRS AND OPTIMIZATIONS COMPLETED!
echo =======================================================
echo.
echo You may now close this window or restart your laptop.
pause
