# Generate KLE json from KLFC keyboard layout json
import sys, json, re, copy
from os import path

MIN_ARGS = 3
VALID_OPTIONS = [["-kt", "-ks", "-kc", "-lc", "-sl", "-bc"], ["--keyboard-type", "--keyboard-size", "--key-color", "--label-color", "--shift-levels", "--back-color"]]
OPTION_DEFAULTS = {
	"-kt" : "iso",
	"-ks" : "100",
	"-kc" : "545454",
	"-lc" : "e0dcc8",
	"-bc" : "454545",
	"-sl" : "1"
}

#Each entry is an array of positions (positions.md). First entry is the one in the base .json. Other ones are aliases.
#This array is processed to match a keyboard type and size if supplied.
ALIASES = [
	["Esc", "Escape", "ESC"], ["F1", "FK01"], ["F2", "FK02"], ["F3", "FK03"], ["F4", "FK04"], ["F5", "FK05"], ["F6", "FK06"], ["F7", "FK07"], ["F8", "FK08"], ["F9", "FK09"], ["F10", "FK10"], ["F11", "FK11"], ["F12", "FK12"], ["PrintScreen", "PRSC"], ["ScrollLock", "SCLK"], ["Pause", "PAUS"], 
	["~", "``` ``", "Tilde", "TLDE"], ["1", "AE01"], ["2", "AE02"], ["3", "AE03"], ["4", "AE04"], ["5", "AE05"], ["6", "AE06"], ["7", "AE07"], ["8", "AE08"], ["9", "AE09"], ["0", "AE10"], ["-", "Minus", "AE11"], ["+", "=", "Plus", "AE12"], ["Yen", "AE13"], ["Backspace", "BKSP"],
	["Tab", "TAB"], ["Q", "AD01"], ["W", "AD02"], ["E", "AD03"], ["R", "AD04"], ["T", "AD05"], ["Y", "AD06"], ["U", "AD07"], ["I", "AD08"], ["O", "AD09"], ["P", "AD10"], ["[", "AD11"], ["]", "AD12"], ["\\", "BKSL"],
	["CapsLock", "CAPS"], ["A", "AC01"], ["S", "AC02"], ["D", "AC03"], ["F", "AC04"], ["G", "AC05"], ["H", "AC06"], ["J", "AC07"], ["K", "AC08"], ["L", "AC09"], [";", "AC10"], ["'", "AC11"], ["\\", "BKSL"], ["Enter", "RTRN"], 
	["Shift_L", "LFSH"], ["Iso", "LSGT"], ["Z", "AB01"], ["X", "AB02"], ["C", "AB03"], ["V", "AB04"], ["B", "AB05"], ["N", "AB06"], ["M", "AB07"], [",", "AB08"], [".", "AB09"], ["/", "AB10"], ["Ro", "AB11"], ["Shift_R", "RTSH"],
	["Control_L", "LCTL"], ["Win_L", "LWIN"], ["Alt_L", "LALT"], ["Mhen", "Muhenkan"], ["Space", "SPCE"], ["Henk", "Henkan"], ["Kana", "Katakana"], ["Alt_R", "RALT"], ["Win_R", "RWIN"], ["Menu", "MENU"], ["Control_R", "RCTL"], 	
	["Insert", "INS"], ["Delete", "DELE"], ["Home", "HOME"], ["End", "END"], ["PageUp", "PGUP"], ["PageDown", "PGDN"], ["Up", "UP"], ["Left", "LEFT"], ["Down", "DOWN"], ["Right", "RGHT"],
	["NumLock", "NMLK"], ["KP_Div", "KPDV"], ["KP_Mult", "KPMU"], ["KP_Min", "KPSU"], ["KP_7", "KP7"], ["KP_8", "KP8"], ["KP_9", "KP9"], ["KP_Plus", "KPAD"], ["KP_4", "KP4"], ["KP_5", "KP5"], ["KP_6", "KP6"], ["KP_Comma"], ["KP_1", "KP1"], ["KP_2", "KP2"], ["KP_3", "KP3"], ["KP_Enter", "KPEN"], ["KP_0", "KP0"], ["KP_Dec", "KPDL"] 
	]


def main():	
	#Check for arg numbers
	if len(sys.argv) == 1:
		usage()
		return
	elif len(sys.argv) == 2:
		if (sys.argv[1] == 'man' or sys.argv[1] == 'help'):
			help()
			return
		else:
			usage()
			return
	elif len(sys.argv) > 2 and len(sys.argv) < MIN_ARGS:
		usage()
		return
	elif len(sys.argv) >= MIN_ARGS:
		# Check that args are good
		if not check_args():
			usage()
			return	
					
	#Fall-through only with good args and good arg number.
	
	#Get all components
	comps = extract_components(True)
	
	#Get list of present keys
	keys = []
	for k in comps.keys():
		keys.append(k)
		
	#Normalize keys to short form
	for i in range(0, len(keys)):
		if keys[i] in VALID_OPTIONS[1]:
			comps[VALID_OPTIONS[0][VALID_OPTIONS[1].index(keys[i])]] = comps[keys[i]]
			del comps[keys[i]]
			print(comps)
			
	#Fill with missing options	
	for i in OPTION_DEFAULTS.keys():
		if i not in comps.keys():
			comps[i] = OPTION_DEFAULTS[i]
			
	#Open input file, parse .json, load to memory
	
	#Create output file from base, change based on memory
	

# Check args for number and validity.
def check_args():
	max_args = len(VALID_OPTIONS[0]) + len(VALID_OPTIONS[1]) + MIN_ARGS
	# Check that last arg is valid output path
	if not (path.isdir(sys.argv[len(sys.argv)-1])):
		print("Invalid output path. Use a relative path (e.g. './') or absolute path (e.g. '/home/user/klfc/kle/myfiles', 'C://User/KLFC/MyFiles'). No quotes.")
	
	# Check that second to last arg is valid file
	if not (path.exists(sys.argv[len(sys.argv)-2]) and re.match('^.*\.json$', sys.argv[len(sys.argv)-2])):
		print("Invalid input file. Use a relative or absolute path. Filename must end with .json. File must be a KLFC layout file. No quotes.")
	
	# Check that arg number makes sense (odd, equal or more than 3+len(valid_options), equal or less than MIN_ARGS)
	if len(sys.argv) > max_args:
		print("Too many arguments. Expected no less than " + str(MIN_ARGS) + " and no more than " + max_args + ".")
		return False
	if len(sys.argv) % 2 == 0:
		print("Bad input.")
		return False
			
	# Obtain option arguments for checking, without file and path entries
	options = extract_components(False)
		
	# Check if options exist
	for i in options.keys():
		if not i in VALID_OPTIONS[0] and not i in VALID_OPTIONS[1]:
			print("\nInvalid option: " + i + "\n")
			return False	
	
	# Check if option values exist
	for i in options.keys():
		value = options[i]
		
		if i == "-kt" or i == "--keyboard-type":
			if not (value in ["ansi", "ANSI", "iso", "ISO", "ans", "ANS", "jis", "JIS", "abnt", "ABNT"]):
				print("\nUnrecognized keyboard type: " + value + "\nSupported types: ANSI, ISO, JIS, ABNT.")
				return False
				
		if i == "-ks" or i == "--keyboard-size":
			if not (value in ["60", "80", "100"]):
				print("\nUnrecognized keyboard size: " + value + "\nSupported sizes: 60, 80, 100.")
				return False
				
		if i == "-kc" or i == "--key-color":
			if not (re.match("^[0-9a-fA-F]{6}$", value)):
				print("\nUnrecognized hex color: " + value + "\nSupported format: ffffff. No hash.")
				return False
				
		if i == "-lc" or i == "--label-color":
			if not (re.match("^[0-9a-fA-F]{6}$", value)):
				print("\nUnrecognized hex color: " + value + "\nSupported format: ffffff. No hash.")
				return False
				
		if i == "-sl" or i == "--shift-levels":
			if int(value) < 1 or int(value) > 4:
				print("\nUnrecognized shift values: " + value + "\nSupported values: 1, 2, 3, 4")
				return False
				
		if i == "-bc" or i == "--back-color":
			if not (re.match("^[0-9a-fA-F]{6}$", value)):
				print("\nUnrecognized hex color: " + value + "\nSupported format: ffffff. No hash.")
				return False
		
	return True
		
# Returns a dictionary with all relevant components. Components not checked for validity.
def extract_components(include_file_and_path):
	extracted = {}
	
	#Process file and path
	if include_file_and_path:
		extracted["file"] = sys.argv[-2]
		extracted["output_path"] = sys.argv[-1]
		
	#Process options
	used_options = copy.deepcopy(sys.argv)
	del used_options[-1]
	del used_options[-1]
	del used_options[0]
	for i in range(0, len(used_options)-1):
		if i % 2 == 0:
			extracted[used_options[i]] = used_options[i+1]
	
	#Return
	return extracted

# Short help
def usage():
	print("\nUsage: python kle-gen.py [OPTIONS] [KLFC_FILE.json] [OUTPUT_PATH]")
	print("Input 'python kle-gen.py help' or 'python kle-gen.py man' for help.\n")

# Long help
def help():
	print("\nSYNTAX:")
	print("python kle-gen.py [OPTIONS] file_to_convert.json [OUTPUT_PATH]\n")
	print("OPTIONS:")
	print("-kt / --keyboard-type (optional): Keyboard type. Defaults to ISO. Can be ANSI, ISO, JIS or ABNT")
	print("-ks / --keyboard-size (optional): Keyboard size (integer; 100, 80 or 60). Defaults to 100%.")
	print("-kc / --key-color     (optional): Key color (hex value). Defaults to grey.")
	print("-lc / --label-color   (optional): Label color (hex value). Defaults to off-white.")
	print("-sl / --shift-levels  (optional): Shift levels (integer, 1-4). Shift levels will be placed in the following order: top left, bottom left, top right, bottom right. Defaults to 1.\n")
	print("The last argument MUST be the output path. Simply add '.' to default to the script dir. Must be a directory.")
	print("The second to last argument MUST be the KLFC .json file to convert. Absolute or relative path.\n")
	print("Full input example:     python kle-gen.py -kt iso -ks 80 -kc #a5a5a5 -lc #aaaaaa -sl 2 ./colemak.json .")
	print("Minimum input example:  python kle-gen.py ./colemak.json .\n")

if __name__ == "__main__":
	main()

