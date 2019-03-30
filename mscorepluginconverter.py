#!/usr/bin/env python3

import sys
import argparse

def get_line_ending(line):
    end = '\n'
    if line.endswith('\r\n'):
        end = '\r\n'
    return end

def replace_imports(line):
    tokens = line.strip().split()
    if len(tokens) < 3:
        return line
    if tokens[0] == "import":
        if tokens[1] in ["MuseScore", "FileIO"] and tokens[2] == "1.0":
            tokens[2] = "3.0"
        return ' '.join(tokens) + get_line_ending(line)
    return line

def replace_props(line):
    replacement_list = {
        ".pos.x ": ".offsetX ",
        ".pos.x=": ".offsetX=",
        ".pos.y ": ".offsetY ",
        ".pos.y=": ".offsetY=",
        ".setSig(": ".timesig = fraction(",
        }
    for orig, target in replacement_list.items():
        line = line.replace(orig, target)
    return line

def replace_enums(line):
    val_replace = [
        { "orig": "Element", "target": "Placement", "values": ["ABOVE", "BELOW"] },
        { "orig": "MScore", "target": "Direction", "values": ["UP", "DOWN"] },
        { "orig": "MScore", "target": "DirectionH", "values": ["LEFT", "RIGHT"] },
        { "orig": "MScore", "target": "OrnamentStyle", "values": ["DEFAULT", "BAROQUE"] },
        { "orig": "MScore", "target": "GlissandoStyle", "values": ["CHROMATIC", "WHITE_KEYS", "BLACK_KEYS", "DIATONIC"] },
        { "orig": "NoteHead", "target": "NoteHeadType", "values": ["HEAD_AUTO", "HEAD_WHOLE", "HEAD_HALF", "HEAD_QUARTER", "HEAD_BREVIS", "HEAD_TYPES"] },
        { "orig": "Note", "target": "NoteValueType", "values": ["OFFSET_VAL", "USER_VAL"] },
        ]
    # applied after val_replace
    any_replace = [
        { "orig": "TextStyleType", "target": "Tid" },
        { "orig": "NoteHead", "target": "NoteHeadGroup" },
        ]
    ambiguous = ["MScore.AUTO"]

    def replace_enum_val(line, orig_name, target_name, val=""):
        orig_str = orig_name + '.' + val
        target_str = target_name + '.' + val
        return line.replace(orig_str, target_str)

    for item in val_replace:
        orig = item["orig"]
        target = item["target"]
        for val in item["values"]:
            line = replace_enum_val(line, orig, target, val)

    for item in any_replace:
        line = replace_enum_val(line, item["orig"], item["target"])

    for s in ambiguous:
        if s in line:
            print("Ambiguous replacement:", s)

    return line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts MuseScore 2 plugins for usage with MuseScore 3")
    parser.add_argument("source", help="Source plugin .qml file")
    parser.add_argument("destination", help="Destination .qml file")

    args = parser.parse_args()

    with open(args.source, newline='') as src:
        script = list(src)

    if not script:
        print("Empty script")
        sys.exit(1)

    script = map(replace_imports, script)
    script = map(replace_props, script)
    script = map(replace_enums, script)

    with open(args.destination, 'w') as out:
        for line in script:
            out.write(line)
