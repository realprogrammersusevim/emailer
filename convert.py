import argparse
from email.message import EmailMessage

import frontmatter
import markdown2

parser = argparse.ArgumentParser(description="Convert Markdown to Email")
parser.add_argument("input", type=argparse.FileType("r"), help="Input file")
parser.add_argument("-o", "--output", type=argparse.FileType("w"), help="Output file")
parser.add_argument("-w", "--wrap", action="store_true", help="Don't preserve wrapping")
args = parser.parse_args()

# Read the text file
with args.input as f:
    source = f.read()

# Extract Yaml block from beginning
frontmatter = frontmatter.loads(source)
metadata = frontmatter.metadata
content = frontmatter.content

# Add line breaks to markdown
if not args.wrap:
    formatted = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if i != len(lines) - 1:
            if line != "" and lines[i + 1] != "":
                formatted.append(f"{line}<br>")
            else:
                formatted.append(line)
        else:
            formatted.append(line)

    formatted_md = "\n".join(formatted)
else:
    formatted_md = content

# Convert Markdown to HTML
markdowner = markdown2.Markdown()
html_content = markdowner.convert(formatted_md)

# Create email file
msg = EmailMessage()
msg["Subject"] = metadata["subject"]
msg["From"] = metadata["from"]
msg["To"] = metadata["to"]
msg.set_content(html_content, subtype="html")

if args.output:
    with args.output as f:
        f.write(msg.as_string())
else:
    print(msg.as_string())
