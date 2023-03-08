#!/usr/bin/python3


import pyautogui, sys, time

if len(sys.argv) > 1:
	cmd = sys.argv[1]
	if cmd == "x":
			print(pyautogui.position().x)
	elif cmd == "y":
			print(pyautogui.position().y)
