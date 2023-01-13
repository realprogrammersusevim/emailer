import argparse
from email.message import EmailMessage

import frontmatter
import markdown2

parser = argparse.ArgumentParser(description="Convert Markdown to Email")
parser.add_argument("input", type=argparse.FileType("r"), help="Input file")
args = parser.parse_args()

# Read the text file
with args.input as f:
    source = f.read()

# Extract Yaml block from beginning
frontmatter = frontmatter.loads(source)
metadata = frontmatter.metadata
content = frontmatter.content

# Add line breaks to markdown
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

# Convert Markdown to HTML
markdowner = markdown2.Markdown()
html_content = markdowner.convert(formatted_md)

# Create email file
msg = EmailMessage()
msg["Subject"] = metadata["subject"]
msg["From"] = metadata["from"]
msg["To"] = metadata["to"]
msg.set_content(html_content, subtype="html")
print(msg)
