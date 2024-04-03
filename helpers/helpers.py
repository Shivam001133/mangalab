

def get_chaper_no(chapter_name=None):
    if chapter_name:
        chapter_name = chapter_name.strip().split(' ')
        chapter_no = [i for i in chapter_name if i.isdigit()]
        return chapter_no[0]
    return None
