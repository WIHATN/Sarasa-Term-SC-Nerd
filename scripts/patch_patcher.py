import sys, re

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

if '# FOR SARASA' in text:
    print("font-patcher already patched, skipping.")
    sys.exit(0)

# ── Hunk 1: header variables ─────────────────────────────────────────────────
INSERT_1 = '''
# FOR SARASA
projectName = "Nerds"
projectNameAbbreviation = ""
projectNameSingular = projectName[:-1]
subFamily = ""
looseName = "Sarasa Term SC Nerd"
compactName = "SarasaTermSCNerd"
'''
text = text.replace(
    'projectName = "Nerd Fonts"\n',
    'projectName = "Nerd Fonts"\n' + INSERT_1
)

# ── Hunk 2: check_panose_monospaced ──────────────────────────────────────────
text = text.replace(
    '    return 1 if panose_mono else 0\n',
    '    # FOR SARASA\n    return 1\n    # return 1 if panose_mono else 0\n'
)

# ── Hunk 3: is_monospaced ─────────────────────────────────────────────────────
text = text.replace(
    'def is_monospaced(font):\n    """ Check if a font is probably monospaced """\n    # Some fonts lie',
    'def is_monospaced(font):\n    """ Check if a font is probably monospaced """\n    # FOR SARASA\n    return (True, None)\n\n    # Some fonts lie'
)

# ── Hunk 4: output filename override ─────────────────────────────────────────
text = re.sub(
    r'(outfile = os\.path\.normpath\(os\.path\.join\(\s*sanitize_filename\(self\.args\.outputdir, True\),\s*sanitize_filename\(fontname\) \+ self\.args\.extension\)\))',
    r"""\1

            # FOR SARASA
            outfile = os.path.normpath(os.path.join(
                sanitize_filename(self.args.outputdir, True),
                f'{compactName}-{self.get_subfamily()}.ttf'
            ))""",
    text
)

# ── Hunk 5: post_fix call ─────────────────────────────────────────────────────
text = text.replace(
    '        if self.args.postprocess:\n            subprocess.call([self.args.postprocess, outfile])',
    '        # FOR SARASA: build hdmx table\n        print("Building hdmx table and fix post table")\n        post_fix(self.args.font, outfile)\n\n        if self.args.postprocess:\n            subprocess.call([self.args.postprocess, outfile])'
)

# ── Hunk 6: Material Design icon range split ─────────────────────────────────
MDI_OLD = """{'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF0001,'SymEnd': 0xF1AF0,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},"""
MDI_NEW = """            # FOR SARASA: split to avoid 65534 glyph limit
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF0001,'SymEnd': 0xF0553,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF0565,'SymEnd': 0xF0E32,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF0E40,'SymEnd': 0xF0E85,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF0E8E,'SymEnd': 0xF0FFF,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF119E,'SymEnd': 0xF11AE,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF11E3,'SymEnd': 0xF126F,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF129E,'SymEnd': 0xF13ED,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF13FE,'SymEnd': 0xF149F,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF14B0,'SymEnd': 0xF14CF,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF14DE,'SymEnd': 0xF165C,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},
            {'Enabled': self.args.material,             'Name': "Material",                'Filename': "materialdesign/MaterialDesignIconsDesktop.ttf",  'Exact': True,  'SymStart': 0xF19E8,'SymEnd': 0xF19FD,'SrcStart': None,   'ScaleRules': MDI_SCALE_LIST,   'Attributes': SYM_ATTR_DEFAULT},"""
if MDI_OLD in text:
    text = text.replace('            ' + MDI_OLD, MDI_NEW)
else:
    print("WARNING: Material Design hunk not found — check font-patcher version")

# ── Hunk 7: get_subfamily method ──────────────────────────────────────────────
SUBFAMILY = '''
    # FOR SARASA: extract subFamily from font name
    def get_subfamily(self):
        file_name = self.args.font.split('.')[-2]
        return file_name.split('-')[-1]
'''
text = text.replace(
    '\ndef half_gap(',
    SUBFAMILY + '\ndef half_gap('
)

# ── Hunk 8: font_dim em field ─────────────────────────────────────────────────
OLD_DIM = "self.font_dim = {'xmin': 0, 'ymin': 0, 'xmax': 0, 'ymax': 0, 'width' : 0, 'height': 0, 'iconheight': 0, 'ypadding': 0}"
NEW_DIM = (OLD_DIM +
    "\n\n        # FOR SARASA\n"
    "        self.font_dim = {'xmin': 0, 'ymin': 0, 'xmax': 0, 'ymax': 0, 'width' : 0, 'height': 0, 'iconheight': 0, 'ypadding': 0, 'em': 0}\n"
    "        self.font_dim['em'] = self.sourceFont.em")
text = text.replace(OLD_DIM, NEW_DIM)

# ── Hunk 9: get_target_width force return 1 ───────────────────────────────────
text = re.sub(
    r'(def get_target_width\(self, stretch\):.*?""".*?\n)',
    r'\1        # FOR SARASA\n        return 1\n\n',
    text,
    flags=re.DOTALL,
    count=1
)

# ── Hunk 10: SFNT name injection ──────────────────────────────────────────────
SFNT_INJECT = '''
        # FOR SARASA
        font.familyname = looseName
        subFamily = self.get_subfamily()
        font.fullname = f"{looseName} {en_subfamily(subFamily)}"
        font.fontname = f"{compactName}-{subFamily}"
        uniqueID = f"{font.fullname}; Sarasa v{self.sourceFont.version}"

        font.appendSFNTName(str("English (US)"), str("UniqueID"), uniqueID)
        font.appendSFNTName(str("Chinese (PRC)"), str("UniqueID"), uniqueID)
        font.appendSFNTName(str('English (US)'), str('Fullname'), font.fullname)
        font.appendSFNTName(str("Chinese (PRC)"), str("Fullname"), zh_family(font.fullname))

        font.appendSFNTName(str('English (US)'), str('Family'), font.familyname)
        font.appendSFNTName(str('Chinese (PRC)'), str('Family'), zh_family(font.familyname))
        font.appendSFNTName(str('English (US)'), str('SubFamily'), en_subfamily(subFamily))
        font.appendSFNTName(str('Chinese (PRC)'), str('SubFamily'), zh_subfamily(subFamily))

        font.appendSFNTName(str('English (US)'), str('Preferred Family'), font.familyname)
        font.appendSFNTName(str('Chinese (PRC)'), str('Preferred Family'), zh_family(font.familyname))
        font.appendSFNTName(str('English (US)'), str('Preferred Styles'), en_subfamily(subFamily))
        font.appendSFNTName(str('Chinese (PRC)'), str('Preferred Styles'), zh_subfamily(subFamily))

'''
text = text.replace(
    '\n        font.comment = projectInfo\n        font.fontlog = projectInfo',
    SFNT_INJECT + '\n        font.comment = projectInfo\n        font.fontlog = projectInfo'
)

# ── Hunk 11: helper functions at end of file ──────────────────────────────────
HELPERS = '''
def zh_family(name):
    res = name.replace(looseName, "更纱终端书呆黑体-简")
    res = res.replace(compactName, "更纱终端书呆黑体-简")
    return res

def en_subfamily(compact):
    return compact.replace("Italic", " Italic").strip()

def zh_subfamily(compact):
    sub_family_dict = {
        "ExtraLight": "特细体",
        "ExtraLightItalic": "特细斜体",
        "Light": "细体",
        "LightItalic": "细斜体",
        "Regular": "常规体",
        "Italic": "斜体",
        "SemiBold": "中粗体",
        "SemiBoldItalic": "中粗斜体",
        "Bold": "粗体",
        "BoldItalic": "粗斜体",
    }
    return sub_family_dict.get(compact, compact)

# FOR SARASA: build hdmx table and fix post table
import math
from fontTools.ttLib import TTFont, newTable

def post_fix(src_file, dst_file):
    dst_font = TTFont(dst_file, recalcBBoxes=False)
    build_hdmx(dst_font)
    fix_isFixedPitch(dst_font)
    src_font = TTFont(src_file)
    dst_font["OS/2"].xAvgCharWidth = src_font["OS/2"].xAvgCharWidth
    src_font.close()
    dst_font.save(dst_file)
    dst_font.close()

def build_hdmx(font):
    headFlagInstructionsMayAlterAdvanceWidth = 0x0010
    sarasaHintPpemMin = 11
    sarasaHintPpemMax = 48
    originalFontHead = font["head"]
    originalFontHmtx = font["hmtx"]
    originalFontHead.flags |= headFlagInstructionsMayAlterAdvanceWidth
    hdmxTable = newTable("hdmx")
    hdmxTable.hdmx = {}
    for ppem in range(
        math.floor(sarasaHintPpemMin / 2) * 2 + 1, sarasaHintPpemMax + 1, 2
    ):
        halfUpm = originalFontHead.unitsPerEm / 2
        halfPpem = math.ceil(ppem / 2)
        hdmxTable.hdmx[ppem] = {
            name: math.ceil(width / halfUpm) * halfPpem
            for name, (width, _) in originalFontHmtx.metrics.items()
        }
    font["hdmx"] = hdmxTable

def fix_isFixedPitch(font):
    font["post"].__dict__["isFixedPitch"] = 1

'''
text = text.replace(
    '\nif __name__ == "__main__":',
    HELPERS + '\nif __name__ == "__main__":'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied successfully.")
