import os
import codecs
import getopt
import re
import sys


genstring_cmd = "find ./ -name *.m -print0 | xargs -0 genstrings -o %s"

def collect_file_strings(filepath):
    strings_dict = {}
    infile = codecs.open(filepath, 'r', encoding='utf-16')
    comment = base = translation = ""
    comment_pass = False
    for line in infile:
        line = line.strip()
        if len(line) > 2:
            if not comment_pass:
                comment = line
                comment_pass = True
            else:
                base, translation = line.split(' = ')
                strings_dict[base] = (translation, comment)
                comment_pass = False
    infile.close()
    return strings_dict


def generate_and_merge_strings(lang, lang_dir, filepath):
    print("Collecting existing '%s' strings" % lang)
    collected = collect_file_strings(filepath)
    print("Generating '%s' strings" % lang)
    os.system(genstring_cmd % lang_dir)
    print("Collecting newly '%s' strings" % lang)
    generated = collect_file_strings(filepath)
    print("Merging '%s' strings" % lang)
    for key, value in collected.iteritems():
        if key in generated:
            generated[key] = value
    print("Writing '%s' file strings" % lang)
    outfile = codecs.open(filepath, 'w', encoding='utf-16')
    for key in sorted(generated.keys()):
        value = generated[key]
        outfile.write("%s\n%s = %s\n\n" % (value[1], key, value[0]))
    outfile.close()


project_name = None
languages = []
options, remainder = getopt.getopt(sys.argv[1:], 'l:p:', ['project=', 'lang='])
for opt, arg in options:
    if opt in ('-p', '--project'):
        project_name = arg

    elif opt in ('-l', '--lang'):
        languages.append(arg)

if project_name is None:
    print('No project specified (you can specify a project using -p or --project)')
elif len(languages) == 0:
    print('No language specified (you can specify a language using -l or --lang)')
else:
    for lang in languages:
        lang_dir = os.path.join(os.getcwd(), project_name, lang + '.lproj')
        filepath = os.path.join(lang_dir, "Localizable.strings")
        if not os.path.exists(filepath):
            print('No Localizable.strings for language %s' % lang)
            print('(filepath: %s)' % filepath)
        else:
            generate_and_merge_strings(lang, lang_dir, filepath)




