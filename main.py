import re
import sys

Words = {
    "if", "else", "while", "return",
    "int", "char", "void", "bool", "true", "false"
}

Tokens = [
    ("COMMENT_BLOCK", r"/\*.*?\*/", re.S),
    ("COMMENT_LINE",  r"//[^\n]*"),
    ("STRING",        r'"([^"\\]|\\.)*"'),
    ("CHAR",          r"'([^'\\]|\\.)'"),
    ("NUMBER",        r"\b\d+\b"),
    ("ID",            r"\b[_A-Za-z]\w*\b"),
    ("SPACES",            r"\s+"),
    ("OP",            r"==|!=|<=|>=|\|\||&&|[+\-*/%<>=!;,(){}[\]]"),
    ("MISC",          r".") 
]


def build_regex():
    parts = []
    flags = 0
    for name, pat, *fl in Tokens:
        f = fl[0] if fl else 0
        parts.append(f"(?P<{name}>{pat})")
        flags |= f
    return re.compile("|".join(parts), flags)


MASTER = build_regex()


def tokenize(code):
    for m in MASTER.finditer(code):
        kind = m.lastgroup
        text = m.group()
        if kind in ("COMMENT_BLOCK", "COMMENT_LINE", "SPACES"):
            continue  
        yield kind, text


def obfuscate(code):
    id_map = {}
    counter = 0
    out = []
    prev_kind = None

    for kind, text in tokenize(code):
        if kind == "ID":
            if text in Words:
                token = text
            else:
                if text not in id_map:
                    id_map[text] = f"_{counter}" #_0 _1
                    counter += 1
                token = id_map[text]
        else:
            token = text

        if prev_kind in ("ID", "NUMBER", "STRING", "CHAR") and kind in ("ID", "NUMBER", "STRING", "CHAR"):
            out.append(" ")

        out.append(token)
        prev_kind = kind

    return "".join(out)


def main():
    print("=== C-Mini Obfuscator ===")
    input_path = input("مسیر فایل ورودی را وارد کنید: ").strip()
    output_path = input("نام فایل خروجی را وارد کنید: ").strip()

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            src = f.read()

        result = obfuscate(src)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"\nعملیات مبهم‌سازی انجام شد.\nخروجی در فایل «{output_path}» ذخیره شد.")
    except FileNotFoundError:
        print("خطا فایل ورودی پیدا نشد")
    except Exception as e:
        print(f"خطای غیرمنتظره: {e}")


if __name__ == "__main__":
    main()
