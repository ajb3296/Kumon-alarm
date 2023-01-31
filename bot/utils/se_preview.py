from bs4 import BeautifulSoup

from bot import se_board_link
from bot.utils.crawler import getText

async def get_preview(post_id: int) -> tuple:
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    link = f"{se_board_link}freeboard/{post_id}"

    html = await getText(link, header)
    parse = BeautifulSoup(html, 'lxml')

    post = parse.find('div', {'class': 'read_body'})
    if post is not None:
        text_list = post.find_all('p')

    # Set img preview
    img_preview = None
    try:
        img_preview = post.find('img')['src'].replace("./", "")
    except:
        pass

    text = ''
    for i in text_list:
        text += i.get_text() + " "
    
    if len(text) <= 100:
        result = text
    else:
        result = f'{text[:100]} ...[더보기]({link})'
    
    return img_preview, result