[Not yet functional]

# KLFC-Gen
Python CLI utility to generate Keyboard Layout Editor (http://www.keyboard-layout-editor.com/) .json files from KLFC (https://github.com/39aldo39/klfc) layout files.

The KLFC format is a simple and powerful 'centralizing' method to design keyboard layouts and generate files for intalling said layout in multiple systems.
KLFC-Gen will generate a complete .json to also visualize such layout in Keyboard Layout Editor. The generated .json can also be directly rendered in high res at KLE-Render (https://kle-render.herokuapp.com/)

## Usage
Make sure you have Python installed and working normally.

Download the full code folder.

Navigate to the folder containing `klfc-gen.py`.

Have a KLFC script ready to use as input. I've included the Colemak example from KLFC.

Open a terminal or command prompt and run the program.

## Syntax

`python klfc-gen.py [OPTIONS] [INPUT_FILE(.json)] [OUTPUT_PATH(dir)]`

Full input example:

`python kle-gen.py -kt iso -ks 80 -kc #a5a5a5 -lc #aaaaaa -sl 2 ./colemak.json .`

Minimum input example:

`python kle-gen.py ./colemak.json .`

The last argument MUST be the output path. Simply add '.' to default to the script dir. Must be a directory.

The second to last argument MUST be the KLFC .json file to convert. Absolute or relative path.

## Options:

`-kt / --keyboard-type (optional): Keyboard type. Defaults to ANSI. Can be ANSI, ISO, JIS or ABNT.`

`-ks / --keyboard-size (optional): Keyboard size (integer; 100, 80 or 60). Defaults to 100%.`

`-kc / --key-color     (optional): Key color (hex value). Defaults to grey.`

`-lc / --label-color   (optional): Label color (hex value). Defaults to off-white.`

`-bc / --back-color   (optional): Keyboard background color (hex value). Defaults to grey.`

`-sl / --shift-levels  (optional): Shift levels (integer, 1-4). Shift levels will be placed in the following order: top left, bottom left, top right, bottom right. Defaults to 2.`

