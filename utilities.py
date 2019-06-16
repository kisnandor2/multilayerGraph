debug = True

TABS = ""

def debug(*arg):
	return
	global TABS
	if arg[0].lower() == "ret":
		TABS = TABS[:-3]
	if debug:
		print(TABS + str(arg))
	if arg[0][0] == "_" or arg[0][0] == "f":
		TABS = TABS + "   "