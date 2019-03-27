from datetime import datetime
import os
import requests

from blogist.types import Post, User, Comment, WrongUsername, List


class Gist:
    def __init__(self, username: str, prefix: str, form: str):
        self.username = username
        self.API = 'https://api.github.com'
        self.TIME = '%Y-%m-%dT%H:%M:%SZ'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json'
        })
        if not self.check_username():
            raise WrongUsername(f'{username} is not found in GitHub.')

        self.user = None
        self.prefix = prefix
        self.format = form
        self.posts = []

    def check_username(self) -> bool:
        resp = self.session.get(f'{self.API}/users/{self.username}')
        if resp.ok:
            data = resp.json()
            if data.get('type', '') == 'User':
                self.user = User(
                    data.get('login'),
                    data.get('name'),
                    data.get('url'),
                    data.get('html_url'),
                    data.get('avatar_url'),
                )
                return True
        return False

    def fetch_all_posts(self):
        url = f'{self.API}/users/{self.username}/gists'
        while True:
            resp = self.session.get(url)
            if resp.ok:
                data = resp.json()
                for gist in data:
                    files = gist.get('files')
                    for file in files:
                        if file.startswith(self.prefix) and file.endswith(f'.{self.format}'):
                            self.posts.append(Post(
                                self.user,
                                file.replace(self.prefix, '', 1),
                                datetime.strptime(gist.get('created_at'), self.TIME),
                                datetime.strptime(gist.get('updated_at'), self.TIME),
                                gist.get('description'),
                                self.get_post_body(files[file].get('raw_url')),
                                self.get_comments(gist.get('comments_url')) if gist.get('comments', 0) > 0 else []
                            ))
                            break # only one file will be add to posts

                next_url = resp.links.get('next')
                if next_url:
                    url = next_url.get('url')
                    continue
            break


    def generate_file_name(self, post: Post) -> str:
        date = post.created_at
        return f'{date.year}-{date.month}-{date.day}-{post.title}'

    def get_post_body(self, url: str) -> str:
        if url is None:
            return ''
        resp = self.session.get(url)
        if resp.ok:
            return resp.text
        return ''

    def get_comments(self, url: str) -> List[Comment]:
        if url is None:
            return []
        resp = self.session.get(url)
        comments = []
        if resp.ok:
            data = resp.json()
            for comment in data:
                user = comment.get('user', {})
                comments.append(Comment(
                    User(
                        user.get('login'),
                        '',
                        user.get('url'),
                        user.get('html_url'),
                        user.get('avatar_url'),
                    ),
                    comment.get('body'),
                    comment.get('created_at'),
                    comment.get('updated_at'),
                ))

        return comments

    def store(self, path: str):
        if not os.path.isdir(path):
            os.mkdir(path)

        for post in self.posts:
            with open(os.path.join(path, self.generate_file_name(post)), 'w', encoding='utf-8') as f:
                f.write(f'---\ntitle: {post.title.rsplit(".", 1)[0]}\n---\n')
                f.write(f'\n{post.description}\n\n<!--more-->\n\n')
                f.write(post.body)
                if post.comments:
                    f.write('\n\n')
                    for com in post.comments:
                        f.write(f'[commont@{com.user.login}] [{com.created_at}] ({com.body})\n')
