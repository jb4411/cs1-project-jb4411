"""
file: html_builder.py
description: This program has two different modes, wizard mode and website
mode. When no command line arguments are provided this program will run in
wizard mode and the user will build a one page website in real time. However if
one or more files are provided as command line arguments, this program will run
in website mode. When run in website mode the program will use the files
provided in the command line arguments to build the body of the website's html
file(s).
language: python3
author: jb4411@g.rit.edu Jesse Burdick-Pless
"""
import sys
import turtle
from dataclasses import dataclass
from typing import Union

@dataclass
class Paragraph:
    title: str
    content: str
    images: Union[list, None]

@dataclass
class FileLink:
    name: str
    file: str

def lower_case(string):
    """
    This function takes a string as input, makes each character lowercase and
    returns the resulting string.
    :param string: The string to be made lowercase
    :return: The lowercase version of string
    """
    new_str = ""
    for letter in string:
        letter = ord(letter)
        if letter > 64 and letter < 91:
            letter += 32
        letter = chr(letter)
        new_str += letter
    return new_str

def print_fonts(fonts):
    """
    This function takes a list of valid fonts as a parameter and prints them
    along with their corresponding index in the list.
    :param fonts: A list of valid fonts.
    :return: None
    """
    print("Choose a font by its number.")
    i = 0
    for element in fonts:
        print(str(i) + ":", element + ", size 14")
        i += 1

def validate_color(legal_colors):
    """
    This function takes a list of valid colors as a parameter and repeatedly
    asks the user to enter colors until they enter a valid color. The chosen
    color is then returned.
    :param legal_colors: A list of valid html colors.
    :return: The color chosen by the user.
    """
    color = input("Choose the name of a color, or in '#XXXXXX' format: ")
    if color[0] != "#":
        color = lower_case(color)
    while color not in legal_colors:
        color = input("Choose color name or '#XXXXXX': ")
        color = lower_case(color)
    return color

def mk_paragraph():
    """
    This function prompts the user for the title of their paragraph and the
    content of the paragraph. It then asks if the user would like to add any
    images. The user can then add as many paragraphs as they would like, each
    with any number of images. Once the user has finished entering paragraphs
    they are turned into valid html and returned.
    :return: The created html representing the paragraphs entered by the user.
    """
    paragraph_title = input("Title of your paragraph: ")
    print("Content of your paragraph (single line)")
    paragraph_content = input("")
    add_images = input("Do you want to add images? [yes] ")
    images = []
    if add_images == "" or lower_case(add_images) == "yes":
        while add_images == "" or lower_case(add_images) == "yes":
            file = input("Image file name: ")
            images += [file]
            add_images = input("Do you want to add another image? [yes] ")

    if images != []:
        paragraph = Paragraph(paragraph_title, paragraph_content, images)
    else:
        paragraph = Paragraph(paragraph_title, paragraph_content, None)
    return paragraph

def run_prompts():
    """
    This function prompts the user to enter a color for the website background,
    a font style, a color for the website paragraphs and a color for the
    website headings.
    :return: The selected background color, font style, paragraph color and
    heading color.
    """
    legal_colors = set()
    with open("valid_colors.txt") as colors:
        for line in colors:
            line = line.strip()
            line = line.split(":")
            for color in line:
                legal_colors.add(color)

    print("Background Color")
    bg_color = validate_color(legal_colors)

    fonts = ["Arial", "Comic Sans MS", "Lucida Grande", "Tahoma", "Verdana", "Helvetica", "Times New Roman"]
    draw_font = input("Do you want to see what the fonts look like? [yes] ")
    if lower_case(draw_font) == "yes" or draw_font == "":
        print("Close the window when you have made your choice.")
        print_fonts(fonts)
        turtle.setup(200, 250)
        turtle.hideturtle()
        turtle.tracer(False)
        turtle.up()
        turtle.title("Font Options")
        turtle.goto(-60, 75)
        for element in fonts:
            turtle.write(element, False, "left", (element, 14, "normal"))
            turtle.up()
            turtle.right(90)
            turtle.forward(25)
            turtle.left(90)
            turtle.down()
        turtle.done()
    else:
        print_fonts(fonts)
    font = input(" >> ")
    valid_nums = set()
    for i in range(7):
        valid_nums.add(str(i))

    while font not in valid_nums:
        print("Please enter a valid number.")
        font = input(" >> ")
    font = fonts[int(font)]

    print("Paragraph Color")
    paragraph_color = validate_color(legal_colors)

    print("Heading Color")
    heading_color = validate_color(legal_colors)

    return bg_color, font, paragraph_color, heading_color

def make_file(filename,website_title,bg_color,paragraph_color,heading_color,font,paragraphs,files_to_link=None):
    """
    This function takes all of the information about the website to be created
    and turns it into a valid html file that is saved in the home directory of
    this Python program.
    :param filename: The name of the html file created.
    :param website_title: The title of the website.
    :param bg_color: The background color selected by the user.
    :param paragraph_color: The paragraph color selected by the user.
    :param heading_color: The heading color selected by the user.
    :param font: The font style selected by the user.
    :param paragraphs: A list of paragraphs to be on the website.
    :param files_to_link: Files to link to at the top of the page if any.
    :return: None
    """
    style = []
    with open("style_template.txt") as f:
        for line in f:
            line = line.strip()
            style += [line]

    file = open(filename, "w+")
    title = "<title>" + website_title
    for element in ["<!DOCTYPE html>", "<html>", "<head>", title, "</title>"]:
        file.write(element + "\n")

    # style
    for element in style:
        idx = None
        for i in range(len(element)):
            if element[i] != "@":
                continue
            else:
                idx = i
                break

        if idx is not None:
            start = element[:i]
            end = element[i + 10:]
            variable = element[i:i + 10]
            variable = variable.strip()
            if variable == "@BACKCOLOR":
                new_piece = bg_color
            elif variable == "@FONTCOLOR":
                new_piece = paragraph_color
            elif variable == "@HEADCOLOR":
                new_piece = heading_color
            elif variable == "@FONTSTYLE":
                new_piece = font
            new_line = start + new_piece + end
            file.write(new_line + "\n")
        else:
            file.write(str(element) + "\n")

    h1 = "<h1>" + website_title
    for element in ["</head>", "<body>", h1, "</h1>", "<hr/>"]:
        file.write(element + "\n")

    if files_to_link is not None and len(sys.argv) > 2:
        html_links = '<p align="center">'
        for html_file in files_to_link:
            website_link = '<a href="' + html_file.file + '">' + html_file.name + '</a>---'
            html_links += website_link
        for element in [html_links,"</p>"]:
            file.write(element + "\n")

    for paragraph in paragraphs:
        file.write("<h2>" + paragraph.title + "\n")
        file.write("</h2>" + "\n")
        file.write("<p>" + paragraph.content + "\n")
        file.write("</p>" + "\n")
        if paragraph.images is not None:
            for image in paragraph.images:
                image = image.strip()
                if image[-1] != "%":
                    file.write('<img src="' + image + '" class="center">' + "\n")
                else:
                    percent = image[-4:]
                    percent = percent.strip()
                    file.write('<img src="' + image[:-3] + '" width="' + percent + '" class="center">' + "\n")

    for element in ["</body>", "</html>"]:
        file.write(element + "\n")

    file.close()

def run_wizard_mode():
    """
    This function prompts the user to enter all of the information
    about the website they would like to create. The data entered is then used
    to create a valid html file with the information entered by the user. The
    html file is then saved as "index.html" in the home directory of this
    Python program.
    :return: None
    """
    website_title = input("What would you like the title of your website to be? ")

    bg_color, font, paragraph_color, heading_color = run_prompts()

    paragraphs = []
    paragraphs += [mk_paragraph()]

    more_paragraphs = input("Do you want to add another paragraph to your website? [yes] ")
    while more_paragraphs == "" or lower_case(more_paragraphs) == "yes":
        paragraphs += [mk_paragraph()]
        more_paragraphs = input("Do you want to add another paragraph to your website? [yes] ")

    make_file("index.html", website_title, bg_color, paragraph_color, heading_color, font, paragraphs)

    print("Your web page has been saved as index.html")

def run_website_mode():
    """
    This function calls run_prompts() to prompt the user to enter a background
    color, font style, paragraph color and heading color for their website.
    This is then used to create the style portion of the html for their
    website. The file(s) provided in the command line arguments are then used
    to construct the body of the html file(s) for the user's website. The
    created file(s) are then saved in the home directory of this Python
    program.
    :return: None
    """
    names = []
    for i in range(len(sys.argv)):
        if i == 0:
            continue
        with open(sys.argv[i]) as f:
            first_line = f.readline().strip()
            names += [first_line]

    html_files = []
    for i in range(len(sys.argv)):
        if i != 0:
            filename = sys.argv[i]
            filename = filename[:-4]
            filename += ".html"
            html_files += [filename]

    files_to_link = []
    for i in range(len(html_files)):
        files_to_link += [FileLink(names[i],html_files[i])]

    bg_color, font, paragraph_color, heading_color = run_prompts()
    for i in range(len(sys.argv)):
        if i == 0:
            continue
        paragraphs = []
        line_num = 1
        current_paragraph = None
        images = []
        content = ""
        with open(sys.argv[i]) as f:
            for line in f:
                if line_num != 1:
                    if line[0] == "!":
                        if line.strip() == "!new_paragraph":
                            if current_paragraph is None:
                                current_paragraph = Paragraph("title","content",None)
                                continue
                            else:
                                if images != []:
                                    current_paragraph.images = images
                                    images = []
                                current_paragraph.content = content
                                paragraphs += [current_paragraph]
                                current_paragraph = Paragraph("title","content",None)
                                content = ""
                        elif line[:6] == "!title":
                            current_paragraph.title = line[7:]
                        elif line[:6] == "!image":
                            images += [line[7:]]
                    else:
                        if line.strip() != "":
                            content += line
                        else:
                            continue
                else:
                    line = line.strip()
                    website_title = line
                line_num += 1

        if images != []:
            current_paragraph.images = images
        current_paragraph.content = content
        paragraphs += [current_paragraph]

        filename = sys.argv[i]
        filename = filename[:-4]
        filename += ".html"

        make_file(filename, website_title, bg_color, paragraph_color, heading_color, font, paragraphs,files_to_link)

    if len(sys.argv) == 2:
        print("Your file has been saved.")
    else:
        print("Your files have been saved.")

def main():
    """
    If no command line arguments are present this function calls
    run_wizard_mode() so the user can build a website in real time. However if
    there are command line arguments present this function calls
    run_website_mode() to build the website using the files provided in the
    command line arguments.
    :return: None
    """
    if len(sys.argv) == 1:
        run_wizard_mode()
    else:
        run_website_mode()

if __name__ == '__main__':
    main()