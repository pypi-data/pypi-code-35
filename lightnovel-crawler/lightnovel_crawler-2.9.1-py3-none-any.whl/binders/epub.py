#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
import os
import re
import base64

try:
    from ebooklib import epub
except Exception as err:
    logging.error(err)
# end try

logger = logging.getLogger('EPUB_BINDER')


def make_intro_page(app):
    logger.info('Creating intro page')
    source_url = app.crawler.home_url or 'Unknown'
    github_url = 'https://github.com/dipu-bd/lightnovel-crawler'

    intro_html = '<div style="%s">' % ';'.join([
        'height: 9in',
        'display: flex',
        'flex-direction: column',
        'justify-content: space-between',
        'text-align: center',
    ])

    intro_html += '''
        <div>
            <h1>%s</h1>
            <h3>%s</h3>
        </div>
    ''' % (
        app.crawler.novel_title or 'N/A',
        app.crawler.novel_author or 'N/A',
    )

    if app.book_cover:
        logger.info('Adding cover: %s', app.book_cover)
        ext = app.book_cover.split('.')[-1]
        with open(app.book_cover, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
        # end with
        intro_html += '<div style="%s">&nbsp;</div>' % ';'.join([
            'height: 4in',
            'width: 100%',
            'background-size: contain',
            'background-repeat: no-repeat',
            'background-position: center',
            'background-image: url(data:image/%s;base64,%s)' % (ext, encoded)
        ])
    # end if

    intro_html += '''
    <div>
        <p><b>Source:</b> <a href="%s">%s</a></p>
        <p><i>Generated by <b><a href="%s">Lightnovel Crawler</a></b></i></p>
    </div>''' % (source_url, source_url, github_url)

    intro_html += '</div>'

    return epub.EpubHtml(
        uid='intro',
        file_name='intro.xhtml',
        title='Intro',
        content=intro_html,
    )
# end def


def make_chapters(book, chapters):
    book.toc = []
    for i, chapter in enumerate(chapters):
        xhtml_file = 'chap_%s.xhtml' % str(i + 1).rjust(5, '0')
        content = epub.EpubHtml(
            # uid=str(i + 1),
            file_name=xhtml_file,
            title=chapter['title'],
            content=chapter['body'] or '',
        )
        book.add_item(content)
        book.toc.append(content)
    # end for
# end def


def bind_epub_book(app, chapters, volume=''):
    book_title = (app.crawler.novel_title + ' ' + volume).strip()
    logger.debug('Binding epub: %s', book_title)

    # Create book
    book = epub.EpubBook()
    book.set_language('en')
    book.set_title(book_title)
    book.add_author(app.crawler.novel_author)
    book.set_identifier(app.output_path + volume)

    # Create intro page
    intro_page = make_intro_page(app)
    book.add_item(intro_page)

    # Create book spine
    book.spine = [intro_page, 'nav']
    # if app.book_cover:
    #     book.set_cover('image.jpg', open(app.book_cover, 'rb').read())
    #     book.spine = ['cover', intro_page, 'nav']
    # else:
    #     book.spine = [intro_page, 'nav']
    # end if

    # Create chapters
    make_chapters(book, chapters)
    book.spine += book.toc
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())

    # Save epub file
    epub_path = os.path.join(app.output_path, 'epub')
    file_name = (app.good_file_name + ' ' + volume).strip()
    file_path = os.path.join(epub_path, file_name + '.epub')
    logger.debug('Writing %s', file_path)
    os.makedirs(epub_path, exist_ok=True)
    epub.write_epub(file_path, book, {})
    print('Created: %s.epub' % file_name)
    return file_path
# end def


def make_epubs(app, data):
    epub_files = []
    for vol in data:
        if len(data[vol]) > 0:
            book = bind_epub_book(
                app,
                volume=vol,
                chapters=data[vol],
            )
            epub_files.append(book)
        # end if
    # end for
    return epub_files
# end def
