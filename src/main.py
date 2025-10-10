from textnode import TextNode # type: ignore
import logging, os, shutil, stat
from webpage import generate_page, generate_pages_recursive # type: ignore

def main():
    logging.basicConfig(filename="logging.log",encoding='utf-8',level=logging.DEBUG)
    copy_contents('public', 'static')

    generate_pages_recursive('content', 'template.html', 'public/index.html')


def copy_contents(destination, source):
    if not os.path.exists(destination):
        logging.debug('destination folder does not exist')
        os.mkdir(destination)
    logging.debug(os.listdir(destination))
    if len(os.listdir(destination)) > 0:
        logging.debug(f"removing files in destination folder: {os.listdir(destination)}")
        shutil.rmtree(destination)
        os.mkdir(destination)
    for i in os.listdir(source):
        try:
            logging.debug(f"coppying file/folder to new destination: {os.path.join(source, i)}")
            if os.path.isfile(os.path.join(source, i)):
                shutil.copy(os.path.join(source, i), os.path.join(destination, i))
            else:
                shutil.copytree(os.path.join(source, i), os.path.join(destination, i))
        except PermissionError:
            os.chmod(os.path.join(source, i), stat.S_IRWXO)
            logging.debug(f"coppying file/folder to new destination: {os.path.join(source, i)}")
            if os.path.isfile(os.path.join(source, i)):
                shutil.copy(os.path.join(source, i), os.path.join(destination, i))
            else:
                shutil.copytree(os.path.join(source, i), os.path.join(destination, i))


if __name__ == "__main__":
    main()

